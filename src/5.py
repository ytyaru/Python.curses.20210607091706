#!/usr/bin/env python3
# coding: utf8
# 窓を使う。ボーダーと内部の２つ窓をつくることで重複をふせぐ。
if __name__ == "__main__":
    import os, curses
    from BorderWindow import BorderWindow
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(BorderWindow)
#    curses.wrapper(BorderWindow(x=2, y=5, w=80, h=10))
    

