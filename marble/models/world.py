#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger(__name__)

import os.path

import nbt
from marble.util import nbt_to_native
from marble.models.regionset import RegionSet

class MinecraftWorld(dict):
    @classmethod
    def load_from_s3(cls, bucket, level_dat_key):
        pass

    @classmethod
    def load_from_db(cls, db, key):
        pass

    @classmethod
    def load_from_nbt(cls, nbt_file):
        if isinstance(nbt_file, basestring):
            with open(nbt_file, 'rb') as nbt_fd:
                level_dat = nbt.NBTFile(fileobj=nbt_fd)
                world_data = nbt_to_native(level_dat['Data'])
        else:
            level_dat = nbt.NBTFile(fileobj=nbt_file)
            world_data = nbt_to_native(level_dat['Data'])

        return cls(world_data)

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
        pass
