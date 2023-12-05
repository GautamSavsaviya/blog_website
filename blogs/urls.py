from django.urls import path
from . import views

app_name = 'blogs'

urlpatterns = [
    path('', views.index, name="index"),
    path('detail/<slug>', views.detail, name='detail'),
    path('my-blogs/', views.my_blogs, name='my_blogs'),
    path('add-blog/', views.add_blog, name='add_blog'),
    path('update-blog/<slug>', views.update_blog, name='update_blog'),
    path('delete-blog/<slug>', views.delete_blog, name='delete_blog'),
]
