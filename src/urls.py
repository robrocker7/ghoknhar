from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blah.views.home', name='home'),
    # url(r'^blah/', include('blah.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # guild wars 2 pages
    url(r'^guild-wars-2/char-ranger-gameplay/$', 'django.views.generic.simple.direct_to_template',
        {'template': 'guildwars2/ranger-gameplay.html'}),

    url(r'^faith/', include('apps.faith.urls', namespace='faith')),
    url(r'^live/$', 'apps.common.views.live', name='live'),
    url(r'^$', 'apps.common.views.main', name='index'),
)
