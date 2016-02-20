# -*- coding: utf-8 -*-
# -*- encoding: utf-8 -*-

from django.shortcuts import render_to_response

def user(request):
    return render_to_response("po2user.html", {})

def userphotos(request):
    return render_to_response("po2userphotos.html", {})

def pageemployee(request):
    return render_to_response("po2pageemployee.html", {})

def help(request):
    return render_to_response("po2help.html", {})

def anketa(request):
    return render_to_response("po2anketa.html", {})

def anketaclear(request):
    return render_to_response("po2anketaclear.html", {})

