from django.urls import path

from . import views

urlpatterns = [
       path('passed/', views.build_passed),
       path('failed/', views.build_failed),
       path("status/", views.build_status),
]

