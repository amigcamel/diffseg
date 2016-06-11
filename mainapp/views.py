"""Views."""
import re
import json
from multiprocessing.pool import ThreadPool
from itertools import repeat

import requests
from django.shortcuts import HttpResponse, Http404


def livac(source_text):
    """
    LIVAC segmentator.

    TODO: can't deal with symbols like this: <>
    """
    url = 'http://www.livac.org/seg/livac_seg_index.php?lang=tc'
    data = {
        'action': 'search',
        'lang': 'tc',
        'search': source_text
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    pat = re.compile(r'<textarea.*id="segmentResult".*?>(.*?)</textarea>')
    res = pat.search(resp.text)
    assert res
    words = re.findall('<(.+?)>', res.group(1))
    return ' '.join(words)


def thulac(source_text):
    """THULAC segmentator."""
    url = 'http://localhost:5000/'
    data = {'source_text': source_text}
    resp = requests.post(url, data=data)
    return resp.text


def _segwrap(segmentator, source_text):
    return globals()[segmentator](source_text)


def seg(request):
    """View for seg."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        source_text = data['source_text']
        segmentators = data['segmentators']
        segmentators = [i.lower() for i in segmentators]
        pool = ThreadPool(processes=1)
        res = pool.starmap_async(_segwrap, zip(segmentators, repeat(source_text)))
        vals = res.get()
        return HttpResponse(json.dumps(vals), content_type="application/json")

    return Http404
