#!/usr/bin/env python

"""CipherSaber, http://ciphersaber.gurus.com.

Copyright (c) 1999-2000 Ng Pheng Siong. All rights reserved."""

RCS_id='$Id: CipherSaber.py,v 1.2 2000/11/26 09:25:40 ngps Exp $'

from M2Crypto import RC4, Rand
import getopt, getpass, sys

class argerr(Exception): pass

cmd = -1
inf = sys.stdin
outf = sys.stdout

optlist, optarg = getopt.getopt(sys.argv[1:], 'dei:o:')
for opt in optlist:
    if '-d' in opt:
        cmd = cmd + 1
    elif '-e' in opt:
        cmd = cmd + 2
    elif '-i' in opt:
        i = opt[1]
        if i == '-':
            inf = sys.stdin
        else:
            inf = open(i, 'rb')
    elif '-o' in opt:
        o = opt[1]
        if o == '-':
            outf = sys.stdout
        else:
            outf = open(o, 'wb')
if cmd < 0:
    raise argerr, "either -d or -e"
if cmd > 1:
    raise argerr, "either -d or -e, not both"

if cmd == 0:
    iv = inf.read(10)
    pp = getpass.getpass('Enter decryption passphrase: ')
else:
    iv = Rand.rand_bytes(10)
    outf.write(iv)
    pp = getpass.getpass('Enter encryption passphrase: ')
    pp2 = getpass.getpass('Enter passphrase again: ')
    if pp != pp2:
        raise SystemExit, 'passphrase mismatch, I\'m outta here...'

ci = RC4.RC4(pp + iv)
del pp, iv

while 1:
    buf = inf.read()
    if not buf: 
        break
    outf.write(ci.update(buf))
outf.write(ci.final())


