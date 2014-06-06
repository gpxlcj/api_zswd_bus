from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'busposition.views.home', name='home'),
    # url(r'^busposition/', include('busposition.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('bus2.views',
    url(r'^bus/userreceive/$','userreceive'),
    url(r'^bus/test/$','test'),
)

urlpatterns += patterns('bus2.bus',
    url(r'^bus/buildnewbus/$', 'buildnewbus'),
    url(r'^bus/getposition/?(.)*', 'getbusposition'),
    url(r'^bus/editbus/$', 'editbusname'),

)

urlpatterns += patterns('bus2.views',
    url(r'^shudong/$', 'renren'),

)
