from django.db import models

# Create your models here.

class dbNames(models.Model):

	dbName = models.CharField(max_length = 100)
	dbUsername = models.CharField(max_length = 100)
	dbPassword = models.CharField(max_length = 100)
	dbHost = models.CharField(max_length = 100)
	dbPort = models.IntegerField()

	def __str__(self):
		return self.dbName



