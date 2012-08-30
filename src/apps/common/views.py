import re
import feedparser

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.cache import cache

from apps.common.models import Setting
from apps.faith.models import Bar
from apps.games.models import Game

def view_wrapper(request, template, context):

    # get video feed
    videos = cache.get('youtube_feed', None)
    if videos is None:
        video_feed = feedparser.parse('http://gdata.youtube.com/feeds/base/users/ghoknhar/uploads?alt=rss&amp;v=2&amp;orderby=published&amp;client=ytapi-youtube-profile')
        videos = []
        for video in video_feed['items'][:3]:
            vid = {}
            vid['id'] = video['id'].split('/')[-1]
            vid['link'] = video['link']
            vid['title'] = video['title']
            videos.append(vid)
            matches = re.search(r'<span>(.+?)</span>', video['summary'], re.S)
            if matches:
                vid['summary'] = matches.group(1)
        cache.set('youtube_feed', videos, 600)

    context['videos'] = videos

    return render_to_response(template,
        context, context_instance=RequestContext(request))

def main(request):

    try:
        live_setting = Setting.objects.get(name='live')
    except:
        live_setting = False

    # if we're live, do a redirect
    if live_setting and live_setting.value == 'True':
        return HttpResponseRedirect(reverse('live'))

    # get current game
    try:
        current_game_setting = Setting.objects.get(name='fav_game')
        current_game = Game.objects.get(slug=current_game_setting.value)
    except:
        current_game = None

    return view_wrapper(request, 'index.html', {
            'game': current_game,
        })

def live(request):
    try:
        bar = Bar.objects.latest('date_created')
    except Bar.DoesNotExist:
        bar = Bar()
        bar.save()

    has_voted = bar.has_voted(request.META['REMOTE_ADDR'])

    return render_to_response('live.html', {
            'has_voted': has_voted,
            'bar': bar,
        }, context_instance=RequestContext(request))
