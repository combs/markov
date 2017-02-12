#!/bin/bash
say -v ava -f text/alice-7-2400000.txt -o alice-7-2400000-osx_ava-monolithic.m4a
say -v susan -f text/constitution-9-2400000.txt -o constitution-9-2400000-osx_susan-monolithic.m4a
say -v fiona -f text/frankenstein-5-2400000.txt -o frankenstein-5-2400000-osx_fiona-monolithic.m4a
say -v ting-ting -f text/kant-12-2400000.txt -o kant-12-2400000-osx_ting-ting-monolithic.m4a
say -v amelie -f text/metamorphosis-9-2400000.txt -o metamorphosis-9-2400000-osx_amelie-monolithic.m4a
say -v lee -f text/shakespeare-7-2400000.txt -o shakespeare-7-2400000-osx_lee-monolithic.m4a
say -v oliver -f text/sherlock-11-2400000.txt -o sherlock-11-2400000-osx_oliver-monolithic.m4a
say -v alex -f text/trump-7-2400000.txt -o trump-7-2400000-osx_alex-monolithic.m4a

for arg in *.m4a
do ffmpeg -loglevel panic -hide_banner -threads 8 -i "$arg" -threads 8 -acodec libvorbis -y -aq 30 -vn -ac 1 -threads 8 "`echo $arg | sed -e 's:m4a:ogg:'`" & 
ffmpeg -i $arg -acodec libmp3lame -ac 1 -q:a 8 -ar 22050 $arg.mp3 &
done


