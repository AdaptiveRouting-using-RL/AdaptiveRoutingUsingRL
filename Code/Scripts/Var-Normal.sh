#!/bin/sh

for deadline in "${Final_deadline[@]}"
do
  for var in "${variance[@]}"
  do
    mkdir -p Results/Var/normal/$deadline/$var
    resultsfile="Results/Var/normal/$deadline/$var/"

    export resultsfile
    export deadline
    export var

    python3 Src/meandelay-normal.py
  done
done