#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import collections

from nbt.nbt import TAG, _TAG_Numeric, TAG_Compound, TAG_String, TAG_Byte_Array

def nbt2py(tag):
    if not isinstance(tag, TAG):
        return tag
    if isinstance(tag, TAG_Compound):
        return {tag_name: nbt2py(tag[tag_name]) for tag_name in tag}
    if isinstance(tag, TAG_Byte_Array):
        return tag.value
    if isinstance(tag, collections.MutableSequence):
        return [nbt2py(t) for t in tag]
    if isinstance(tag, TAG_String):
        return tag.value
    if isinstance(tag, _TAG_Numeric):
        return tag.value

Range1D = collections.namedtuple('Range1D', ['min', 'max'])
Range2D = collections.namedtuple('Range2D', ['x', 'z'])

Point2D = collections.namedtuple('Point2D', ['x', 'z'])
Point3D = collections.namedtuple('Point3D', ['x', 'z', 'y'])
