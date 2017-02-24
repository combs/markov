#!/bin/bash

cd /var/db/ngramradio || exit
# speak(txt_file, m4a_file, voice)
function speak()
{
if [ ! -e $1 ]
then
  echo "$1 not found"
  return
fi
if [ ! -e $2 ] || [ $1 -nt $2 ]
then
  say -v $3 -f $1 -o $2 || rm $2 &
fi

}

speak text/alice-7-2400000.txt alice-7-2400000-osx_ava-monolithic.m4a ava
speak text/constitution-9-2400000.txt constitution-9-2400000-osx_susan-monolithic.m4a susan
speak text/frankenstein-5-2400000.txt frankenstein-5-2400000-osx_fiona-monolithic.m4a fiona
speak text/kant-12-2400000.txt kant-12-2400000-osx_ting-ting-monolithic.m4a ting-ting
speak text/metamorphosis-9-2400000.txt metamorphosis-9-2400000-osx_amelie-monolithic.m4a amelie
speak text/shakespeare-7-2400000.txt shakespeare-7-2400000-osx_lee-monolithic.m4a lee
speak text/sherlock-11-2400000.txt sherlock-11-2400000-osx_oliver-monolithic.m4a oliver
speak text/trump-7-2400000.txt trump-7-2400000-osx_alex-monolithic.m4a alex

wait

for arg in *mono*.m4a
do
  OGG="`echo $arg | sed -e 's:m4a:ogg:'`"
  MP3="`echo $arg | sed -e 's:m4a:mp3:'`"
  if [ "$arg" -nt "$OGG" ] || [ ! -e "$OGG" ]
  then
    ffmpeg -y -loglevel panic -hide_banner -threads 8 -i "$arg" -threads 8 -acodec libvorbis -y -aq 30 -vn -ac 1 -threads 8 "$OGG" || rm "$OGG"  &
  fi
  if [ "$arg" -nt "$MP3" ] || [ ! -e "$MP3" ]
  then
    ffmpeg -y -loglevel panic -hide_banner -threads 8 -i "$arg" -acodec libmp3lame -ac 1 -q:a 9 -ar 22050 "$MP3" || rm "$MP3" &
  fi

done

wait
./sync.sh
