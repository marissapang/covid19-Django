from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
   # path('filter/<str>', views.filteredTrends, name='filtered-trends')
]
