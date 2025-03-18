from django.urls import path
from .import views


urlpatterns = [
    path('index/', views.index, name='index'),  
    path('blog/', views.blog_list, name='blog'),  
    path('contact/', views.contact, name='contact'),    
    path('sign_up', views.sign_up, name='sign_up'),
    path('log_in', views.log_in, name='log_in'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('delete/<int:id>/', views.delete, name='delete'),  
    path('blog_details/<int:id>/', views.blog_detials, name='blog_details'),
    path('edit_blog/<int:id>/', views.edit_blog, name='edit'),   
    path('profile/edit/', views.edit_profile, name='edit_profile'), 
    

] 

