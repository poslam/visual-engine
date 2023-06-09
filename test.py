import curses
from curses import wrapper


def main(stdscr):
    stdscr.clear() 
    
    while True:
        key = stdscr.getkey()
        stdscr.addstr(key + '\n')
        
        if key == "KEY_UP":
            stdscr.addstr("aaaaaa")
        
        if key == "l":
            break

wrapper (main)