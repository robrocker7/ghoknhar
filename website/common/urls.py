from django.conf.urls import patterns, url, include
from website.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT


urlpatterns = patterns('website.common.views',
    url(r'^login/$', 'login_view', name='login'),
    url(r'^logout/$', 'logout_view', name='logout'),
    url(r'^views/(?P<path>.*)\.html$', 'angular_template',
        name='angular_template'),
    url(r'^$', 'home', name='home'),
)


if DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': STATIC_ROOT}),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': MEDIA_ROOT}),
)
