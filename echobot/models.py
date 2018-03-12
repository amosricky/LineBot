from django.db import models

# Create your models here.
class user(models.Model):
    userID = models.CharField(max_length=100)
    TimeStamp = models.CharField(max_length=100)

    def __unicode__(self):
        return self.userID

class goods(models.Model):
    goodsID = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    webLink = models.CharField(max_length=100)
    timestamp = models.CharField(max_length=100)

    def __unicode__(self):
        return self.goodsID

class image(models.Model):
    goodsID = models.CharField(max_length=100)
    imageLink = models.CharField(max_length=100)

    def __unicode__(self):
        return self.imageLink

class goods_condition(models.Model):
    goodstitle = models.CharField(max_length=100)
    price = models.IntegerField()

    def __unicode__(self):
        return self.goodstitle