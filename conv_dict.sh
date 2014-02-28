#!/bin/bash

if [ $# != 1 ]; then
    echo "Usage:" $0 "sougou_dict_dir"
    exit 1
fi

scel_file_dir=$1
temp_path="/tmp/luna_pinyin.sougou.dict.yaml"
output_path="$HOME/Library/Rime/luna_pinyin.sougou.dict.yaml"

cat <<EOF > $temp_path
# Rime dictionary
# encoding: utf-8

---
name: luna_pinyin.sougou
version: "`date "+%Y-%m-%d"`"
sort: by_weight
use_preset_vocabulary: true
import_tables:
  - luna_pinyin
...

# table begin
EOF

find $scel_file_dir -type "f" -exec cat {} >> $temp_path +;
mv $temp_path $output_path
