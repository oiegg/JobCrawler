from django.db import models

# Create your models here.


class Info(models.Model):
    title = models.CharField(max_length=256, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    category = models.IntegerField()
    source_url = models.CharField(max_length=1024)
    add_time = models.DateTimeField()
    post_url = models.CharField(max_length=256, blank=True, null=True)
    post_time = models.DateTimeField(blank=True, null=True)
    post_status = models.IntegerField()
    retry = models.IntegerField()


class G(models.Model):
    OIEGG_USERNAME = models.CharField(max_length=128)
    OIEGG_PASSWORD = models.CharField(max_length=128)
    CRAWLER_STATUS = models.IntegerField()
    POSTER_STATUS = models.IntegerField()
