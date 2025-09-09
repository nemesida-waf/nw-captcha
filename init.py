#!/usr/bin/env python3

"""
Nemesida WAF CAPTCHA
Copyright (c) 2017-2025 Pentestit LLC - All Rights Reserved
Author: Romanov R.
"""

from multiprocessing import cpu_count
from logger import log

# Socket path
bind = "127.0.0.1:8080"

# Worker options
workers = cpu_count() + 1

# Logging options
loglevel = 'critical'
logconfig = '/var/www/nw-captcha/logging.conf'

# Logging
log.info('START')
