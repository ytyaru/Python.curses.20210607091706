# curses

　cursesは端末を操作するためのライブラリである。

# 情報源

* [ANSI Escape Code](https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters)
* [howto/curses](https://docs.python.org/ja/3/howto/curses.html)
* [library/curses](https://docs.python.org/ja/3/library/curses.html)

# 実行環境

環境|[ANSI Escape Code][]|ライブラリ
----|--------------------|----------
bash|`echo -e "\e[31m赤\e[m"`|`tput setaf 1 && echo '赤'`
python|`print('\033[31m赤\033[m')`|`import curses`

# python cursesライブラリ

* window/pad

　Pythonのcursesにはwindow/padという便利なクラスがある。これは表示領域を自動的に計算してくれる。

クラス|横幅超過|高さ超過
------|--------|--------
window|折り返す|非表示
pad|指定する|指定する

　windowは端末の物理的な幅／高さが上限である。padは仮想領域をもっており、端末の物理サイズより大きな領域をもてる。そのかわり描画するときはその範囲を指定せねばならない。

```
window.refresh()
pad.refresh(開始行,開始列,終端行,終端列,高さ,幅)
```

　端末サイズを越えた行数を表示したいことがよくある。そのときは以下のようにして開始行を変数にする。なぜか高さは-1しないとエラーになる。`_curses.error: prefresh() returned ERR`

```
pad_start_line = 0
pad.refresh(pad_start_line,0,0,0,curses.LINES-1,curses.COLS)
```

コード|概要
------|----
curses.LINES|端末の物理的な行数
curses.COLS|端末の物理的な列数

# 最小コード

## 0

　なにもせず正常終了する。異常終了しない最小コードである。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses
try:
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
except Exception as e: raise
finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
```

## 1

　赤字`RED`を表示してみる。なにかキーを押下すると終了する。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses
try:
    stdscr = curses.initscr()
    curses.start_color()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.addstr('RED', curses.A_REVERSE | curses.color_pair(1))
    stdscr.getkey()
except Exception as e: raise
finally:
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
```

## 2

　短い最小化コード。`curses.wrapper()`をつかって初期化や`try`,`except`を簡略化する。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses

def main(stdscr): pass

if __name__ == "__main__":
    curses.wrapper(main)
```

## 3

　引数を渡してみる。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses

def main(stdscr, msg):
    stdscr.addstr(msg, curses.A_REVERSE | curses.color_pair(1))
    stdscr.getkey()


if __name__ == "__main__":
    curses.wrapper(main, 'Hello')
```

　引数は`*args`, `**kwargs`のどちらの形式でも渡せる。詳細は[curses.wrapper][]参照。

* [curses.wrapper](https://docs.python.org/ja/3/library/curses.html#curses.wrapper)

[curses.wrapper]:https://docs.python.org/ja/3/library/curses.html#curses.wrapper

## 4

　クラスを渡してみる。`__init__()`が実行される。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses

class Main:
    def __init__(self, screen):
        self.__screen = screen


if __name__ == "__main__":
    curses.wrapper(Main)
```

## 5

　クラスに引数を渡す。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses

class Main:
    def __init__(self, screen, msg):
        self.__screen = screen


if __name__ == "__main__":
    curses.wrapper(Main, 'Hello')
```

## 6

　描画し、キー待受する。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses

class Main:
    def __init__(self, screen, msg):
        self.__screen = screen
        self.__msg = msg
        self.__draw()
        self.__input()
    def __draw(self):
        self.__screen.addstr(self.__msg)
    def __input(self):
        self.__screen.getkey()


if __name__ == "__main__":
    curses.wrapper(Main, 'Hello')
```


## 7

　色の初期化をする。ついでにカーソル非表示。

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses

class Main:
    def __init__(self, screen, msg):
        self.__screen = screen
        self.__msg = msg
        self.__init_cursor()
        self.__init_color_pair()
        self.__draw()
        self.__input()
    def __init_cursor(self): curses.curs_set(0)
    def __init_color_pair(self):
        if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
        if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
        curses.use_default_colors()
        for i in range(1, curses.COLORS):
            curses.init_pair(i, i, curses.COLOR_BLACK)
    def __draw(self):
        self.__screen.addstr(self.__msg, curses.A_REVERSE | curses.color_pair(1))
    def __input(self):
        self.__screen.getkey()


if __name__ == "__main__":
    curses.wrapper(Main, 'Hello')
```




















## 2

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses
def main(stdscr):
    curses.curs_set(0)
    if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
    if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
    curses.use_default_colors()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i, curses.COLOR_BLACK)
    try:
        for i in range(1, curses.COLORS):
            stdscr.addstr(str(i).rjust(3), curses.A_REVERSE | curses.color_pair(i))
    except curses.ERR: pass
    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    try:
        os.environ['TERM'] = 'xterm-256color'
        stdscr = curses.initscr()
        curses.start_color()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        main(stdscr)
    except Exception as e: raise
    finally:
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
```

## 1

```python
#!/usr/bin/env python3
# coding: utf8
import os, curses
def main(stdscr):
    curses.curs_set(0)
    if not curses.has_colors(): raise Exception('このターミナルは色を表示できません。')
    if not curses.can_change_color(): raise Exception('このターミナルは色を変更できません。')
    curses.use_default_colors()
    for i in range(1, curses.COLORS):
        curses.init_pair(i, i, curses.COLOR_BLACK)
    try:
        for i in range(1, curses.COLORS):
            stdscr.addstr(str(i).rjust(3), curses.A_REVERSE | curses.color_pair(i))
    except curses.ERR: pass
    stdscr.refresh()
    stdscr.getkey()


if __name__ == "__main__":
    os.environ['TERM'] = 'xterm-256color'
    curses.wrapper(main)
```

```python
```
```python
```
```python
```
```python
```
#curses.window.refresh
