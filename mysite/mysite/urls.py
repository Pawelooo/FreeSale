from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from mysite import settings
from shop.views import ProductDetailView, ProductListView, ProductUpdateView, ProductCreateView, ProductDeleteView, \
      CategoryListView, PromotionCreateView, custom_page_not_found_view
from users.views import signup

urlpatterns = [
      path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
      path('product/', ProductListView.as_view(), name='product_list'),
      path('admin/', admin.site.urls),
      path('users/', include('users.urls', namespace='users')),
      path('users/accounts/signup', signup, name='sign_up'),
      path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
      path('product/create/', ProductCreateView.as_view(), name='product_create'),
      path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
      path('', CategoryListView.as_view(), name='category_list'),
      path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
      path('promotion/create/', PromotionCreateView.as_view(), name='promotion_create'),
      path('404/', custom_page_not_found_view)


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL)


