#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class TileSet(object):
    @classmethod
    def load(cls, region_set, dest_vfs, render_config):
        return cls(region_set, dest_vfs, render_config)

    def __init__(self, region_set, dest_vfs, render_config):
        pass

    def render_tile(self, x, y):
        pass
