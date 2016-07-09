#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os.path
import fnmatch

from nbt.nbt import NBTFile
from marble.util import nbt_to_native
from marble.models.regionset import RegionSet

class MinecraftWorld(dict):
    @classmethod
    def load(cls, vfs):
        with vfs.open('level.dat', 'rb') as fd:
            level_dat = NBTFile(fileobj=fd)
            world_data = nbt_to_native(level_dat['Data'])

        return cls(vfs, world_data)

    def __init__(self, vfs, *pargs, **kwargs):
        self._vfs = vfs
        super(MinecraftWorld, self).__init__(*pargs, **kwargs)

    def __setitem__(self, key, value):
        raise NotImplemented()
    def __delitem__(self, key):
        raise NotImplemented()

    @property
    def spawn(self):
        return (self['SpawnX'], self['SpawnZ'], self['SpawnY'])

    @property
    def seed(self):
        return self['RandomSeed']

    @property
    def name(self):
        return self['LevelName']

    def iter_regionsets(self):
        yield self.get_regionset(RegionSet.PRIMARY_REGIONSET_NAME)

        for fs_dir in self._vfs.ilistdir(dirs_only=True):
            try:
                yield self.get_regionset(fs_dir)
            except ValueError:
                continue

    def get_regionset(self, name):
        if self._vfs.isdir(os.path.join(name, RegionSet.REGION_SUBDIR)):
            return RegionSet.load(name, self._vfs.opendir(name))
        else:
            raise ValueError('No regionset found for dimension: %s' % name)
