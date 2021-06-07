#!/usr/bin/env python3
# coding: utf8
# 窓を使う。ボーダーと内部の２つ窓をつくることで重複をふせぐ。
import curses
class BorderWindow:
    def __init__(self,stdscr,x=-1,y=-1,w=-1,h=-1):
        self.__initialize()
        self.__screen = stdscr
        x = 2; y = 5; w = 80; h = 10;
        if x < 0: x = 0
        if y < 0: y = 0
        if w < 0: w = curses.COLS
        if h < 0: h = curses.LINES
        self.__outer, self.__inner = self.__make_window_border(x,y,w,h)
        self.__draw()
        self.__finalize()
    @property
    def Inner(self): return self.__inner
    @property
    def Outer(self): return self.__outer
    def __initialize(self):
        if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
        if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
        curses.use_default_colors()
        for i in range(1, curses.COLORS):
            curses.init_pair(i, i-1, -1)
        curses.init_pair(1, 0, 15) #  curses.COLOR_BLACK, curses.COLOR_WHITE
    def __finalize(self):
        curses.doupdate()
        self.__screen.refresh()
        self.__screen.getkey()

    def __make_window_border(self,x,y,w,h):
        outer = self.__make_window(x,y,w,h)
        outer.border(0)
        return (outer, self.__make_window(x+1,y+1,w-2,h-2))
    def __make_window(self,x,y,w,h):
        if curses.LINES < y: raise Exception(f'引数yは{curses.LINES}以下にしてください。')
        if curses.COLS < x: raise Exception(f'引数xは{curses.COLS}以下にしてください。')
        if w < 1: raise Exception(f'引数wは1以上にしてください。')
        if h < 1: raise Exception(f'引数hは1以上にしてください。')
        return self.__screen.subwin(h, w, y, x)
    def __draw(self):
        try:
            for i in range(1, curses.COLORS):
                self.__inner.addstr(str(i).rjust(3), curses.A_REVERSE | curses.color_pair(i))
        except curses.error: pass
        if self.__inner.is_wintouched(): self.__inner.refresh()

