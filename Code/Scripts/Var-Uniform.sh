#!/bin/sh

for deadline in "${Final_deadline[@]}"
do
  for var in "${variance[@]}"
  do
    mkdir -p Results/Var/uniform/$deadline/$var
    resultsfile="Results/Var/uniform/$deadline/$var/"

    export resultsfile
    export deadline
    export var

    python3 Src/meandelay-uniform.py
  done
done