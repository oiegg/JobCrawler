from django.db import models

# Create your models here.


class Info(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    category = models.IntegerField()
    source_url = models.CharField(max_length=1024)
    add_time = models.DateTimeField()
    post_url = models.CharField(max_length=256)
    post_time = models.DateTimeField()
    post_status = models.IntegerField()


class Gb(models.Model):
    OIEGG_USERNAME = models.CharField(max_length=128)
    OIEGG_PASSWORD = models.CharField(max_length=128)
    CRAWLER_STATUS = models.IntegerField()
    POSTER_STATUS = models.IntegerField()
