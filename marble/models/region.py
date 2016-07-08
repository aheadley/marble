#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from nbt.region import RegionFile

class AnvilRegion(object):
    @classmethod
    def load(cls, fd):
        pass

    def __init__(self):
        pass



class MinecraftChunk(object):
    @classmethod
    def load(cls, chunk_data):
        pass

    @classmethod
    def load_from_region(cls, x, z, region):
        pass

    def __init__(self):
        pass
