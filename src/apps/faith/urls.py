from django.conf.urls import patterns, include, url

urlpatterns = patterns('apps.faith.views',
    url(r'^new/$', 'new_bar', name='new'),

    url(r'^instance/(?P<bar_id>\d+)/$', 'check_votes', name='check_votes'),
    url(r'^instance/(?P<bar_id>\d+)/vote/$', 'vote', name='vote'),
)
