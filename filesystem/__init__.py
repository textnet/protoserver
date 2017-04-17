# -*- coding: UTF-8 -*-
import re
import os

import config


'''
This module operates like ‘textnet’ filesystem:
- finds files by set of tags
- gets data from known ‘root’ nodes

NO CACHE YET

'''

def simplify_name(name):
    return re.sub(r'\W+', ' ',name).lower().strip()

def find(query):
    tags = [x for x in [simplify_name(x) for x in query.split("#")] if len(x) > 0]
    print config.filesystem.source
    for dirName, subdirList, fileList in os.walk(config.filesystem.source):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            print('\t%s' % fname)
