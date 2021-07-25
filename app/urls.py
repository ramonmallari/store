from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('add_item', views.add_item),
    path('all_items', views.all_items),
    path('logout', views.logout),
    path('edit_account', views.edit),
    path('user/<int:user_id>', views.user),
    path('user/<int:user_id>/user_edit', views.user_edit),
    path('item/<int:item_id>', views.item),
    path('item/<int:item_id>/edit', views.edit),
    path('item/<int:item_id>/edit/update', views.make_edit),
    path('item/<int:item_id>/delete', views.delete_item),
    path('add_to_cart/<int:item_id>', views.add_cart),
    path('view_cart', views.view_cart),
    path('remove/<int:item_id>', views.remove)
    
]