#!/bin/sh
for filename in *;
do 
if [`date -r $filename +%y%m%d` <= "160429"];
then rm $filename;
fi 
done
