from django.conf.urls import include, url

from website.raspi import views

urlpatterns = [
    url(r'^picture/', views.picture),
]