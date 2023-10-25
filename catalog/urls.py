from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import CategoryListView, ProductListView, BlogCreateView, BlogUpdateView, \
    BlogDeleteView, BlogListView, BlogDetailView, IndexView, ProductCreateView, ProductUpdateView, ProductDetailView, \
    ProductDeleteView

app_name = CatalogConfig.name

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('products/<int:pk>/', ProductListView.as_view(), name='electronic_category'),
    path('blog/', BlogListView.as_view(), name='blogs'),
    path('blog/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('blog/create', BlogCreateView.as_view(), name='blog_create'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
    path('blog/edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),
    path('add_product/', ProductCreateView.as_view(), name='add_product'),
    path('edit_product/<int:pk>', ProductUpdateView.as_view(), name='edit_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
