#!/usr/bin/env python3
# coding: utf8
# クラス化する。キー待受。ボーダーラインに囲まれた文字列を表示する。
import os, time, string, curses
class Main:
    def __init__(self, screen):
        self.__screen = screen
        self.__initialize()
        self.__main()
        self.__finalize()
    def __main(self):
#        window = CursorListWindow(self.__screen)
        window = ScrollCursorListWindow(self.__screen)
    def __initialize(self):
        curses.curs_set(0)
        if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
        if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
        self.__init_color_pair()
    def __init_color_pair(self):
        curses.use_default_colors()
        for i in range(1, curses.COLORS):
            curses.init_pair(i, i, curses.COLOR_BLACK)
    def __finalize(self):
        pass
    
class BorderWindow:
    @property
    def Inner(self): return self.__inner
    @property
    def Outer(self): return self.__outer
    @property
    def Screen(self): return self.__screen
    def __init__(self,screen,x=-1,y=-1,w=-1,h=-1):
        self.__screen = screen
        if x < 0: x = 0
        if y < 0: y = 0
        if w < 0: w = curses.COLS
        if h < 0: h = curses.LINES
        self.__make_window_border(x,y,w,h)
    def __make_window_border(self,x,y,w,h):
#        self.__outer = curses.newpad(h,w)
        self.__outer = self.__make_window(x,y,w,h)
        self.__outer.border(0)
        self.__inner = self.__make_window(x+1,y+1,w-2,h-2)
#        self.__inner = self.__outer.subpad(h-2,w-2,y+1,x+1)
    def __make_window(self,x,y,w,h):
        if curses.LINES < y: raise Exception(f'引数yは{curses.LINES}以下にしてください。')
        if curses.COLS < x: raise Exception(f'引数xは{curses.COLS}以下にしてください。')
        if w < 1: raise Exception(f'引数wは1以上にしてください。')
        if h < 1: raise Exception(f'引数hは1以上にしてください。')
        return self.__screen.subwin(h, w, y, x)
    def draw(self):
        if self.Screen.is_wintouched(): self.Screen.refresh()

class ListWindow(BorderWindow):
    @property
    def X(self): return self.__x
    @property
    def Y(self): return self.__y
    @property
    def W(self): return self.__w
    @property
    def H(self): return self.__h
    @property
    def Items(self): return self.__items
    @Items.setter
    def Items(self, v): self.__items = v
    def __init__(self,screen,items=None,x=-1,y=-1,w=-1,h=-1):
        self.__items = ['たたかう', 'わざ', 'まほう', 'どうぐ', 'にげる'] if items is None else items
        self.__x = x
        self.__y = y
        self.__w = self.__get_window_width() if -1 == w else w
        self.__h = self.__get_window_height() if -1 == h else h
        super().__init__(screen,self.X,self.Y,self.W,self.H)
        self.draw()
    def __get_window_height(self): # +2はボーダーラインの幅
        return len(self.__items) + 2
    def __get_window_width(self): # +2はボーダーラインの幅
        return max(self.__get_item_width(i) for i in self.__items) + 2
    def __get_item_width(self, item):
        return sum([1 if c in string.printable else 2 for c in item])
    def draw(self):
        try:
            for i, s in enumerate(self.__items):
                self.Inner.addstr(i, 0, s.ljust(self.__w), curses.color_pair(1))
        except curses.error: pass
        super().draw()

class CursorListWindow(ListWindow):
    def up(self):
        self.__index = len(self.Items)-1 if self.__index <= 0 else self.__index-1
    def down(self):
        self.__index = 0 if len(self.Items)-1 <= self.__index else self.__index+1
    def __init__(self,screen,items=None,index=0,x=-1,y=-1,w=-1,h=-1):
        self.__index = index
        super().__init__(screen,items=items,x=x,y=y,w=w,h=h)
#        self.input()
    def draw(self):
        try:
            for i, s in enumerate(self.Items):
                self.Inner.addstr(i, 0, s.ljust(self.W), 
                                  curses.color_pair(1) | curses.A_REVERSE if i == self.__index else curses.color_pair(1))
        except curses.error: pass
        self.Inner.refresh();
    def input(self):
        self.Screen.keypad(True)
        x = 0
        y = 0
        while True:
            key = self.Screen.getch()
            h, w = self.Inner.getmaxyx()
            if ord('q') == key or 27 == key: break
            if curses.KEY_UP == key: self.up()
            if curses.KEY_DOWN == key: self.down()
            try: self.draw()
            except curses.error: pass
            time.sleep(0.01)

class ScrollCursorListWindow(CursorListWindow):
    def __init__(self,screen,items=None,index=0,x=-1,y=-1,w=-1,h=-1):
#        items = [str(i) for i in range(0, 100)]
        super().__init__(screen,items=items,index=index,x=x,y=y,w=w,h=h)
        self.Items = [str(i) for i in range(0, 100)]
#        sefl.Outer.resize(4, 82)
#        sefl.Inner.resize(2, 80)
#        self.Items = ['A', 'B']
#        self.Inner.resize(h,w)
#        self.Inner.scrollok(True)
#        self.Inner.idlok(True)
#        h, w = self.Inner.getmaxyx()
#        self.Inner.setscrreg(1, 4)
        self.input()
    def input(self):
        self.Screen.keypad(True)
        page = 0
        while True:
            key = self.Screen.getch()
            h, w = self.Inner.getmaxyx()
            if ord('q') == key or 27 == key: break
#            if curses.KEY_UP == key: self.up()
#            if curses.KEY_DOWN == key: self.down()
#            if curses.KEY_UP == key: self.Inner.scroll(1)
#            if curses.KEY_DOWN == key: page += 1; key: self.Inner.scroll(page)
#            if curses.KEY_UP == key: self.Inner.scroll()
#            if curses.KEY_DOWN == key: self.Inner.scroll()
            if curses.KEY_UP == key:
                page += 1
            if curses.KEY_DOWN == key: 
                page -= 1
            h, w = self.Inner.getmaxyx()
            self.Inner.refresh(page, 0, h, w, h, w)


            try: self.draw()
            except curses.error: pass
            time.sleep(0.01)


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(Main)

