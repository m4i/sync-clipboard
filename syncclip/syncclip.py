#!/usr/bin/env python2

import os
import sys
import win32clipboard

VIM_YANKRING = 'vim-yankring'

def get(args):
    command = ' '.join(['"%s"' % args[0]] + args[1:] + ['-t', VIM_YANKRING])
    stdout = os.popen(command)
    text = stdout.read()

    text = text.decode('utf-8').replace('\n', '\r\n')

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

def put(args):
    win32clipboard.OpenClipboard()
    text = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
    win32clipboard.CloseClipboard()

    text = text.replace('\r\n', '\n').encode('utf-8')

    command = ' '.join(['"%s"' % args[0]] + args[1:] + [VIM_YANKRING])
    stdin, stdout = os.popen2(command)
    stdin.write(text)

if __name__ == '__main__':
    if not (len(sys.argv) >= 4 and
            sys.argv[1] in ('get', 'put') and
            os.path.isfile(sys.argv[2])):
        sys.exit(1)

    if sys.argv[1] == 'get':
        get(sys.argv[2:])
    else:
        put(sys.argv[2:])
