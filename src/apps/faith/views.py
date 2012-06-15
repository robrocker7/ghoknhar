from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from apps.faith.models import Vote, Bar
from apps.common.decorators import ajax_view
from apps.common.functions import json_response

def vote(request, bar_id):
    try:
        bar = Bar.objects.get(id=bar_id)
    except Bar.DoesNotExist:
        raise Http404

    vote = request.GET.get('is', None)

    if not vote:
        raise Http404

    ip_address = request.META['REMOTE_ADDR']
    if vote == 'faith':
        bar.has_faith(ip_address)
    if vote == 'faithless':
        bar.no_faith(ip_address)

    if request.is_ajax():
        return json_response({'success': True})
    return HttpResponseRedirect(reverse('faith:track'))
    
@ajax_view
def check_votes(request, bar_id):
    try:
        bar = Bar.objects.get(id=bar_id)
    except Bar.DoesNotExist:
        return json_response({'success': False,
            'errors': ['no_bar']})

    # first check to see if a new bar has been created
    new_bar_check = Bar.objects.latest('date_created')
    if bar.id != new_bar_check.id:
        return json_response({'success': False,
            'new_bar': True, 'bar_id': new_bar_check.id})

    return json_response({'success': True,
        'faith_count': bar.faith_count(),
        'no_faith_count': bar.no_faith_count()})

def track(request):
    try:
        bar = Bar.objects.latest('date_created')
    except Bar.DoesNotExist:
        bar = Bar()
        bar.save()

    has_voted = bar.has_voted(request.META['REMOTE_ADDR'])

    return render_to_response('faith/track.html', {
            'has_voted': has_voted,
            'bar': bar,
        }, context_instance=RequestContext(request))

@login_required
def new_bar(request):
    if 'new' in request.GET:
        bar = Bar()
        bar.save()
        return HttpResponseRedirect(reverse('faith:new'))

    return render_to_response('faith/new.html', {},
        context_instance=RequestContext(request))
