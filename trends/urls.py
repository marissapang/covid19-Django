from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="trends-index"),
    path('local-gov-update', views.localGovUpdate, name="local-gov-update")
]
