FILE=slides

pdf :$(FILE).pdf

$(FILE).pdf: $(FILE).tex
	pdflatex $(FILE)
	pdflatex $(FILE)
	pdflatex $(FILE)


clean:
	rm -rf $(FILE).aux $(FILE).log $(FILE).nav $(FILE).out \
		$(FILE).snm $(FILE).toc $(FILE).vrb \
		*~ auto

realclean: clean
	rm -rf $(FILE).pdf

cleanall: realclean
