# coding: u8

import os
import site
import sys

"""Add `handlers`, `vendor/*` directories to Python's site-packages path."""


def setup():
    ROOT = os.path.dirname(os.path.abspath(__file__))
    path = lambda *a: os.path.join(ROOT, *a)

    prev_sys_path = list(sys.path)

    directories = [ROOT, 'handlers', 'vendor']
    for directory in directories:
        site.addsitedir(path(directory))

    '''
    subdirs = ['vendor']
    for subdir in subdirs:
        if os.path.exists(path(subdir)):
            for directory in os.listdir(path(subdir)):
                full_path = path(subdir, directory)
                if os.path.isdir(full_path):
                    site.addsitedir(full_path)
    '''

    # Move the new items to the front of sys.path. (via virtualenv)
    new_sys_path = []
    for item in list(sys.path):
        if item not in prev_sys_path:
            new_sys_path.append(item)
            sys.path.remove(item)
    sys.path[:0] = new_sys_path
