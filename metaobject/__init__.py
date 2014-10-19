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

def parse_commit(repopath):
    from datetime import datetime

    OLDPWD = os.getcwd()
    os.chdir(repopath)
    try:
        import subprocess
        git_cmd = "git log -n1 --decorate 2> /dev/null | tr '(,)' ';;;'"
        commit = str(subprocess.check_output(git_cmd, shell=True))
    except (AttributeError, subprocess.CalledProcessError):
        commit = ''
    os.chdir(OLDPWD)

    commit_magic, commit_token = ('', '')
    if commit.count(' ') > 2:
        commit_magic, commit_token, _ = commit.split(' ', 2)
    version_tag = commit_token if commit_magic == 'commit' else 'UNKNOWN'
    version = 'dev-' + version_tag

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
    except:
        pass

    # look for (Date: ...)
    try:
        date_lines = commit.split('\n')
        date_line = 'UNKNOWN'
        date_str = 'UNKNOWN'
        time_str = 'UNKNOWN'
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

    return date_str, time_str, version, version_tag

__repo_path__ = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))
__title__ = os.path.basename(__repo_path__)
(__date__, __time__, __version__, __version_tag__) = parse_commit(__repo_path__)
__credits__ = u'Copyright \xa9 %s Andrew Robbins, All rights reserved.' % (__date__.split('-')[0])
__homepage_url__ = 'https://github.com/andydude/%s/blob/%s/README.md' % (__title__, __version_tag__)
__download_url__ = 'https://github.com/andydude/%s/archive/%s.zip' % (__title__, __version_tag__)

if __name__ == '__main__':
    print("credits:", __credits__)
    print("datetime:", __date__, __time__)
    print("title:", __title__)
    print("version:", __version__)
    print("version_tag:", __version_tag__)
    print("download_url:", __download_url__)
    print("url:", __homepage_url__)

else:
    from .objects import MetaObject
