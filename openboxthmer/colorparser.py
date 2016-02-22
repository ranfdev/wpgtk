#!/usr/bin/env python3
import fileinput
from subprocess import call
from sys import argv
from colorsys import rgb_to_hls
from colorsys import hls_to_rgb
from getpass import getuser
from random import randint

homedir = "/home/" + getuser()
walldir = homedir + "/.wallpapers/"


def read_color_in_line( xres_file ):
    xres_file = "." + xres_file + ".Xres"
    try:
        f = open( walldir + xres_file, "r" )
    except IOError as err:
        print( err )
        print( err.args )
        print( err.filename )
        return "4A838F"
    line_get = randint( 2, 10 )
    xres_list = [ line for line in f ]
    color = xres_list[ line_get ]
    color = color.split( " ", len( color ) )
    color = color[1]
    color = color.strip( '#' )
    color = color.strip( '\n' )
    return color

def reduce_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hsl = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hsl = list(hsl)
    hsl[1] = hsl[1] - reduce_lvl
    rgb = hls_to_rgb( hsl[0], hsl[1], hsl[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def add_brightness( hex_string, reduce_lvl ):
    rgb = list( int(hex_string[i:i+2], 16) for i in ( 0, 2, 4 ) )
    hsl = rgb_to_hls( rgb[0], rgb[1], rgb[2] )
    hsl = list(hsl)
    hsl[1] = hsl[1] + reduce_lvl
    rgb = hls_to_rgb( hsl[0], hsl[1], hsl[2] )
    rgb_int = []
    for elem in rgb:
        rgb_int.append( int(elem) )
    rgb_int = tuple( rgb_int )
    hex_result = '%02x%02x%02x' % rgb_int
    return hex_result

def change_colors_tint2( active, inactive ):
    backupdir = homedir + "/.themes/colorbamboo/openbox-3/themerc.base"
    realdir = homedir + "/.themes/colorbamboo/openbox-3/themerc"
    call( ["cp", backupdir, realdir] )
    with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
        for line in file:
            print( line.replace( "4A838F", active ), end='' )
    with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
        for line in file:
            print( line.replace( "2C4448", inactive ), end='' )
    call( [ "sh", "-c", "(killall -e tint2) & (sleep 1s && tint2) &"] )

def change_colors_ob( active, inactive ):
    backupdir = homedir + "/.config/tint2/tint2rc.base"
    realdir = homedir + "/.config/tint2/tint2rc"
    call( ["cp", backupdir, realdir] )
    with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
        for line in file:
            print( line.replace( "4A838F".lower(), active ), end='' )
    with fileinput.FileInput( realdir, inplace=True, backup=False ) as file:
        for line in file:
            print( line.replace( "2C4448".lower(), inactive ), end='' )
    call( ["openbox", "--reconfigure"] )

if __name__ == "__main__":
    base_color = read_color_in_line( argv[1] )
    if( base_color == "4A838F" ):
        base_redux = 0
        inact_redux = 50
    else:
        base_redux = 30
        inact_redux = 78
    active = reduce_brightness( base_color, base_redux )
    inactive = reduce_brightness( base_color, inact_redux )
    print( active )
    print( inactive )
    change_colors_ob( active, inactive )
    change_colors_tint2( active, inactive )
    print( "SUCCESS" )
