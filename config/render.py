# -*- coding: UTF-8 -*-


renderers = [
    dict(id="txt",    title="Textnet",    ext=['md', 'mdown', 'txt',]),
    dict(id="attach", title="Attachment", ext=['attach']),
]
renderer_fallback  = 'attach'

inlines = [
    dict(id="image",    ext=['jpg', 'jpeg', 'png', 'gif',]),
    dict(id="download", ext=['download']),
]
inline_fallback = "download"
