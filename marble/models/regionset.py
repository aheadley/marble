#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger(__name__)

import os.path
import fnmatch

import nbt

class RegionSet(object):
    REGION_FILENAME         = u'r.{x}.{z}.mca'

    @classmethod
    def load(cls, vfs):
        return cls(vfs)

    @classmethod
    def load_from_db(cls, db, dim_data):
        pass

    def __init__(self, vfs):
        self._bounds = None
        self._vfs = vfs

    @property
    def name(self):
        return os.path.basename(self._vfs)

    @property
    def dim_id(self):
        name = self.name
        if name.startswith('DIM'):
            dim_id = name.replace('DIM', '')
            try:
                dim_id = int(dim_id)
                return dim_id
            except ValueError as err:
                pass
        return None

    def get_region(self, x, z):
        fd = self._vfs.open(self.REGION_FILENAME.format(x=x, z=z), 'rb')
        return nbt.RegionFile(fileobj=fd)

    def get_region_paths(self):
        return fnmatch.filter(self._vfs.ilistdir(files_only=True),
            self.REGION_FILENAME.format(x='*', z='*'))

    def iter_regions(self):
        for region_fn in self.get_region_paths():
            yield nbt.RegionFile(fileobj=self._vfs.open(region_fn, 'rb'))
    __iter__ = iter_regions

    @property
    def bounds(self):
        if self._bounds is None:
            self._bounds = self._find_bounds()
        return self._bounds

    def _find_bounds(self):
        region_coords = [(int(c[1]), int(c[2])) \
            for c in (os.path.basename(f).split('.') \
                for f in self.get_region_paths())]

        xmax = max(c[0] for c in region_coords)
        xmin = min(c[0] for c in region_coords)
        zmax = max(c[1] for c in region_coords)
        zmin = min(c[1] for c in region_coords)

        return ((xmin, xmax), (zmin, zmax))
