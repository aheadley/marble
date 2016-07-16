#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os.path
import fnmatch

from nbt.region import RegionFile

from ..util import Range1D, Range2D

class Dimension(object):
    PRIMARY_REGIONSET_NAME  = u''
    REGION_FILENAME         = u'r.{x}.{z}.mca'
    REGION_SUBDIR           = u'region'
    DATA_SUBDIR             = u'data'

    @classmethod
    def load(cls, name, vfs):
        return cls(name, vfs)

    @classmethod
    def load_from_db(cls, db, dim_data):
        pass

    def __init__(self, name, vfs):
        self._bounds = None
        self._vfs = vfs
        self._name = name

    @property
    def name(self):
        return self._name

    @property
    def dim_id(self):
        if self.name.startswith('DIM'):
            dim_id = self.name.replace('DIM', '')
            try:
                dim_id = int(dim_id)
                return dim_id
            except ValueError as err:
                pass
        return None

    @property
    def is_empty(self):
        return len(self.get_region_paths()) > 0

    @property
    def bounds(self):
        if self._bounds is None:
            self._bounds = self._find_bounds()
        return self._bounds

    def get_region_path(self, x, z):
        return os.path.join(self.REGION_SUBDIR,
            self.REGION_FILENAME.format(x=x, z=z))

    def get_region(self, x, z):
        region_handle = self._vfs.open(
            self.get_region_path(x, z), 'rb')
        return RegionFile(fileobj=region_handle)

    def get_region_paths(self):
        return fnmatch.filter(
            self._vfs.ilistdir(self.REGION_SUBDIR, files_only=True, full=True),
            os.path.join(self.REGION_SUBDIR, self.REGION_FILENAME.format(x='*', z='*'))
        )

    def iter_regions(self):
        for region_fn in self.get_region_paths():
            print region_fn
            yield RegionFile(fileobj=self._vfs.open(region_fn, 'rb'))
    __iter__ = iter_regions

    def _find_bounds(self):
        region_coords = [(int(c[1]), int(c[2])) \
            for c in (os.path.basename(f).split('.') \
                for f in self.get_region_paths())]

        bounds = Range2D(
            x=Range1D(
                min=min(c[0] for c in region_coords),
                max=max(c[0] for c in region_coords),
            ),
            z=Range1D(
                min=min(c[1] for c in region_coords),
                max=max(c[1] for c in region_coords),
            ),
        )

        return bounds
