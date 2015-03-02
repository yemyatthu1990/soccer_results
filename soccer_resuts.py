#!/usr/bin/env python
from bs4 import BeautifulSoup
from random import randint
from datetime import date,timedelta
import requests
import time

raw_today_date = date.today()
today_time = raw_today_date.strftime("%Y%m%d")

has_fixture = False
eplurl = "http://scores.nbcsports.com/epl/scoreboard_daily.asp"
ligaurl = "http://scores.nbcsports.com/liga/scoreboard_daily.asp"
seriurl = "http://scores.nbcsports.com/seri/scoreboard_daily.asp"
bundurl = "http://scores.nbcsports.com/bund/scoreboard_daily.asp"
#url =  "http://scores.nbcsports.com/epl/scoreboard_daily.asp?gameday=%s" % (today_time)

# color range - 30,38
def color(this_color, string):
    return "\033[" + this_color + "m" + string + "\033[0m"

# I copied it from https://github.com/addyosmani/psi/blob/master/lib%2Futils.js#L36-L50
def buffer(msg, length):
        ret = ""

	length = length - len(msg) - 1

	if length > 0:
            ret = " " * length
        

	return ret

""" getTerminalSize()
 - get width and height of console
 - works on linux,os x,windows,cygwin(windows)
"""

__all__=['getTerminalSize']


def getTerminalSize():
   import platform
   current_os = platform.system()
   tuple_xy=None
   if current_os == 'Windows':
       tuple_xy = _getTerminalSize_windows()
       if tuple_xy is None:
          tuple_xy = _getTerminalSize_tput()
          # needed for window's python in cygwin's xterm!
   if current_os == 'Linux' or current_os == 'Darwin' or  current_os.startswith('CYGWIN'):
       tuple_xy = _getTerminalSize_linux()
   if tuple_xy is None:
       print "default"
       tuple_xy = (80, 25)      # default value
   return tuple_xy

def _getTerminalSize_windows():
    res=None
    try:
        from ctypes import windll, create_string_buffer

        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12

        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    except:
        return None
    if res:
        import struct
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        sizex = right - left + 1
        sizey = bottom - top + 1
        return sizex, sizey
    else:
        return None

def _getTerminalSize_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
       import subprocess
       proc=subprocess.Popen(["tput", "cols"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       cols=int(output[0])
       proc=subprocess.Popen(["tput", "lines"],stdin=subprocess.PIPE,stdout=subprocess.PIPE)
       output=proc.communicate(input=None)
       rows=int(output[0])
       return (cols,rows)
    except:
       return None


def _getTerminalSize_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl, termios, struct, os
            cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ,'1234'))
        except:
            return None
        return cr
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (env['LINES'], env['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

def scrap_web (web_url,leauge):
    league_name= leauge
    r = requests.get(web_url)
#    global has_fixture          
    data =  r.text
    global raw_today_date
    soup = BeautifulSoup(data)
    sizex,sizey = getTerminalSize()
    line_break = '*' * sizex
    today_time_pretty = "For %s" % (raw_today_date.strftime("%d-%m-%Y"))
    today_break = '-' * len(today_time_pretty)


    print color(str(randint(31,38)),"\n%s Daily Results - Brought to you by Ye Myat Thu with <3" %(league_name))
        
    print line_break+"\n"
    print color(str(randint(31,38)),today_time_pretty)
    print today_break+"\n"
    
    for table in soup.find_all('td'):
        if table.get('class') != None:
            for data in table.get('class'):
                if 'HomeTeam' in data:
 #                   has_fixture = True
                    print color(str(randint(31,38)),table.span.get('title'))+" ",
                    print buffer(table.span.get('title'),24),
                    
                if 'Score' in data and 'Half' not in data and table.get('style') == None and table.get("colspan") == None: 
  #                      has_fixture = True 
                    print table.get_text()+" ",

                if 'AwayTeam' in data:
   #                 has_fixture = True
                    print buffer(table.span.get('title'),24),
                    print color(str(randint(31,38)),table.span.get('title')) +"\n"

    # if has_fixture is False:
    #     print color(str(randint(31,38)),"No Results for today!\n")
    #     see_yest = raw_input("Do you want previous day results? y/n: " )
    #     if see_yest == 'y':
    #         raw_today_date = raw_today_date-timedelta(1)
    #         today_time =  (raw_today_date.strftime("%Y%m%d"))
    #         url = "http://scores.nbcsports.com/epl/scoreboard_daily.asp?gameday=%s" % (today_time)
    #         scrap_epl(url)
    #     elif see_yest == 'n':
    #         sys.exit(0)

if __name__ == "__main__":
    try:
        scrap_web(eplurl,'Premier League')
        scrap_web(ligaurl,'La Liga')
        scrap_web(seriurl,'Serie A')
        scrap_web(bundurl,'Bundesliga')
    except requests.ConnectionError:
       print "No connection available"
