from django.urls import path
from . import views



urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('consume/delete/<int:pk>/', views.ConsumeDelete.as_view(), name='consume_delete'),
    path('consume/delete-all/', views.ConsumeDeleteAll.as_view(), name='consume_delete_all'),
]
