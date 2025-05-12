from django.db import models

# Create your models here.

class Dork(models.Model):
    keyword = models.CharField(max_length=200)
    domain = models.CharField(max_length=200, null=True, blank=True)
    query = models.CharField(max_length=500)
    results = models.TextField(null=True, blank=True)  # Résultats obtenus via scraping

    def __str__(self):
        return self.query
