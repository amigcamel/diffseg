import requests
from pyquery import PyQuery as Pq
from django.shortcuts import render


def livac(text):
    url = 'http://www.livac.org/seg/livac_seg_index.php?lang=tc'
    data = {
        'action': 'search',
        'lang': 'tc',
        'search': text
    }
    resp = requests.post(url, data=data)
    return resp
    dom = Pq(resp.raw)
    res = dom('#segmentResult')
    return res
