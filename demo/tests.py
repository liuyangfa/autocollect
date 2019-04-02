# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from eventlet.greenthread import sleep

# Create your tests here.
import eventlet
from eventlet.green import urllib2

eventlet.monkey_patch()

def writedata():
    with open("liuyf.txt", "w") as file:
        sleep(2)
        file.write(u"你好".encode('utf-8'))


def main():
    print eventlet.spawn_n(writedata)
    print "over"

if __name__ == '__main__':
    print "start ...."
    main()
    print "end....."