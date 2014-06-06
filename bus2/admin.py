__author__ = 'gou'
# -*-coding:utf-8-*-
from django.contrib import admin
from bus2.models import *
'''
class PositionModelAdmin(admin.ModelAdmin):
    using = 'other'

    def save_model(self,request,obj,form,change):
        obj.save(using = self.using)
    def delete_model(self,request,obj):
        obj.delete(using = self.using)
    def queryset(self,request):
        return super(MultiDBModelAdmin,self).queryset(request).using(self.using)
    def formfield_for_foreignkey(self,db_field,request=None,**kwargs):
        return super(MultiDBModelAdmin,self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)
    def formfield_for_manytomany(self,db_field,request=None,**kwargs):
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class BusModelAdmin(admin.ModelAdmin):
    using = 'other'

    def save_model(self,request,obj,form,change):
        obj.save(using = self.using)
    def delete_model(self,request,obj):
        obj.delete(using = self.using)
    def queryset(self,request):
        return super(MultiDBModelAdmin,self).queryset(request).using(self.using)
    def formfield_for_foreignkey(self,db_field,request=None,**kwargs):
        return super(MultiDBModelAdmin,self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)
    def formfield_for_manytomany(self,db_field,request=None,**kwargs):
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)

class NowPositionModelAdmin(admin.ModelAdmin):
    using = 'other'

    def save_model(self,request,obj,form,change):
        obj.save(using = self.using)
    def delete_model(self,request,obj):
        obj.delete(using = self.using)
    def queryset(self,request):
        return super(MultiDBModelAdmin,self).queryset(request).using(self.using)
    def formfield_for_foreignkey(self,db_field,request=None,**kwargs):
        return super(MultiDBModelAdmin,self).formfield_for_foreignkey(db_field, request=request, using=self.using, **kwargs)
    def formfield_for_manytomany(self,db_field,request=None,**kwargs):
        return super(MultiDBModelAdmin, self).formfield_for_manytomany(db_field, request=request, using=self.using, **kwargs)
'''
admin.site.register(Position)
admin.site.register(Bus)
admin.site.register(NowPosition)
