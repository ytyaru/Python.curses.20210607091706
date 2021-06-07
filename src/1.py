#!/usr/bin/env python3
# coding: utf8
# 色をセットする。
import os, curses
def main(stdscr):
    if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
    if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
    curses.use_default_colors()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i-1, -1)
    curses.init_pair(1, 0, 15) #  curses.COLOR_BLACK, curses.COLOR_WHITE

    def make_window(x,y,w,h):
        if curses.LINES < y: raise Exception(f'引数yは{curses.LINES}以下にしてください。')
        if curses.COLS < x: raise Exception(f'引数xは{curses.COLS}以下にしてください。')
        if w < 1: raise Exception(f'引数wは1以上にしてください。')
        if h < 1: raise Exception(f'引数hは1以上にしてください。')
        return stdscr.subwin(h, w, y, x)
#        return curses.newwin(y, x, h, w)
    window1 = make_window(2, 5, 80, 10)
    stdscr.noutrefresh()
    window1.noutrefresh()
    window1.erase()
    try:
        for i in range(1, curses.COLORS):
            window1.addstr(str(i).rjust(3), curses.A_REVERSE | curses.color_pair(i))
    except curses.ERR: pass
    if window1.is_wintouched(): window1.refresh()
    curses.doupdate()
    stdscr.getkey()
    curses.endwin()


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(main)

