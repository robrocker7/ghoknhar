from django.shortcuts import render

def picture(request):
    return render(request, 'raspi/picture.html', {})