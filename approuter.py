#! -*- coding:utf-8 -*-
__author__ = 'gou'
class masterapprouter(object):

    def db_for_read(self, model, **hints):
        return self.__app_router(model)

    def db_for_write(self, model, **hints):
        return self.__app_router(model)

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == obj2._meta.app_lable:
            return True
        return None

    def allow_syncdb(self, db, model):
        return model._meta.app_label == db
    def __app_router(self, model):
        if model._meta.app_label == 'home':
            return 'busdb'
        else:
            return 'default'
