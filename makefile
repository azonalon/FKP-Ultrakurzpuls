main.pdf: main.tex
	# pdflatex -synctex=1 -shell-escape -interaction=nonstop-mode main.tex
	# biber	  main
	# pdflatex -synctex=1 -shell-escape -interaction=nonstop-mode main.tex
	# pdflatex -synctex=1 -shell-escape -interaction=nonstop-mode main.tex
	# pdflatex -synctex=1 -shell-escape -interaction=nonstop-mode main.tex
	rubber main.tex


clean:
	rm *.aux
	rm *.log
	rm *.gz
	rm *.blg
	rm *.bbl
	rm *.lof
	rm *.lot
	rm *.out
	rm *.ptc
	rm *.toc
	rm *blx.bib
	rm *run.xml
	rm *.bcf                                                                                                                                                  
