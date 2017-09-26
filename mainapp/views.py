"""Views."""
import re
import os
import json
import pdb
from multiprocessing.pool import ThreadPool
from itertools import repeat

import requests
import thulac as thulacSeg
from django.shortcuts import HttpResponse, Http404
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


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
    return words


def thulac(source_text):
    """THULAC segmentator."""
    url = 'http://localhost:5000/'
    data = {'source_text': source_text}
    # resp = requests.post(url, data=data)
    # return resp.text.split(' ')
    thu = thulacSeg.thulac(seg_only=True, model_path="thulac/models/")
    segtxt = [x[0] for x in thu.cut(source_text)]
    return segtxt


def deepseg(source_text):
    """DeepSeg."""
    url = 'http://localhost:8081/deepseg'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    data = {'data': source_text}
    resp = requests.post(url, data=json.dumps(data), headers=headers)
    res = json.loads(resp.text)['result']
    res = re.sub(' +', ' ', res)
    return res.split(' ')


def segcomp(segres_list):
    """
    Compare results of different segmentators.

    :params: segres_list: must be a list
    """
    def _idxer(lst):
        idx = 0
        output = []
        for w in lst:
            nw = []
            for c in w:
                nw.append('__%s__%d__' % (c, idx))
                idx += 1
            output.append(''.join(nw))
        return output

    def _comp(lst, intsec):
        con = []
        pat = re.compile(r'__(.)__\d+__')
        for hw in lst:
            if hw in intsec:
                con.append(''.join(pat.findall(hw)))
            else:
                con.append('<span class="diff">' +
                           ''.join(pat.findall(hw)) + '</span>')
        return ' '.join(con)

    hwl = [_idxer(segres) for segres in segres_list]  # hwl: hash words list
    intsec = set.intersection(*map(set, hwl))
    res = [_comp(hw, intsec) for hw in hwl]
    return res


def _segwrap(segmentator, source_text):
    return globals()[segmentator](source_text)


@ensure_csrf_cookie
def seg(request):
    """View for seg."""
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        source_text = data['source_text']
        source_text = source_text.replace('\n', ' ')  # remove linebreaks
        segmentators = data['segmentators']
        segmentators = [i.lower() for i in segmentators]
        pool = ThreadPool(processes=5)
        res = pool.starmap_async(_segwrap, zip(
            segmentators, repeat(source_text)))
        vals = res.get()
        seg_with_diff = segcomp(vals)
        return HttpResponse(json.dumps(seg_with_diff), content_type="application/json")
    elif request.method == 'GET':
        return HttpResponse('')

    return Http404


@csrf_exempt
def uploader(request):
    """
    Attachment uploadder.

    TODO: remove @csrf_exempt
    """
    for filename, file in request.FILES.items():
        name = request.FILES[filename].name
        path = os.path.join('/tmp', name)
        with open(path, 'wb') as f:
            f.write(file.read())
    return HttpResponse('ok')
