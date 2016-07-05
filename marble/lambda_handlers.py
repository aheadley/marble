#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import boto3
import logging

logger = logging.getLogger('marble-func-00')
logger.setLevel(logging.INFO)

import hashlib
import os.path

s3 = boto3.resource('s3')
bucket = s3.Bucket('marble-testing')

CHUNK_SIZE = 4 * 1024

def lambda_handler(event, context):
    key = 'test-world/' + event['Records'][0]['Sns']['Message']
    logger.info('key: %s', key)

    dest = os.path.join('/tmp', os.path.basename(key))
    logger.info('dest: %s', dest)

    bucket.download_file(key, dest)
    logger.info('download complete')

    with open(dest) as fd:
        chunk = fd.read(CHUNK_SIZE)
        h = hashlib.md5(chunk)

        while chunk:
            h.update(chunk)
            chunk = fd.read(CHUNK_SIZE)
    md5sum = h.hexdigest()
    logger.info('hash: %s', md5sum)

    bucket.put_object(Key=key + '.md5sum', Body=md5sum)

    return md5sum


if __name__ == '__main__':
    pass
