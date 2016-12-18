#!/bin/bash

PICKS='alice*ava*.mp3 brothers*milena*.mp3 trump*alex*.mp3 shakesp*lee*.mp3 frank*fiona*.mp3 sherlock*oliver*.mp3 const*susan*.mp3 kant*ting*.mp3 meta*amelie*.mp3 '
cd /var/db/ngramradio
rsync -var --progress $PICKS chip@ngramradio.local:radio/
