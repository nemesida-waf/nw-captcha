#!/usr/bin/env python3

"""
Nemesida WAF CAPTCHA
Copyright (c) 2017-2025 Pentestit LLC - All Rights Reserved
Author: Romanov R.
"""

import json

from fastapi import FastAPI, Request, Form, status
from fastapi.responses import Response, HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from core import captcha_img_gen
from core import mclient
from core import memc_prefix
from core import request_preprocessing
from core import unblock_ip

from init import db

from logger import log

##

app = FastAPI(redirect_slashes=False, ocs_url=None, redoc_url=None, openapi_url=None)
templates = Jinja2Templates(directory='templates')

##

@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    try:

        # request preprocessing
        r = request_preprocessing(request)
            
        # response
        if r:
            return templates.TemplateResponse('index.html', {'request': request, 'sid': r[0], 'args': r[1]})
        else:
            return Response(status_code=400)
    
    except Exception as e:
        log.error('An error occurred in /: {}'.format(e))


@app.get('/captcha')
async def main(request: Request):
    try:
        sid = str(request.query_params.get('sid'))
        r = captcha_img_gen(sid)
        return Response(status_code=400) if r is None else StreamingResponse(r, media_type='image/png', status_code=200)
    except Exception as e:
        log.error('An error occurred in /captcha: {}'.format(e))


@app.post('/verify', response_class=HTMLResponse)
async def main(request: Request, sid: str = Form(...), answer: str = Form(...)):

    try:

        # receive data from the memcached
        memout = mclient.get(memc_prefix + sid)
        if not memout:

            # request preprocessing
            r = request_preprocessing(request)

            # response
            if r:
                return templates.TemplateResponse('index.html', {'request': request, 'sid': r[0], 'args': r[1], 'status': 0})
            else:
                return Response(status_code=400)
            
        # success validation
        if str(answer) == str(json.loads(memout).get('answer')):
            tdata = json.loads(memout).get('data', {})
            url = unblock_ip(db, tdata)
            return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER) if url else Response(content='', status_code=502)

        # fail validation
        else:
            
            # request preprocessing
            r = request_preprocessing(request)

            # response
            if r:
                return templates.TemplateResponse('index.html', {'request': request, 'sid': r[0], 'args': r[1], 'status': 1})
            else:
                return Response(status_code=400)

    except Exception as e:
        log.error('An error occurred in /verify: {}'.format(e))
