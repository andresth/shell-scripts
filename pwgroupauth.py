#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Like pwauth but also checks group membership.

Requires python-pam
    sudo pip3 install python-pam
"""

import argparse
import grp
import sys

import pam


def pwgroupauth(username, password, group):
    """Authenticate user."""
    try:
        if username not in grp.getgrnam(group)[3]:
            return False
    except KeyError:
        return False

    if pam.pam().authenticate(username, password):
        return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='pwauth with groups')
    parser.add_argument('group')
    args = parser.parse_args()
    user = sys.stdin.readline().strip()
    passwd = sys.stdin.readline().strip()

    if pwgroupauth(user, passwd, args.group):
        exit(0)
    exit(1)
