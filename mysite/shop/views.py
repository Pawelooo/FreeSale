import random
from urllib import request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, InvalidPage, Paginator
from django.db.models import F, Q, Count
from django.shortcuts import redirect, render
from django.template import response, RequestContext
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, FormView
from hitcount.views import HitCountDetailView

from shop.forms import PromotionCreateForm
from shop.models import Product, Category, Promotion, PROMOTION_CHOICES
from users.models import UserInfo


class ProductDetailView(HitCountDetailView):
    model = Product
    count_hit = True


class ProductListView(ListView):
    model = Product
    paginate_by = 16

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        products = []
        for product in context['object_list']:
            promotions = list(
                product.promotion_set
                    .filter(end_date__gte=timezone.now())
                    .values_list('promotion_type', flat=True)
                    .distinct()
            )

            product.promotions = [dict(PROMOTION_CHOICES).get(promotion) for promotion in promotions]
            products.append(product)
        context['object_list'] = products
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        products = Product.objects.all().annotate(highlight=Count('promotion',
                                                                  filter=Q(promotion__end_date__gte=timezone.now(),
                                                                           promotion__promotion_type=
                                                                           PROMOTION_CHOICES[0][0]))).order_by(
            '-highlight')
        # products = products.order_by('-promotion__promotion_type')
        category = self.request.GET.get('category')

        if category:
            products = products.filter(category_id=category)
        product_name = self.request.GET.get('q')
        if product_name:
            products = products.filter(name__icontains=product_name)
        return products


# TODO filtorwanie ogłoszen poprzez najwieksza ilosc wyśiwtleń

class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'price', 'description', 'category', 'image']

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(ProductUpdateView, self).form_valid(form)


class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'price', 'description', 'category', 'image']
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        return super(ProductCreateView, self).form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product_list')

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class CategoryListView(ListView):
    model = Category


class PromotionCreateView(FormView):
    form_class = PromotionCreateForm
    template_name = 'shop/promotion_form.html'

    def form_valid(self, form):
        # Todo filtorwanie produktów użtykownika
        # ToDo przekierowanie na formularz
        if form.is_valid():
            promotion = form.save(commit=False)
            user_info, created = UserInfo.objects.get_or_create(user=self.request.user)
            price = promotion.get_price()
            if user_info.balance > price:
                user_info.balance = F('balance') - price
                user_info.save()
                promotion.save()
            else:
                messages.error(self.request, 'Nie masz tyle pieniędzy. Doładuj Konto ! ')
                return redirect('promotion_create')
            return redirect('product_list')
        return redirect('product_list')

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form_kwargs = self.get_form_kwargs()
        form_kwargs['user'] = request.user
        form = form_class(**form_kwargs)
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)


def custom_page_not_found_view(request):
    return render(request, 'templates/404.html', status=404)


