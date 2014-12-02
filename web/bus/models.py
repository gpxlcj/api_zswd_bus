#!-*- coding:utf-8 -*-
from django.db import models
from lib.build_json import render_to_json


RECEIVE_BUS_ID = 'id'
RECEIVE_BUS_LATITUDE = 'latitude'
RECEIVE_BUS_LONGITUDE = 'longitude'



#坐标类
class Coordinate(models.Model):

    longitude = models.FloatField(u'经度')
    latitude = models.FloatField(u'纬度')
    time = models.DateTimeField(u'时间', auto_now=True, blank=True)
    bus_number = models.CharField(u'所属车辆名称', max_length=100, blank=True)
    bus_route = models.CharField(u'所属路线名称', max_length=100, blank=True)
    
    class Meta:
        verbose_name = u'坐标'
        verbose_name_plural = u'坐标类'

    def __unicode__(self):
        return "%d_by_%s"  % (self.id, self.time)

#测试坐标类
class TestCoordinate(models.Model):

    longitude = models.FloatField(verbose_name=u'经度')
    latitude = models.FloatField(verbose_name=u'纬度')
    time = models.DateTimeField(u'时间', auto_now=True, blank=True)

    class Meta:
        verbose_name = u'测试坐标'
        verbose_name_plural = u'测试坐标类'
#特征点坐标类
class SpecialCoordinate(models.Model):

    longitude = models.FloatField(u'经度')
    latitude = models.FloatField(u'纬度')
    route_name = models.CharField(u'所属路线名称', max_length=100, blank=True)

    class Meta:
        verbose_name = u'特征点坐标'
        verbose_name_plural = u'特征点坐标类'

    def __unicode__(self):
        return "%s" % self.route_name

#路线类
class Route(models.Model):

    departure_stop = models.CharField(u'始发站', max_length=30)
    final_stop = models.CharField(u'终点站', max_length=30)
    special_coordinate = models.OneToOneField(SpecialCoordinate, verbose_name=u'线路特征点')

    class Meta:
        verbose_name = u'路线'
        verbose_name_plural = u'路线类'

    def __unicode__(self):
        return "%s-%s" % (self.departure_stop, self.final_stop)
        
#车站类        
class Stop(models.Model):

    
    name = models.CharField(u'名称', max_length=30)
    route = models.ForeignKey(Route, verbose_name=u'路线')
    longitude = models.FloatField(u'经度', default=0)
    latitude = models.FloatField(u'纬度', default=0)
    arrive_time = models.IntegerField(u'从始点到该站的时间', blank=True, default=0)

    class Meta:
        verbose_name = u'站点'
        verbose_name_plural = u'站点类'
    
    def __unicode__(self):
        return "%s" % self.name


#校车类
class Bus(models.Model):
    
    route = models.ForeignKey(Route, verbose_name=u'路线')
    coordinate = models.OneToOneField(Coordinate, verbose_name=u'当前坐标')
    stop = models.ForeignKey(Stop, verbose_name=u'站点')
    number = models.CharField(max_length=100, verbose_name=u'车辆代号')
    class Meta:
        verbose_name = u'校车'
        verbose_name_plural = u'校车类'

    def __unicode__(self):
        return "%s" % self.number

    def update_position(self, request):

        if request.method == 'POST':

            new_coordinate = Coordinate(longitude=request.POST.get(RECEIVE_BUS_LONGITUDE),
                                        latitude=request.POST.get(RECEIVE_BUS_LATITUDE),
                                        bus_number=request.POST.get(RECEIVE_BUS_ID))
            new_coordinate.save()
            self.coordinate = new_coordinate
            self.save()
            ans = 1
        elif request.method == 'GET':

            new_coordinate = Coordinate(longitude=request.GET.get(RECEIVE_BUS_LONGITUDE),
                                        latitude=request.GET.get(RECEIVE_BUS_LATITUDE),
                                        bus_number=request.GET.get(RECEIVE_BUS_ID))
            new_coordinate.save()
            self.coordinate = new_coordinate
            self.save()
            ans = 1
        else:
            ans = 0

        status = {
            'status': ans,
        }
        return render_to_json(status)
