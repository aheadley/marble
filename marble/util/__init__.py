#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger(__name__)

nbt_to_native = lambda compound_tag: \
    {tag.name: tag.value for tag in compound_tag}
