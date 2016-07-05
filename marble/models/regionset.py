#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger(__name__)


class RegionSet(object):
    @classmethod
    def load(cls):
        pass

    @classmethod
    def load_from_db(cls, db, dim_data):
        pass

    def __init__(self, dim_name):
        pass

    def iter_chunks(self):
        pass

    def get_chunk(self, x, z):
        pass


