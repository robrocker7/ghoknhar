from functools import wraps

from django.http import Http404

def ajax_view(view_func):
    def _decorator(request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        return view_func(request, *args, **kwargs)
    return wraps(view_func)(_decorator)
