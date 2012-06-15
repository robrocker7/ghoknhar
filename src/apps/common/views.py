from django.template import RequestContext
from django.shortcuts import render_to_response

from apps.faith.models import Bar

def main(request):
    try:
        bar = Bar.objects.latest('date_created')
    except Bar.DoesNotExist:
        bar = Bar()
        bar.save()

    has_voted = bar.has_voted(request.META['REMOTE_ADDR'])

    return render_to_response('index.html', {
            'has_voted': has_voted,
            'bar': bar,
        }, context_instance=RequestContext(request))
