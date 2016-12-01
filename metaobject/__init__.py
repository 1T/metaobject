#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# metaobject
# Copyright (c) 2014, Andrew Robbins, All rights reserved.
#
# This library ("it") is free software; it is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License ("LGPLv3") <https://www.gnu.org/licenses/lgpl.html>.
'''
metaobject - A Meta-Object protocol library
'''
from __future__ import absolute_import
from __future__ import print_function

import os.path

def legacy_parse_commit(repopath):
    import subprocess
    OLDPWD = os.getcwd()
    os.chdir(repopath)

    git_cmd = "git log -n1 --decorate 2> /dev/null | tr '(,)' ';;;'"

    try:
        commit = subprocess.check_output(git_cmd, shell=True)
    except (AttributeError, subprocess.CalledProcessError):
        commit = ''
    commit_magic, commit_token = ('', '')
    version_tag = 'UNKNOWN'
    try:
        if commit.count(' ') > 2:
            commit_magic, commit_token, _ = commit.split(' ', 2)
            version_tag = commit_token if commit_magic == 'commit' else 'UNKNOWN'
    except:
        pass
    version_num = int(version_tag, 16)
    version = '0.dev' + str(version_num)[-10:]

    # look for (tag: ...)
    try:
        tag_start = commit.find('tag: ')
        if tag_start != -1:
            tag_start += 5
            tag_end = commit.find(';', tag_start)
            if tag_end != -1:
                version_tag = commit[tag_start:tag_end]
                if version_tag.startswith('v'):
                    version = version_tag[1:]
                else:
                    version = version_tag
    except:
        pass

    # look for (Date: ...)
    date_line = 'UNKNOWN'
    date_str = 'UNKNOWN'
    time_str = 'UNKNOWN'
    try:
        date_lines = commit.split('\n')
        for line in date_lines:
            if line.startswith('Date: '):
                date_line = line
        if date_line.startswith('Date: '):
            date_line = date_line.split(':', 1)[1]
            date_line = date_line.split('-', 1)[0] if '-' in date_line else date_line
            date_line = date_line.split('+', 1)[0] if '+' in date_line else date_line
            date_time = datetime.strptime(date_line, ' %a %b %d %H:%M:%S %Y ')
            date_str = date_time.strftime('%F')
            time_str = date_time.strftime('%T')
    except:
        pass

    os.chdir(OLDPWD)
    return date_str, time_str, version, version_tag

def parse_commit(repopath):
    '''
    Returns the version along with other stuff.
    '''
    from datetime import datetime

    # First, try legacy v#.#.#
    version, version_tag = '0', '0'
    try:
        d, t, version, version_tag = legacy_parse_commit(repopath)
        if not version.startswith('dev'):
            return d, t, version, version_tag
    except Exception as err:
        pass

    # Second, try #.#.# using PBR
    #if False:
    #    import pbr.git
    #    version = version_tag = '0.dev0'
    #    changelog = pbr.git._iter_log_oneline('%s/.git' % repopath)
    #    for _, tags, _ in changelog:
    #        if tags:
    #            version = version_tag = pbr.git._get_highest_tag(tags)
    #            break
    #    else:
    #
    #        # Third, try built-in pkg_resources
    #        import pkg_resources
    #        with open(os.path.join(repopath, 'package.json')) as reader:
    #            name = json.loads(reader.read())['name']
    #        dist = pkg_resources.get_distribution(name)
    #        version = version_tag = dist._version

    d, t = datetime.now().isoformat().split('T')
    return d, t, version, version_tag

__repo_path__ = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
(_, _, __version__, __version_tag__) = parse_commit(__repo_path__)

if __name__ == '__main__':
    print("version:", __version__)
    print("version_tag:", __version_tag__)

else:
    from .objects import MetaObject
