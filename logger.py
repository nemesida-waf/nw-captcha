#!/usr/bin/env python3

"""
Nemesida WAF API
Copyright (c) 2017-2025 Pentestit LLC - All Rights Reserved
Author: Romanov R.
"""

import logging

##
# Log settings
##

logf = '/var/log/nwaf/captcha/api.log'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
file_handler = logging.FileHandler(logf)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)
