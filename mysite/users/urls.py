from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path, include

from mysite import settings
from users.views import signup, UserDetailView, UserUpdateView, ConversationListView, ConversationDetailView, \
    ConversationCreateView, MessageCreateView, deleteuser, ProductBYUserListView, Activate

app_name = 'users'

urlpatterns = [
    url(r'^signup/$', signup, name='signup'),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    path("profile/<int:pk>/", UserDetailView.as_view(), name='user_detail'),
    path("profile/update/<int:pk>/", UserUpdateView.as_view(), name='user_update'),
    path("conversations/", ConversationListView.as_view(), name='conversations'),
    path("conversations/<int:pk>/", ConversationDetailView.as_view(), name='conversation_detail'),
    path("conversations/create/", ConversationCreateView.as_view(), name='conversation_create'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('delete_account/<int:pk>/', deleteuser, name='delete_user'),
    path('my_porduct/', ProductBYUserListView.as_view(), name='my_product'),
    path('activate/<str:uuid>/<str:token>', Activate.as_view(), name='activate'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

