from django.http import HttpResponse
from django.utils import simplejson

def json_response(x):
    return HttpResponse(simplejson.dumps(x, sort_keys=True, indent=2),
                        content_type='application/json; charset=UTF-8')
