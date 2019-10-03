#!/bin/sh

for deadline in "${Final_deadline[@]}"
do
  mkdir -p Results/uniform-wc/$deadline/
  resultsfile="Results/uniform-wc/$deadline/"
  export deadline
  export resultsfile
  python3 Src/meandelay-uniform-worstcase.py
done