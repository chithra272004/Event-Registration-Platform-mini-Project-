from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('organisedevents/', views.organisedevents, name='organisedevents'),
    path('members/', views.members,name='members'),
    path('login/', views.login_view,name='login'),
    path('home/', views.home,name='home'),
    path('eventdetails/<pk>', views.eventdetails,name='eventdetails'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('addevent/', views.addevent, name='addevent'),
    path('', views.home, name='home'),
    path('delete_event/<pk>', views.delete_event,name='delete_event'),
    path('register/<pk>', views.register,name='register'),
    path('edit_event/<pk>',views.edit_event, name='edit_event'),
    path('reg_detail/<event_id>', views.reg_detail, name='reg_detail'),
    path('logout/', views.user_logout, name='logout')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)