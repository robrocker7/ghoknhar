from django.conf.urls import patterns, include, url

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

    # playlist pages
    url(r'^games/$', 'apps.common.views.view_wrapper',
        {'template': 'playlists.html', 'context': {} },
        name="playlists"),

    # guild wars 2 pages
    url(r'^games/guild-wars-2/$', 'apps.common.views.view_wrapper',
        {'template': 'guildwars2/index.html', 'context': {} },
        name="gw2-index"),
    url(r'^games/guild-wars-2/char-ranger-gameplay/$', 'apps.common.views.view_wrapper',
        {'template': 'guildwars2/ranger-gameplay.html', 'context': {} },
        name='gw2-ranger'),

    url(r'^faith/', include('apps.faith.urls', namespace='faith')),
    url(r'^live/$', 'apps.common.views.live', name='live'),
    url(r'^$', 'apps.common.views.main', name='index'),
)
