#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger(__name__)

import glob
import fnmatch
import os.path

import botocore

class AbstractFilesystem(object):
    @classmethod
    def clone(cls, orig_vfs, new_prefix):
        pass

    def open(self, path, mode='rb'):
        raise NotImplementedError()

    def glob(self, pattern):
        raise NotImplementedError()

    def exists(self, path):
        raise NotImplementedError()

    def getmtime(self, path):
        raise NotImplementedError()

class LocalFilesystem(AbstractFilesystem):
    def __init__(self, prefix):
        chroot_path = os.path.abspath(prefix)
        self._chroot = chroot_path

    def _resolve(self, path):
        return os.path.join(self._chroot, path)

    def open(self, path, mode='rb'):
        return open(self._resolve(path), mode)

    def glob(self, pattern):
        return glob.iglob(self._resolve(pattern))

    def exists(self, path):
        return os.path.exists(self._resolve(path))

    def getmtime(self, path):
        return os.path.getmtime(self._resolve(path))

class S3Filesystem(AbstractFilesystem):
    def __init__(self, bucket_name, prefix=''):
        s3 = boto3.client('s3')
        self._bucket = s3.Bucket(bucket_name)
        self._prefix = prefix

    def _resolve(self, path):
        return os.path.join(prefix, path)

    def _path_to_obj(self, path):
        return self._bucket.Object(self._bucket.name, path)

    def open(self, path, mode='rb'):
        obj = self._path_to_obj(self._resolve(path))
        resp = obj.get()
        return resp['Body']

    def glob(self, pattern):
        return fnmatch.filter(
            (obj.key for obj in self._bucket.objects.filter(Prefix=self._prefix)),
            pattern)

    def exists(self, path):
        obj = self._path_to_obj(self._resolve(path))
        try:
            obj.load()
        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == '404':
                return False
            else:
                raise err
        else:
            return True

    def getmtime(self, path):
        return self._path_to_obj(self._resolve(path)).last_modified

