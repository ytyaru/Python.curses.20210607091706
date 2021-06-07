#!/usr/bin/env python3
# coding: utf8
# 窓を使う。ボーダーと内部の２つ窓をつくることで重複をふせぐ。
import os, curses
def make_window_border(stdscr,x,y,w,h):
    outer = make_window(stdscr,x,y,w,h)
    outer.border(0)
    return (outer, make_window(stdscr,x+1,y+1,w-2,h-2))

def make_window(stdscr,x,y,w,h,is_border=False):
    if curses.LINES < y: raise Exception(f'引数yは{curses.LINES}以下にしてください。')
    if curses.COLS < x: raise Exception(f'引数xは{curses.COLS}以下にしてください。')
    if w < 1: raise Exception(f'引数wは1以上にしてください。')
    if h < 1: raise Exception(f'引数hは1以上にしてください。')
    return stdscr.subwin(h, w, y, x)

def draw(window):
    try:
        for i in range(1, curses.COLORS):
            window.addstr(str(i).rjust(3), curses.A_REVERSE | curses.color_pair(i))
    except curses.error: pass
#    except curses.ERR: pass
    if window.is_wintouched(): window.refresh()

def main(stdscr):
    if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
    if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
    curses.use_default_colors()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i-1, -1)
    curses.init_pair(1, 0, 15) #  curses.COLOR_BLACK, curses.COLOR_WHITE
    
    outer1, inner1 = make_window_border(stdscr, 2, 5, 80, 10)
    draw(inner1)
    curses.doupdate()
    stdscr.refresh()
    stdscr.getkey()
    curses.endwin()


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(main)

