# -*- coding: UTF-8 -*-
import re
import os
import base64
import uuid
from pprint import pprint

import config

COMMAND = '~'

'''
This module operates like ‘textnet’ filesystem:
- finds files by set of tags
- gets data from known ‘root’ nodes

NO CACHE YET

Quite naive and messed up implementation.
Fragments will probably become classes

'''

# universal simplifier: lowercase, remove non-word characters
def simplify_name(name):
    return re.sub(r'\W+', ' ',name, flags=re.UNICODE).lower().strip()

# These encoders convert everything to textnet-compatible raw format
def encoder_txt(abs_path):
    with open(abs_path, 'r') as f:
        content = f.read().decode('UTF-8')
    lines = content.split("\n") + ["----------"]
    fragments = []
    fragment = []
    for l in lines:
        if re.match(r'^-{5,}\s*$', l):
            fragments += ["\n".join(fragment)]
            fragment = []
        else:
            fragment += [l]
    fragments = [x for x in fragments if not re.match(r'^\s*$', x)]
    return fragments

def encoder_attach(abs_path):
    with open(abs_path, 'rb') as f:
        content = f.read()
    return ["\n".join([
        '~decode: attach',
        base64.urlsafe_b64encode(content)
    ])]

def encoder_skip(abs_path):
    return []

registered_encoders = dict(
    txt    = encoder_txt,
    attach = encoder_attach,
    skip   = encoder_skip,
)

def get_raw_fragments(abs_path):
    # prepare encoders
    encoders = dict()
    for e in config.filesystem.encoders:
        for ext in e["ext"]:
            encoders["."+ext] = e
    encoders_default  = "."+config.filesystem.encoders_default
    encoders_fallback = "."+config.filesystem.encoders_fallback
    # find encoder
    path, ext = os.path.splitext(abs_path)
    if ext == "": ext = encoders_default
    if ext not in encoders: ext = encoders_fallback
    encoder = registered_encoders[ encoders[ext]["id"] ]
    return encoder(abs_path)

def get_command(line):
    if len(line) == 0 or line[0] != COMMAND:
        return None
    else:
        parts = line.split(":")
        if len(parts) == 1:
            return dict(command=simplify_name(parts[0]))
        else:
            return dict(command=simplify_name(parts[0]), content=":".join(parts[1:]))

def get_tags(tags_commands):
    tags = []
    for command in tags_commands:
        tags += [x for x in [simplify_name(t) for t in command["content"].split('#')] if len(x) > 0]
    return tags

def get_fragment_structure(fragment_content):
    fragment = dict(content=fragment_content, uuid=uuid.uuid4())
    # find commands
    fragment["commands"] = []
    lines = fragment_content.split("\n")
    for line in lines:
        command = get_command(line)
        if command: fragment["commands"] = fragment["commands"]+[command]
    # extract tags
    fragment["tags"] = get_tags([command for command in fragment["commands"] if command["command"] == "tags"])
    return fragment


def build_sources(abs_paths):
    fragments_by_tag  = dict()
    fragments_by_uuid = dict()
    publishing = dict()
    for abs_path in abs_paths:
        for dirName, subdirList, fileList in os.walk(os.path.dirname(abs_path)):
            for fname in fileList:
                fname = fname.decode("UTF-8")
                fragment_count = 0
                # remove all ignored
                okay = True
                for r in config.filesystem.ignore:
                    if re.search(r,fname):
                        okay = False
                        break
                if okay:
                    # get filename tags
                    fname_trimmed = re.sub(r'\..*?$', '', fname)
                    tags = [simplify_name(x) for x in (fname, fname_trimmed)]
                    # get fragments
                    fragments = [get_fragment_structure(f) for f in get_raw_fragments(os.path.join(dirName, fname))]
                    for fragment in fragments:
                        fragment_count   += 1
                        fragment["tags"] += [str(fragment_count).encode("UTF-8")]
                        fragment["tags"] += tags
                        fragments_by_uuid[fragment["uuid"]] = fragment
                        for tag in fragment["tags"]:
                            if tag not in fragments_by_tag: fragments_by_tag[tag] = []
                            fragments_by_tag[tag] += [fragment]
                    # get publish command
                    for fragment in fragments:
                        for command in fragment["commands"]:
                            if command["command"] == "publish":
                                command["publish_path"] = "/".join([simplify_name(x) for x in command["content"].split("/")])
                                if command["publish_path"] not in publishing:
                                    publishing[command["publish_path"]] = []
                                publishing[command["publish_path"]] += [dirName]
    return dict(by_tag=fragments_by_tag, by_uuid=fragments_by_uuid, publishing=publishing)

def lookup_paths(publish_path, abs_paths):
    sources = build_sources(abs_paths)
    publish_path = "/".join([simplify_name(x) for x in publish_path.split("/")])
    print publish_path
    if publish_path in sources["publishing"]:
        return sources["publishing"][publish_path]

def find(publish_path, tags, abs_paths):
    return filter(tags, lookup_paths(publish_path, abs_paths))

def filter(tags, abs_paths):
    sources = build_sources(abs_paths)
    uuids = []
    first = True
    for tag in tags:
        tag = simplify_name(tag)
        # it is enough to meet a non-existing tag
        if tag not in sources["by_tag"]:
            return []
        # first time just add everything
        if first:
            uuids = [f["uuid"] for f in sources["by_tag"][tag]]
            first = False
        else:
            uuids = [f["uuid"] for f in sources["by_tag"][tag] if f["uuid"] in uuids]
    return [sources["by_uuid"][x] for x in uuids]
