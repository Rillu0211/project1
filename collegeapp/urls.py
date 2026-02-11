from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.loginpage,name='loginpage'),
    path('login1',views.login1,name='login1'),
    path('signup/', views.signup1, name='signup1'),
    path('home',views.home,name='home'),
    path('teacherhome',views.teacherhome,name='teacherhome'),
    path('addcourse1',views.addcourse1,name='addcourse1'),
    path('addcourse',views.addcourse,name='addcourse'),
    path('add_student',views.add_student,name='add_student'),
    path('add_studentdb',views.add_studentdb,name='add_studentdb'),
    path('showstudents',views.showstudents,name='showstudents'),
    path('editstudents/<int:pk>/',views.editstudents,name='editstudents'),
    path('editdb/<int:pk>/',views.editdb,name='editdb'),
    path('delete/<int:pk>/',views.delete,name='delete'),
    path('edit_teacher', views.edit_teacher, name='edit_teacher'),
    path('profile', views.profile, name='profile'),
    path('logout/', views.logout_user, name='logout'),
    path('view-teachers/', views.view_teachers, name='view_teachers'),
    path('delete1/<int:pk>/',views.delete1,name='delete1'),








]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)