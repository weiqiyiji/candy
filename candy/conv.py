#!/usr/bin/env python
# coding=utf-8

import mmap
import os
import struct
import sys
import traceback


from candy.utils import (read_block,
                         read_int16,
                         read_string,
                         SafeFileWriter)


class DictItem(object):
    def __init__(self, spelling_list, hanzi, frequency):
        self.spelling_list = spelling_list
        self.hanzi = hanzi
        self.frequency = frequency

    def __str__(self):
        return (u'%s\t%s\t%d' % (self.hanzi,
                                 ' '.join(self.spelling_list),
                                 self.frequency)).encode('utf8')


class SougouDict(object):

    _NAME_OFFSET = 0x130
    _CATEGORY_OFFSET = 0x338
    _DESCRIPTION_OFFSET = 0x540
    _SAMPLE_OFFSET = 0xd40
    _DICT_OFFSET = 0x1540
    _HANZI_OFFSET =0x2628

    def __init__(self, scel_file):
        self._scel_file = scel_file
        self.items = []
        self.valid = True
        self.name = os.path.basename(scel_file)
        self.category = None
        self.description = None
        self.sample = None

    def parse(self):
        if os.path.getsize(self._scel_file) == 0:
            self.valid = False
            return
        f = open(self._scel_file, 'rb')
        fp = mmap.mmap(f.fileno(), 0)

        if not self._verify(fp):
            self.valid = False
            return
        self.name = read_string(fp, self._NAME_OFFSET)
        self.category = read_string(fp, self._CATEGORY_OFFSET)
        self.description = read_string(fp, self._DESCRIPTION_OFFSET)
        self.sample = read_string(fp, self._SAMPLE_OFFSET)

        if read_block(fp, self._DICT_OFFSET, 4) != '\x9d\x01\x00\x00':
            self.valid = False
            return
        spellings = self._read_spellings(fp, self._DICT_OFFSET + 4)
        self._read_items(fp, self._HANZI_OFFSET, spellings)
        f.close()

    def _read_spellings(self, fp, read_offset):
        spellings = []
        while True:
            mark, count = read_int16(fp, read_offset, 2)
            read_offset += 4
            spelling = read_string(fp, read_offset, count)
            spellings.append((mark, spelling))
            if spelling == 'zuo':  # The last pinyin
                break
            read_offset += count
        return spellings

    def _read_items(self, fp, read_offset, spellings):
        while read_offset < fp.size():
            spelling_list = []
            next_offset, count = read_int16(fp, read_offset, 2)
            next_offset -= 1
            read_offset += 4
            marks = read_int16(fp, read_offset, count / 2)
            read_offset += count
            for mark in marks:
                for m, spelling in spellings:
                    if mark == m:
                        spelling_list.append(spelling)
                        break
            hanzi_len = read_int16(fp, read_offset, 1)[0]
            read_offset += 2
            hanzi = read_string(fp, read_offset, hanzi_len)
            self.items.append(DictItem(spelling_list, hanzi, 1))
            read_offset += hanzi_len + 12 + next_offset * (hanzi_len + 14)

    def _verify(self, fp):
        return read_block(fp, 0, 8) == '\x40\x15\x00\x00\x44\x43\x53\x01'


def sougou_main():
    if len(sys.argv) != 3:
        print 'Usage: %s sougou_dict_dir output_dir' % sys.argv[0]
        sys.exit(1)
    sougou_dict_dir = unicode(sys.argv[1])
    output_dir = unicode(sys.argv[2])
    if not os.path.exists(sougou_dict_dir):
        print 'Sougou dict dir not exists'
        sys.exit(1)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for scel_file in os.listdir(sougou_dict_dir):
        try:
            realpath = os.path.join(sougou_dict_dir, scel_file)

            sg_dict = SougouDict(realpath)
            output_path = os.path.join(output_dir, sg_dict.name + '.txt')
            if os.path.exists(output_path):
                print u'%s already processed, skip...' % realpath
                continue
            sg_dict.parse()
            if not sg_dict.valid:
                print >>sys.stderr, u'Cannot parse invalid file %s' % sg_dict.name
                continue
            writer = SafeFileWriter(output_path)
            for item in sg_dict.items:
                writer.writeline(str(item))
            writer.close()
            print u'%s successfully parsed' % sg_dict.name
        except Exception, ex:
            print >>sys.stderr, u'Parse %s failed' % realpath
            traceback.print_exc(file=sys.stderr)
