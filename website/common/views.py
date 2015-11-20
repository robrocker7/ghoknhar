from django.shortcuts import render


def home(request):
    return render(request, 'new_base.html', {})


def angular_view_loader(request, template_name):
    """ Return HTML for Angular View. """
    return render(request, 'angular/{0}.html'.format(template_name), {})
