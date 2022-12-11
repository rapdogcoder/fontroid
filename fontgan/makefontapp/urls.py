
from django.urls import path, include
from makefontapp import views
urlpatterns = [
    path('', views.index),
    path('feedback/<int:user_id>/<date>', views.feedback),
    path('aboutus', views.aboutus),
    path('howtouse', views.howtouse),
    path('contact', views.contact),
    path('detail', views.detail)
]

