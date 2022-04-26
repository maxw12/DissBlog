from django.conf.urls.static import static
from django.urls import path

from testdjango import settings
from . import views

urlpatterns = [
    # class based url views
    path('', views.HomeView.as_view(), name='home'),

    # submission
    path('submission/<int:pk>', views.DetailView.as_view(), name='submission-detail'),
    path('submission/<int:pk>/delete', views.DeleteView.as_view(), name='delete_submission'),

    # submit
    path('submit/', views.AddSubmissionView.as_view(), name='submit'),

    # authentication
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.Logout, name='logout'),

    path('mysubmission/', views.MyPostView.as_view(), name='my_post'),

    path('like/<int:pk>', views.LikeView, name='like_post'),

    path('search', views.HomeView.as_view(), name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
