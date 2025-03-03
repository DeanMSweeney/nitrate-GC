set grid
set pointsize 2
set xlabel "Energy [eV]"
set ylabel "DOS"
set nokey
set terminal postscript eps color
set output "dosplot.eps"
plot "DOS33" u 1:2 w lp lt 1 lw 2.0 pt 7 ps 0.6