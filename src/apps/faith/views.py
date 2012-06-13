from apps.faith.models import Vote, Bar
from apps.common.decorators import ajax_view
from apps.common.functions import json_response

@ajax_view
def vote(request, bar_id):
    try:
        bar = Bar.objects.get(id=bar_id)
    except Bar.DoesNotExist:
        return json_response({'success': False,
            'errors': ['no_bar']})

    vote = request.GET.get('is', None)

    if not vote:
        return json_response({'success': False,
            'errors': ['no_vote']})
    
    ip_address = request.META['REMOTE_ADDR']
    if vote == 'faith':
        bar.has_faith(ip_address)
    if vote == 'faithless':
        bar.no_faith(ip_address)

    return json_response({'success': True})

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
            'new_bar': True})

    return json_response({'success': True,
        'faith_count': bar.faith_count(),
        'no_faith_count': bar.no_faith_count()})
