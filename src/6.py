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

def draw(window, items, width):
    try:
        for i, s in enumerate(items):
            window.addstr(i, 0, s.ljust(width), curses.A_REVERSE | curses.color_pair(1))
    except curses.error: pass
    if window.is_wintouched(): window.refresh()

def main(stdscr):
    curses.curs_set(0)
    if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
    if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
    curses.use_default_colors()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i-1, -1)
    curses.init_pair(1, 0, 15) #  curses.COLOR_BLACK, curses.COLOR_WHITE

    items = ['たたかう', 'わざ', 'にげる']
    width = max(len(s) for s in items)
    outer1, inner1 = make_window_border(stdscr, 0, 0, (width*2)+2, len(items)+2)
    draw(inner1, items, width)
    curses.doupdate()
    stdscr.refresh()
    stdscr.getkey()
    curses.endwin()


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(main)

