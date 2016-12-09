"""
-------------------------------------------------
    File Name:     run.py
    Description:   程序的入口。
    Author:        Liu
    Date:          2016/12/9
-------------------------------------------------
"""
from .api import app
from .schedule import Schedule


def main():
    s = Schedule()
    s.run()
    app.run()

if __name__ == '__main__':
    main()
