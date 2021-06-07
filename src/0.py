#!/usr/bin/env python3
# coding: utf8
import os, curses
def main(stdscr):
    if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
    if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
    curses.use_default_colors()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i-1, -1)
    curses.init_pair(1, 0, 15) #  curses.COLOR_BLACK, curses.COLOR_WHITE
    try:
        for i in range(1, curses.COLORS):
            stdscr.addstr(str(i).rjust(3), curses.A_REVERSE | curses.color_pair(i))
    except curses.ERR: pass
    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(main)

