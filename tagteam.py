## tagteam.py
# Generates a "KEY-BPM" composite tag in an ID3 tag
#  Wrote this cuz I find it helpful for harmonic mixing to sort by this field

# *** files need to be analyzed first [needs BPM and initial key set] ***

# python3 tagteam.py /path/to/files
#  python3 tagteam.py "/Volumes/Tunes/! Tracks/2021/2021-01"
# - will walk through all files/subdirectories off main path

# requires taglib which was a bit weird to compile
# https://github.com/supermihi/pytaglib#manual-compilation-general
#  on osx had to do a: brew install taglib
#  then run this to install the library
#   pip3 install --global-option=build_ext --global-option="-I/usr/local/include/" --global-option="-L/usr/local/lib" pytaglib;2D

import subprocess
import os
import sys
import taglib

# I like to use the COMPOSER field.  Can't display it on Traktor tho.
# LABEL is a nice easy one that works on both Traktor + Serato
# you can use COMMENT but script nukes the id3v1 version to prevent confusion
tagfield = "LABEL"

fileformats = ["mp3","aiff","wav","flac"]

# list @ https://forums.pioneerdj.com/hc/en-us/community/posts/115018048243-Camelot-Wheel-TO-Key-List-turned-around-Sorted-both-ways-
keys = {
    'A':'11B',
    'Ab': '4B',
    'Am': '8A',
    'A#': '6B',
    'A#m': '3A',
    'Abm': '1A',
    'B': '1B', 
    'Bm': '10A',
    'Bb': '6B',
    'Bbm': '3A',
    'C': '8B',
    'Cm': '5A',
    'C#': '3B',
    'C#m': '12A',
    'D': '10B',
    'Db': '3B',
    'Dm': '7A',
    'D#': '5B',    
    'D#m': '2A',
    'Dbm': '12A',
    'E': '12B',
    'Eb': '5B',
    'Em': '9A',
    'Ebm': '2A',
    'F': '7B',
    'Fm': '4A',
    'F#': '2B',
    'F#m': '11A',
    'G': '9B',
    'Gm': '6A',
    'G#': '4B',
    'Gb': '2B',
    'G#m': '1A',

    # added these after Virtual DJ ate all my key mappings
    '1m': '1B',
    '2m': '2B',
    '3m': '3B',
    '4m': '4B',
    '5m': '5B',
    '6m': '6B',
    '7m': '7B',
    '8m': '8B',
    '9m': '9B',
    '10m': '10B',
    '11m': '11B',
    '12m': '12B',
    
    '1d': '1A',
    '2d': '2A',
    '3d': '3A',
    '4d': '4A',
    '5d': '5A',
    '6d': '6A',
    '7d': '7A',
    '8d': '8A',
    '9d': '9A',
    '10d': '10A',
    '11d': '11A',
    '12d': '12B'    
}

walk_dir = None

if len(sys.argv) == 2:
    walk_dir = sys.argv[1]

if not walk_dir:
    print("Did you forget the directory?  tagteam.py /path/to/audiofiles")
    sys.exit()

print('Starting directory = ' + os.path.abspath(walk_dir))

for root, subdirs, files in os.walk(walk_dir):
        for filename in files:
            if [ele for ele in fileformats if ("." + ele in filename.lower())]:
                file_path = os.path.join(root, filename)
                print('%s' % (file_path))

                foundkey = None
                bpm = None
                initialkey = None

                song = taglib.File(file_path)

                #throw these thru a .get to make sure they're not missing
                getkey = song.tags.get("INITIALKEY")
                if getkey:
                    initialkey = getkey[0]

                getbpm = song.tags.get("BPM")
                if getbpm:
                    bpm = int(getbpm[0])
                

                if initialkey and bpm:
                    for key in keys:
                        if key == initialkey: 
                            foundkey = keys[key]

                    if foundkey:
                        # round off the bpm to 3 digits
                        newtag = foundkey + "-" + str(bpm).zfill(3)
                        print(' FOUND: %s -> %s = %s' % (initialkey, foundkey, newtag))

                        # if using COMMENT nuke the ID3V1 version if it exists
                        if tagfield == "COMMENT":
                            if "COMMENT:ID3V1 COMMENT" in song.tags:
                                del song.tags["COMMENT:ID3V1 COMMENT"]
                                song.save()
                        
                        song.tags[tagfield] = [newtag]
                        song.save()
                    else:
                        print(' NOT FOUND: %s' % (initialkey))

                else:
                    print('Unable to find bpm (%s) or key (%s) - ensure analyzed in Serato?' % (bpm, initialkey))

