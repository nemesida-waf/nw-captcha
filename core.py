#!/usr/bin/env python3

"""
Nemesida WAF CAPTCHA
Copyright (c) 2017-2025 Pentestit LLC - All Rights Reserved
Author: Romanov R.
"""

import io
import json
import numpy as np
import random
import requests
import sys

from base64 import b64decode
from math import sin
from PIL import Image, ImageDraw, ImageFont
from pymemcache.client.base import Client

from logger import log

##

db_fname = 'db.json'
memc_prefix = 'CAPTCHA_'

##

mclient = Client(('127.0.0.1', 11211), connect_timeout=1, no_delay=True)


def captcha_qa_gen():

    num1 = random.randint(1, 10)
    num2 = random.randint(1, 50)
    # operator = random.choice(['+', '-'])
    operator = '+'

    answer = num1 + num2 if operator == '+' else num1 - num2
    question = '{} {} {}'.format(num1, operator, num2)

    return question, str(answer)


def apply_wave_distortion(image, amplitude, wavelength):

    img_array = np.array(image)
    height, width = img_array.shape[:2]
    new_img = Image.new('RGB', (width, height), color='white')
    new_array = np.array(new_img)

    for y in range(height):
        for x in range(width):
            new_x = x + int(amplitude * sin(2 * 3.14 * y / wavelength))
            if 0 <= new_x < width:
                new_array[y, new_x] = img_array[y, x]

    return Image.fromarray(new_array)


def captcha_img_gen(sid):
    try:

        # receive data from the memcached
        memout = mclient.get(memc_prefix + sid)
        if not memout:
            return None

        # drawing the text
        image = Image.new('RGB', (200, 80), color='white')
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default(20)
        text = json.loads(memout).get('question')
        draw.text((40, 40), text, fill='black', font=font)

        # wave distortion
        image = apply_wave_distortion(image, 40, 80)

        # noise
        draw = ImageDraw.Draw(image)
        for _ in range(100):
            x = random.randint(0, 199)
            y = random.randint(0, 79)
            draw.point((x, y), fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

        # convert the image
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)

        # return the image
        return img_byte_arr

    except Exception as e:
        log.error('An error occurred during CAPTCHA generation for SID {}: {}'.format(sid, e))
        return None


def db_load():
    try:

        # read file data
        with open(db_fname, 'r') as f:
            r = json.loads(f.read())

        # db data validation
        if not r:
            log.error('ERROR: file {} is empty'.format(db_fname))
            sys.exit(1)

        # empty values
        for x in r:
            k = [k for k, v in x.items() if not v]
            if k:
                log.error('ERROR: file {} contains empty value(s): {}'.format(db_fname, ', '.join(k)))
                sys.exit(1)

        # default response
        return r

    except Exception as e:
        log.error('An error occurred while processing {}: {}'.format(db_fname, e))

    # empty file
    log.error('ERROR: file {} is missing'.format(db_fname))
    sys.exit(1)


def request_preprocessing(request):
    try:

        # init
        sid = str(id(request))
        query = dict(request.query_params)
        args = '&'.join(k + '=' + v for k, v in query.items())
        tdata = {'schema': '', 'vhost': '', 'url': '', 'uuid': '', 'ip': ''}

        # update target data
        for col in tdata.keys():
            try:

                # backward compatibility
                if col in ['schema'] and (not query.get(col)):
                    tdata[col] = 'https://'
                    continue

                # skip empty
                if not query.get(col):
                    continue

                # decode with '#' in URL
                if (col == 'url') and ('#' in query.get(col)):
                    r = query.get(col).split('#')
                    d = b64decode(r[0]).decode('UTF-8', errors='ignore')
                    tdata[col] = d + '#' + '#'.join(r[:-1])

                # decode other
                else:
                    tdata[col] = b64decode(query.get(col)).decode('UTF-8', errors='ignore')

            except Exception as e:
                log.error('An error occurred while processing {} in request query: {} ({})'.format(col, e, query))

        # combine the url
        tdata['url'] = tdata['schema'] + tdata['vhost'] + tdata['url']

        # delete unused
        for col in ['schema', 'vhost']:
            del tdata[col]

        # captcha generation
        question, answer = captcha_qa_gen()

        # update the sessions
        mclient.set(
            memc_prefix + sid,
            json.dumps({
                'answer': answer,
                'question': question,
                'data': tdata
            }), 60
        )

        # return the data
        return sid, args

    except Exception as e:
        log.error('An error occurred while unblocking IP: {}'.format(e))

    # default response
    return None


def unblock_ip(db, tdata):
    try:

        # init
        url = ''
        token = ''
        tip = tdata.get('ip')
        turl = tdata.get('url')
        tuuid = tdata.get('uuid')

        # extract captcha url/token by uuid
        for item in db:

            # uuid comparing
            if item.get('uuid') == tuuid:

                # url/token
                url = item.get('url')
                token = item.get('token')

                # stop processing
                break

        # captcha token validation
        if not token:
            log.error('CAPTCHA token by UUID ({}) not found: {}'.format(tuuid, tdata))
            return None

        # captcha url validation
        if not url:
            log.error('CAPTCHA URL by UUID ({}) not found'.format(tuuid))
            return None

        # init
        proxies = {}
        s = requests.Session()
        s.trust_env = False
        headers = {'User-Agent': 'Nemesida WAF CAPTCHA', 'x-nwaf-captcha-v4': json.dumps({'token': token, 'delete_banned_ip': tip})}

        # proxy server processing
        try:

            # load the proxy
            try:
                from settings import proxy
            except Exception:
                proxy = ''

            # non-empty proxy processing
            if proxy:
                proxies = {'http': proxy, 'https': proxy}

        except Exception as e:
            log.error('An error occurred while processing proxy server: {}'.format(e))

        # unblock the IP
        result = s.get(
            url,
            proxies=proxies,
            headers=headers,
            verify=True,
            timeout=30
        )

        # success IP unblocking
        if (result.status_code in range(200, 299)) and (json.loads(result.content).get('status') == 'success'):
            return turl

    except Exception as e:
        log.error('An error occurred while unblocking IP: {} ({})'.format(e, tdata))

    # default response
    return None
