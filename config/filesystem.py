# -*- coding: UTF-8 -*-

sources = ['~/Dropbox/NY Textnet Container/']
cache   = '~/textnet-cache/'

ignore = [
    r'^\.',
    r'Icon',
]

encoders = [
    dict(id="txt",    title="Textnet",    ext=['md', 'mdown', 'txt',]),
    dict(id="attach", title="Attachment", ext=['attach']),
    dict(id="skip",   title="Skip",       ext=['~']),
]
encoders_default  = 'txt'
encoders_fallback = '~'


# DO NOT USE ~!
from os.path import expanduser

sources = [expanduser(source) for source in sources]
cache  = expanduser(cache)
