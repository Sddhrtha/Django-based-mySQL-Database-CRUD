from django.urls import path, include

from . import views


app_name = 'connection'
urlpatterns = [
	path('<int:pk>', views.Select , name = 'Select'),
	path('read/<int:pk>/<str:table>', views.Read, name = 'Read'),
	path('delete/<int:pk>/<int:row>/<str:table>', views.Delete, name = 'Delete'),
	path('create/<int:pk>/<str:table>', views.Create, name = 'Create'),
	path('update/<int:pk>/<int:row>/<str:table>', views.Update, name = 'Update'),
]