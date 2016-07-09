#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import collections

nbt_to_native = lambda compound_tag: \
    {tag_name: compound_tag[tag_name].value for tag_name in compound_tag}

Range1D = collections.namedtuple('Range1D', ['min', 'max'])
Range2D = collections.namedtuple('Range2D', ['x', 'z'])

Point2D = collections.namedtuple('Point2D', ['x', 'z'])
Point3D = collections.namedtuple('Point3D', ['x', 'z', 'y'])
