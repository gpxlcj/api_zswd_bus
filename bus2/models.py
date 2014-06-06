# -*-coding:utf-8-*-
from django.db import models

#当前位置坐标类
class NowPosition(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.CharField(max_length = 100)

    class Meta:
        verbose_name = u'当前坐标'
        verbose_name_plural = u'当前坐标类'

    def __unicode__(self):
        return '%s' %self.id

#位置类
class Position(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.CharField(max_length = 100)
    class Meta:
        verbose_name = u"坐标"
        verbose_name_plural = u"坐标类"

    def __unicode__(self):
        return '%s' %self.id

#汽车设备类
class Bus(models.Model):
    bus_id = models.IntegerField(max_length = 100, blank = True)
    bus_name = models.CharField(max_length = 100, blank = True)
    bus_position = models.ManyToManyField(Position, blank = True)
    bus_nowposition = models.ForeignKey(NowPosition)
    bus_type = models.IntegerField(default = 0)
    bus_accuracy = models.FloatField(default = 0)
    bus_speed = models.FloatField(default = 0)
    class Meta:
        verbose_name = u"校车"
        verbose_name_plural = u"校车类"

    def __unicode__(self):
        return '%s' %self.bus_id

