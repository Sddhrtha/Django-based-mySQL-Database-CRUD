from django.urls import path
from django.urls import include

from . import views


app_name = 'userCRUD'
urlpatterns = [
	path('create/', views.CreatedbNames, name = 'CreatedbNames'),
	path('read/', views.ReaddbNames, name = 'ReaddbNames'),
	path('edit/<int:pk>', views.EditdbNames, name = 'EditdbNames'),
	path('update/<int:pk>', views.UpdatedbNames, name = 'UpdatedbNames'),
	path('delete/<int:pk>', views.DeletedbNames, name = 'DeletedbNames'),
]
