# -*- coding: UTF-8 -*-
import config
import pymmd

''' index parameter is used to skip fragments harvested into the one being processed '''

def render_txt(fragment, index):
    html = pymmd.convert(fragment["content"])
    return html, index

def render_image(fragment, index):
    return "<h1>TODO</h1>", index
def render_download(fragment, index):
    return "<h1>TODO</h1>", index

def render_attach(fragment, index):
    inline = None
    if "ext" in fragment["commands_hash"]:
        for i in config.render.inlines:
            if fragment["commands_hash"]["ext"]["content"] in i["ext"]:
                inline = i["id"]
                break
    if inline is None or inline not in registered_inlines:
        inline = config.render.inline_fallback
    return registered_inlines[inline](fragment, index)

registered_inlines = dict(
    image = render_image,
    download = render_download,
)
registered_renderers = dict(
    txt    = render_txt,
    attach = render_attach,
)

def render_fragments(fragments):
    result, index = [], 0
    while index < len(fragments):
        renderer = None
        for r in config.render.renderers:
            if fragments[index]["commands_hash"]["ext"]["content"] in r["ext"]:
                renderer = r["id"]
                break
        print fragments[index]["commands_hash"]["ext"], renderer
        if renderer is None or renderer not in registered_renderers:
            renderer = config.render.renderer_fallback
        _ = dict(uuid=fragments[index]["uuid"])
        __, index = registered_renderers[renderer](fragments[index], index)
        _["html"] = __
        index+=1
        result+=[_]
    return result
