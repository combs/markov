#!/bin/bash
for arg in text/*.txt 
do php runner.php $arg & 
done
