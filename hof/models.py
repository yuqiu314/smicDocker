#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
from django.conf import settings
from django.db import models
from PyPDF2 import PdfFileReader
from wand.image import Image
from uuid import uuid4

def content_file_name(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (instance.id, ext)
    filepath = os.path.join('images', filename)
    fullpath = os.path.join(settings.MEDIA_ROOT, filepath)
    if os.path.exists(fullpath):
        os.remove(fullpath)
    return filepath
    
# Create your models here.
class Employee(models.Model):
    id              = models.CharField(max_length=50, primary_key=True)
    chinesename     = models.CharField(max_length=50)
    preferredname   = models.CharField(max_length=50)
    division        = models.CharField(max_length=50)
    depart          = models.CharField(max_length=50)
    section         = models.CharField(max_length=50)
    hc              = models.CharField(max_length=50)
    bcnt            = models.PositiveIntegerField()
    bscore          = models.PositiveIntegerField()
    brank           = models.PositiveIntegerField()
    bgrade          = models.PositiveIntegerField()
    ccnt            = models.PositiveIntegerField()
    cscore          = models.PositiveIntegerField()
    crank           = models.PositiveIntegerField()
    cgrade          = models.PositiveIntegerField()
    icnt            = models.PositiveIntegerField()
    iscore          = models.PositiveIntegerField()
    irank           = models.PositiveIntegerField()
    igrade          = models.PositiveIntegerField()
    qcnt            = models.PositiveIntegerField()
    qscore          = models.PositiveIntegerField()
    qrank           = models.PositiveIntegerField()
    qgrade          = models.PositiveIntegerField()
    cocnt           = models.PositiveIntegerField()
    coscore         = models.PositiveIntegerField()
    corank          = models.PositiveIntegerField()
    cograde         = models.PositiveIntegerField()
    totalcnt        = models.PositiveIntegerField()
    totalscore      = models.PositiveIntegerField()
    totalrank       = models.PositiveIntegerField()
    totalgrade      = models.PositiveIntegerField()
    head_image      = models.FileField(upload_to=content_file_name, max_length=255,blank=True)
    showcnt         = models.PositiveIntegerField()
    showscore       = models.PositiveIntegerField()
    showrank        = models.PositiveIntegerField()
    showgrade       = models.PositiveIntegerField()

class VisitCount(models.Model):
    cnt = models.PositiveIntegerField()
    
class UploadData(models.Model):
    file = models.FileField(upload_to='excel',max_length=255,blank=True)
    
class UploadPPT(models.Model):
    file = models.FileField(upload_to='ppt',max_length=255,blank=True)
    
class Poll(models.Model):
    question = models.CharField(max_length=200)

    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)
    with_comment = models.BooleanField()

    @property
    def votes(self):
        return len(self.vote_set.all())

    def __unicode__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice)
    comment = models.TextField()
    def has_comment(self):
        return comment != ''
    
class VotedEmp(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    
def process_content_file(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid4().hex, ext)
    filepath = os.path.join('article', filename)
    fullpath = os.path.join(settings.MEDIA_ROOT, filepath)
    
    if os.path.exists(fullpath):
        os.remove(fullpath)
    return filepath
    
class Article(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')
    content_type = models.CharField(max_length=20, blank=True)
    content_file = models.FileField(upload_to=process_content_file, max_length=255,blank=True)
    
    def __unicode__(self):
        return self.title

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=15) <= self.pub_date < now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
    def save(self, *args, **kwargs):
        super(Article, self).save(*args, **kwargs)
        cf = str(self.content_file)
        ext = cf.split('.')[-1]
        if ext == 'pdf':
            filename = os.path.join(settings.MEDIA_ROOT, cf)
            to = filename.replace(".pdf", "")
            file_in = PdfFileReader(filename)
            num = file_in.getNumPages()
            for i in range(num):
                with Image(filename=filename + "[%d]"%i, resolution=144) as img:
                    img.save(filename=to + "[%d]"%i + ".jpg")