import urllib
import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import DetailView, UpdateView, ListView, CreateView, DeleteView, FormView

from shop.models import Product
from users.forms import UserInfoUpdateForm, UserForm, MessageForm, UserDeleteForm, ConversationCreateForm, \
    ConversationForm, UserCreateEmailForm
from users.models import UserInfo, Conversation, Message

from django.contrib.auth import get_user_model, login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.token import account_activation_token


def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = UserCreateEmailForm(request.POST)
            if form.is_valid():

                recaptcha_response = request.POST.get('g-recaptcha-response')
                url = 'https://www.google.com/recaptcha/api/siteverify'
                value = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                data = urllib.parse.urlencode(value).encode()
                req = urllib.request.Request(url, data=data)
                response = urllib.request.urlopen(req)
                result = json.loads(response.read().decode())

                if result['success']:
                    user = form.save()
                    user.is_active = False
                    user.save()
                    mail_subject = 'Aktywuj swoje konto. !'
                    current_site = get_current_site(request)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = account_activation_token.make_token(user)
                    activation_link = "{0}/users/activate/{1}/{2}".format(current_site, uid, token)
                    message = "Hello {0},\n {1}".format(user.username, activation_link)
                    to_email = form.cleaned_data.get('email')
                    email = EmailMessage(mail_subject, message, to=[to_email])
                    print(email)
                    email.send()
                    messages.success(request, 'Poprawna rejstracja')
                    UserInfo.objects.get_or_create(user=user)

                else:
                    messages.error(request, 'Nie zaznaczyles reCAPTCHA')
                    return render(request, 'signup.html', messages)
            else:
                return render(request, 'signup.html')


        else:
            form = UserCreateEmailForm()
        return render(request, 'signup.html', {'form': form})
    else:
        messages.info(request, 'Jesteś zalogowany !')
        return redirect(f'/users/profile/update/{request.user.pk}')


class Activate(View):
    def get(self, request, uuid, token):
        try:
            uid = force_text(urlsafe_base64_decode(uuid))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            # activate user and login:
            user.is_active = True
            user.save()
            login(request, user)

            return render(request, 'activation.html')

        else:
            return HttpResponse('Activation link is invalid!')

    def post(self, request):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important, to update the session with the new password
            return HttpResponse('Password changed successfully')


@login_required
def deleteuser(request):
    if request.method == 'POST':
        delete_form = UserDeleteForm(request.POST, instance=request.user)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('blog-home')
    else:
        delete_form = UserDeleteForm(instance=request.user)

    context = {
        'delete_form': delete_form
    }

    return render(request, 'users/delete_account.html', context)


class UserDetailView(DetailView):
    model = User
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # user_info = UserInfo.objects.filter(user=self.request.user).first()
        # context['detail_form'] = UserInfoUpdateForm(instance=user_info)
        return context


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm

    def get_queryset(self):
        return self.model.objects.filter(id=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_info = UserInfo.objects.filter(user=self.request.user).first()
        context['detail_form'] = UserInfoUpdateForm(instance=user_info)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST, instance=request.user)
        user_info, created = UserInfo.objects.get_or_create(user=request.user)
        detail_form = UserInfoUpdateForm(request.POST, instance=user_info)
        if form.is_valid() and detail_form.is_valid():
            form.save(commit=False)
            form.user = request.user
            form.save()
            detail_form.save(commit=False)
            detail_form.user = request.user
            detail_form.save()
            return HttpResponseRedirect('')

        return render(request, 'auth/user_form.html', {'form': form, 'detail_form': detail_form})


class UserDelete(DeleteView):
    model = User


class ConversationListView(ListView):
    model = Conversation

    def get_queryset(self):
        filters = Q(user_1=self.request.user) | Q(user_2=self.request.user)
        return Conversation.objects.filter(filters)


class ConversationDetailView(DetailView):
    model = Conversation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages = Message.objects.filter(conversation_id=self.object.pk).order_by('created_at')
        context['msgs'] = messages
        context['form'] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('message'):
            Message.objects.create(
                message=request.POST['message'],
                user_from=self.request.user,
                conversation=self.get_object()
            )

        return HttpResponseRedirect('')


class ProductBYUserListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'my_product.html'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class MessageCreateView(CreateView):
    model = Message
    fields = '__all__'


class ConversationCreateView(FormView):
    form_class = ConversationCreateForm
    template_name = 'users/conversation_form.html'

    def form_valid(self, form):
        conversation = ConversationForm(data=dict(user_1=self.request.GET.get('user_to'), user_2=self.request.user))
        if conversation.is_valid():
            conversation = conversation.save()
            Message.objects.create(user_from=self.request.user, message=form.cleaned_data['message'],
                                   conversation=conversation)
            return redirect('users:conversation_detail', pk=conversation.id)
        return redirect('product_list')

