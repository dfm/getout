#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import os
from getout import create_app
dirname = os.path.dirname(os.path.abspath(__file__))
app = create_app(os.path.join(dirname, "local.py"))
