from django.conf.urls import url, include
# from agentcms.settings import DEBUG, STATIC_ROOT, MEDIA_ROOT
# from rest_framework.urlpatterns import format_suffix_patterns

from . import views
urlpatterns = [
    url(r'^$', views.home, name='home'),
]

# urlpatterns += format_suffix_patterns(restpatterns)

# if DEBUG:
#     urlpatterns += patterns('',
#         (r'^static/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': STATIC_ROOT}),
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve',
#         {'document_root': MEDIA_ROOT}),
# )
