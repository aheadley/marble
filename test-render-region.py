#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import os.path

from fs.opener import fsopendir
from marble.models.world import MinecraftWorld
from PIL import Image
import numpy


BLOCK_DATA_AXIS_X = 2
BLOCK_DATA_AXIS_Z = 1
BLOCK_DATA_AXIS_Y = 0

w = MinecraftWorld.load(fsopendir(sys.argv[1]))
dest = sys.argv[2]

print w.name, w.spawn, w.seed

for rs in w.iter_regionsets():
    print rs.name
    print rs.dim_id
    print rs.bounds

    for r in rs.iter_regions():
        img = Image.new('L', (512, 512))
        pixels = img.load()
        img_dest = os.path.join(dest, os.path.basename(r.filename) + '.png')

        for chunk in r.get_metadata():
            chunk_data = r.get_nbt(chunk.x, chunk.z)
            chunk_blocks = None
            for chunk_section in chunk_data['Level']['Sections']:
                # print chunk_section['Y']
                section_blocks = numpy.frombuffer(chunk_section['Blocks'].value,
                    dtype=numpy.uint8)
                section_blocks = section_blocks.astype(numpy.uint16).reshape((16, 16, 16))
                try:
                    add = numpy.frombuffer(chunk_section['Add'].value,
                        dtype=numpy.uint8)
                    add = add.astype(numpy.uint16).reshape((16, 16, 8))

                    add_exp = numpy.empty((16, 16, 16), dtype=numpy.uint16)
                    add_exp[:,:,::2] = (add & 0x0F) << 8
                    add_exp[:,:,1::2] = (add & 0xF0) << 4

                    section_blocks += add_exp
                except Exception as err:
                    # print err
                    pass
                if chunk_blocks is None:
                    chunk_blocks = section_blocks
                else:
                    chunk_blocks = numpy.append(chunk_blocks, section_blocks,
                            axis=BLOCK_DATA_AXIS_Y) \
                        .reshape((chunk_blocks.shape[BLOCK_DATA_AXIS_Y] + \
                                section_blocks.shape[BLOCK_DATA_AXIS_Y], 16, 16))

            for x in range(chunk_blocks.shape[BLOCK_DATA_AXIS_X]):
                for z in range(chunk_blocks.shape[BLOCK_DATA_AXIS_Z]):
                    pixels[(chunk.x * 16) + x, (chunk.z * 16) + z] = \
                        abs(numpy.where(chunk_blocks[:,z,x] != 0)[0][-1] - 60) * 2

        with open(img_dest, 'wb') as fd:
            img.save(fd)
        print 'wrote: %s' % img_dest
