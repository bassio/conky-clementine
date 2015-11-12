#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#
# anowplaying.py
#
#  Connects to dbus and retrieves
#  information about the currently
#  playing track in amarok.
#

import dbus, optparse, shutil, commands

if __name__ == '__main__':
    '''Check if clementine is running'''
    output = commands.getoutput('ps -A')
    if 'clementine' not in output:
        raise SystemExit

    '''Get system bus'''
    bus = dbus.SessionBus()
    amarok = bus.get_object('org.mpris.clementine', '/Player')
    amarokdict = amarok.GetMetadata()

    '''Set up the command line parser'''
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-a',  '--artist',  action='store_true', help='artist name')
    parser.add_option('-t',  '--title',   action='store_true', help='title of the track')
    parser.add_option('-l',  '--album',   action='store_true', help='album name')
    parser.add_option('-g',  '--genre',   action='store_true', help='genre of the current track')
    parser.add_option('-y',  '--year',    action='store_true', help='year of the track')
    parser.add_option('-m',  '--mtime',    action='store_true', help='time of the track')
    parser.add_option('-r',  '--rtime',    action='store_true', help='remaining time for the track')
    parser.add_option('-e',  '--etime',    action='store_true', help='elapsed time for the track')
    parser.add_option('-p',  '--progress',    action='store_true', help='progress of the track')
    parser.add_option('-n',  '--track',   action='store_true', help='track number')
    parser.add_option('-b',  '--bitrate', action='store_true', help='bitrate of the track')
    parser.add_option('-s',  '--sample',  action='store_true', help='sample rate of the track')
    parser.add_option('-c',  '--cover',   metavar='filename',  help='copy cover art to destination file')
    parser.add_option('-w',  '--titlewrapped',   metavar='length', help='title of the track (text-wrapped)')
    parser.add_option('--bar',   metavar='barmaxlength', help='bar')
    parser.add_option('--bar-remaining',   metavar='barmaxlength', help='bar')
    parser.add_option('--albumwrapped',   metavar='maxlength', help='bar')
    
    '''Get the parser options printed'''
    (opts, args) = parser.parse_args()
    if opts.artist and amarokdict.has_key('artist') :
        artist = amarokdict['artist'].replace("\\", "\n").replace("/", "\n")
        print artist
        
    if opts.title and amarokdict.has_key('title'):
        print amarokdict['title']
    if opts.titlewrapped and amarokdict.has_key('title'):
        title = amarokdict['title'].replace("\\", "\n").replace("/", "\n")
        if len(title) > 25:
            print title + "\n" + title
            
    if opts.album and amarokdict.has_key('album'):
        print amarokdict['album']
        
    if opts.albumwrapped and amarokdict.has_key('album'):
        album = amarokdict['album']
        if len(album) > int(opts.albumwrapped):
            import textwrap
            print textwrap.fill(album, int(opts.albumwrapped))
        else:
            print opts.albumwrapped
            print album
            
    if opts.genre and amarokdict.has_key('genre'):
        print amarokdict['genre']
    if opts.year and amarokdict.has_key('year'):
        print amarokdict['year']
    if opts.track and amarokdict.has_key('tracknumber'):
        print amarokdict['tracknumber']
    if opts.bitrate and amarokdict.has_key('audio-bitrate'):
        print amarokdict['audio-bitrate']
    if opts.sample :
        print amarokdict['audio-samplerate']

    '''Manage time stuff'''
    cpos = mt = mtime = etime = rtime = progress = None
    if (opts.etime or opts.rtime or opts.mtime or opts.progress) and amarokdict.has_key('mtime'):
        cpos    = amarok.PositionGet()/1000
        mt      = amarokdict['mtime']/1000
        mtime   = str(mt/60)+":"+str(mt%60) if mt%60>9 else str(mt/60)+":0"+str(mt%60)
        etime   = str(cpos/60)+":"+str(cpos%60) if cpos%60>9 else  str(cpos/60)+":0"+str(cpos%60)
        rtime   = str((mt-cpos)/60)+":"+str((mt-cpos)%60) if (mt-cpos)%60>9 else str((mt-cpos)/60)+":0"+str((mt-cpos)%60)
        progress= float(cpos)/float(mt)*100
    if opts.etime and etime is not None:
        print etime
    if opts.rtime and rtime is not None:
        print rtime
    if opts.mtime and mtime is not None:
        print mtime
    if opts.progress and progress is not None:
        print progress
    if opts.bar:
        maxbarlength = int(opts.bar)

        cpos    = amarok.PositionGet()/1000
        mt      = amarokdict['mtime']/1000
        mtime   = str(mt/60)+":"+str(mt%60) if mt%60>9 else str(mt/60)+":0"+str(mt%60)
        etime   = str(cpos/60)+":"+str(cpos%60) if cpos%60>9 else  str(cpos/60)+":0"+str(cpos%60)
        rtime   = str((mt-cpos)/60)+":"+str((mt-cpos)%60) if (mt-cpos)%60>9 else str((mt-cpos)/60)+":0"+str((mt-cpos)%60)
        progress= float(cpos)/float(mt)
        
        bar_length = int(progress * maxbarlength)
        
        print("_" * bar_length)

    if opts.cover :
        cover = amarokdict['arturl']
        if cover != "" :
            try :
                shutil.copyfile(cover.replace('file://', ''), opts.cover)
                print ""
            except Exception, e:
                print e
                print ""
        else :
            print ""
    
