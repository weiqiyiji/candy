#!/usr/bin/env python
# coding=utf-8

import os
import struct
import shutil
import tempfile


def read_block(fp, offset, length):
    fp.seek(offset, os.SEEK_SET)
    return fp.read(length)

def read_int16(fp, offset, num):
    return struct.unpack('<' + 'H' * num, read_block(fp, offset, num * 2))

def read_string(fp, offset, max_size=64):
    return read_block(fp, offset, max_size).decode('utf16').rstrip('\0')


class SafeFileWriter(object):

    def __init__(self, path):
        self.path = path
        self.tmpfd, self.tmppath = tempfile.mkstemp()

    def write(self, data):
        os.write(self.tmpfd, data)

    def writeline(self, line):
        self.write(line + '\n')

    def writelines(self, lines):
        for line in lines:
            self.writeline(line)

    def close(self):
        os.close(self.tmpfd)
        shutil.move(self.tmppath, self.path)
