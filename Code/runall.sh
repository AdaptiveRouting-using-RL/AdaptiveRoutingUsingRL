#!/bin/sh

Final_deadline=(20 25 30 35 40)
variance=(1 2 3 4 5)
num_episodes=1000

plot_deadline=20,25,30,35,40
plot_variance=1,2,3,4,5

export num_episodes
export Final_deadline
export variance
export plot_deadline
export plot_variance

rm -rf Results/*

. Scripts/NoVariance.sh
. Scripts/Dynamic.sh
. Scripts/Uniform-WC.sh
. Scripts/Var-Normal.sh
. Scripts/Var-Uniform.sh

mkdir pdfs
pdflatex -output-directory pdfs Plots/Fig2-Exp1-NoVariance.tex
pdflatex -output-directory pdfs Plots/Fig3-Exp2-Dynamic.tex
pdflatex -output-directory pdfs Plots/Fig4-Exp3a-Var-Normal.tex
pdflatex -output-directory pdfs Plots/Fig5-Exp3b-Var-Uniform.tex
pdflatex -output-directory pdfs Plots/Fig6-Exp3c-Uniform-WC.tex

#python3 Scripts/Process-res.py
#pdflatex -output-directory pdfs Plots/Var-Normal-paths.tex
#pdflatex -output-directory pdfs Plots/Var-Uniform-paths.tex

## Clean up
rm -r pdfs/*.aux
rm -r pdfs/*.log
