from django import forms
from django.shortcuts import render_to_response
from gmapi import maps
from gmapi.forms.widgets import GoogleMap


class MapForm(forms.Form):
    map = forms.Field(widget=GoogleMap(attrs={'width':510, 'height':510}))


def index(request):
    gmap = maps.Map(opts = {
        'center': maps.LatLng(31.307453, 121.512979),
        'mapTypeId': maps.MapTypeId.ROADMAP,
        'zoom': 14,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    context = {'form': MapForm(initial={'map': gmap})}
    return render_to_response('cloud/index.html', context)
