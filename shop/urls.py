from django.urls import path
from .admin_panel_views import *
from .views import *



admin_panel_urlpatterns = [
	path('admin_panel', admin_panel),
	path('admin_panel/roles', admin_panel_roles),
	path('admin_panel/categories', admin_panel_product_categories),
	path('admin_panel/categories/delete', admin_panel_delete_category),
	path('admin_panel/tags', admin_panel_tags),
	path('admin_panel/tags/delete', admin_panel_delete_tag),
	path('admin_panel/tags/add', admin_panel_add_tag),
	path('admin_panel/products', admin_panel_products),
	path('admin_panel/products/add', admin_panel_products_add),
	path('admin_panel/products/edit/<int:pid>', admin_panel_edit_product),
	path('admin_panel/remove_tag', admin_panel_remove_product_tag),
	path('admin_panel/add_tag', admin_panel_add_product_tag),
	path('admin_panel/categories/add', admin_panel_add_category),
	path('admin_panel/remove_cat', admin_panel_remove_product_cat),
	path('admin_panel/add_cat', admin_panel_add_product_cat),
	path('admin_panel/delete_product', delete_product)
]

urlpatterns = [
	path('', home),
	path('login', login_view),
	path('register', reg_view),
	path('logout', logout),
	path('catalog', catalog)
] + admin_panel_urlpatterns
