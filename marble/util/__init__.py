#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger(__name__)

nbt_to_native = lambda compound_tag: \
    {tag_name: compound_tag[tag_name].value for tag_name in compound_tag}

# def nbt_to_native(root_tag):

