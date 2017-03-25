from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from models import *


def home(request):
    return render(request, 'home.html', {})


def admin(request):

    return render(request, 'admin.html', {
        'words': Word.objects.all().order_by('-freq')
    })


# AJAX
def scan_url(request):
    url = request.POST.get('url', None)
    url_text = tools.get_url_text(url)  # only the text, excludes html tags

    if url_text is None:
        return HttpResponseNotFound("Invalid URL: '{0}'".format(url))

    words_list = tools.LanguageParser.parse(url_text)
    for word in words_list:
        Word.add_word(word)
        del word['_word']
        del word['id']

    return JsonResponse({
        'words_list': words_list
    })

