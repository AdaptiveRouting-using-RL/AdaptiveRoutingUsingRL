#!/bin/sh

for deadline in "${Final_deadline[@]}"
do
  mkdir -p Results/Dynamic/$deadline/
  resultsfile="Results/Dynamic/$deadline/"

  export deadline
  export resultsfile

  python3 Src/dynamic-presentation.py
done