from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.files.storage import FileSystemStorage
from django.conf import settings

fs = FileSystemStorage(location=settings.UPLOAD_ROOT, base_url=settings.UPLOAD_URL)

# Create your models here.
class Category(models.Model):
    '''
    A primary category that appears as a top menu item.
    '''
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    ordering = models.IntegerField(default=0, help_text=_('Override alphabetical order in category display.'))

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ['ordering', 'title']


class SecondaryCategory(models.Model):
    '''
    A secondary category that appears as a left menu item.
    '''
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    ordering = models.IntegerField(default=0, help_text=_('Override alphabetical order in category display.'))
    parent = models.ForeignKey(Category)

    def __unicode__(self):
        return u'%s' % self.title



class Photo(models.Model):
    '''
    Photos are all the details about products that go into building your standard gallery on a website.
    '''
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(SecondaryCategory)
    thumb = models.ImageField(upload_to='thumb', storage=fs)
    big = models.ImageField(upload_to='big', storage=fs)


    def __unicode__(self):
        return u'%s' % self.title

