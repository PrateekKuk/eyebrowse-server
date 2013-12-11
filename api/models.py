from django.db import models
from django.contrib.auth.models import User

from datetime import datetime

class FilterListItem(models.Model):
    user = models.ForeignKey(User, null=False, blank=False)
    url = models.URLField(max_length=200, null=False, blank=False)
    date_created = models.DateTimeField(default=datetime.utcnow())
    
    class Meta:
        abstract = True
    
class WhiteListItem(FilterListItem):
    
    class Meta:
        unique_together = ('user','url')

    def __unicode__(self):
        return "Whitelist item %s for %s" % (self.url, self.user.username)

class BlackListItem(FilterListItem):
    
    class Meta:
        unique_together = ('user','url')
    
    def __unicode__(self):
        return "Blacklist item %s for %s" % (self.url, self.user.username)

class EyeHistory(models.Model):
    user = models.ForeignKey(User)

    src = models.CharField(max_length=40, default='')
    url = models.URLField(max_length=2000, default='')
    domain = models.URLField(max_length=2000, default='')
    favIconUrl = models.URLField(max_length=2000, default='')
    title = models.CharField(max_length=2000, default='')

    start_event = models.CharField(max_length=40, default='')
    start_time = models.DateTimeField()

    end_event = models.CharField(max_length=40, default='')
    end_time = models.DateTimeField()

    total_time = models.IntegerField() # store in ms
    
    # store as human readable according to moment.js library: http://momentjs.com/docs/#/displaying/humanize-duration/
    humanize_time = models.CharField(max_length=200, default='') 
    def __unicode__(self):
        return "EyeHistory item %s for %s on %s" % (self.url, self.user.username, self.start_time)