#!/bin/sh

mkdir -p Results/novar

for deadline in "${Final_deadline[@]}"
do
  mkdir -p Results/novar/$deadline/
  resultsfile="Results/novar/$deadline/"
  export deadline
  export resultsfile
  python3 Src/e-greedy-presentation.py
done
