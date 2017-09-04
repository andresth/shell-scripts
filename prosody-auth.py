#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
External authentication script for prosody mod_auth_external.

Needs mod_auth_external https://modules.prosody.im/mod_auth_external.html
Needs to be run as root.
    `external_auth_command="sudo /path/to/script"`
Make sure it is write protected
    `chmod 555 /path/to/script`
"""

import crypt
import grp
import re
import spwd
import sys
from subprocess import PIPE, Popen


def isuser(username, domain, password=None):
    """Check if user exists and if he is a member of the group 'domain'."""
    try:
        spwd.getspnam(username)
        return username in grp.getgrnam(domain)[3]
    except KeyError:
        return False
    except PermissionError:
        print('No permission to access /etc/shadow')
        exit(999)
    return False


def auth(username, domain, password=None):
    """Check if user is allowed to login."""
    password = '' if (password == 0) or (password is None) else password
    try:
        storedPassword = spwd.getspnam(username)[1]
        givenPassword = crypt.crypt(password, storedPassword)
        return (username in grp.getgrnam(domain)[3]) \
            and (storedPassword == givenPassword)
    except KeyError:
        return False
    except PermissionError:
        print('No permission to access /etc/shadow')
        exit(999)
    return False


def setpass(username, domain, password=None):
    """Change user password."""
    password = '' if (password == 0) or (password is None) else password
    return False


pattern = r'^(?P<command>.*?):(?P<username>.*?):(?P<domain>.*?)(?::(?P<password>.*?)){0,1}'
methodes = {'isuser': isuser,
            'auth': auth,
            'setpass': setpass}

if __name__ == '__main__':
    while True:
        line = sys.stdin.readline().rstrip('\n')
        match = re.fullmatch(pattern, line, re.IGNORECASE)
        try:
            if methodes[match.group('command')](*(match.groups(0)[1:])):
                print(1)
            else:
                print(0)
        except (KeyError, AttributeError):
            print(0)
    exit(0)
