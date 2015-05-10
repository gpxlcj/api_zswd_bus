#! -*- coding:utf-8 -*-
__author__ = 'gpxlcj'

from django.core.serializers import *
import json
from django.http import HttpResponse


#返回json数据
def render_to_json(data):
    data = json.dumps(data)
    content_type = "application/json"
    response = HttpResponse(data, content_type=content_type)
    return response


def return_status(status_code):
    status = {
        'status': status_code
    }
    return status