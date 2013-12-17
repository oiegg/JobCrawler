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

    def toDict(self, withContent=False):
        res = {}
        for p in ['title', 'source_url', 'post_url', 'category', 'post_status', 'retry']:
            res[p] = getattr(self, p)
        res['add_time'] = str(self.add_time)
        if self.post_time:
            res['post_time'] = str(self.post_time)
        else:
            res['post_time'] = None
        if withContent:
            res['content'] = self.content
        return res


class G(models.Model):
    OIEGG_USERNAME = models.CharField(max_length=128)
    OIEGG_PASSWORD = models.CharField(max_length=128)
    CRAWLER_STATUS = models.IntegerField()
    POSTER_STATUS = models.IntegerField()
