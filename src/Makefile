
opt=-Xmx1024m 
jar=../thirdparty/antlr-3.1.3.jar
gramfile=JavaScript
ending=.g 
antlropt=-Xconversiontimeout 200000 
outputdir=jshadobf/parser





$(outputdir)/$(gramfile)Parser.py: $(gramfile)$(ending)
	java $(opt) -jar $(jar) $(gramfile)$(ending) $(antlropt) -o $(outputdir)


force: 
	@touch $(gramfile)$(ending)
	@$(MAKE)


clean:
	find ./ -name "*.pyo" -exec rm  \{\} \;
	find ./ -name "*.pyc" -exec rm  \{\} \;
	find ./ -name "*~" -exec rm  \{\} \;
	rm -f *~ $(outputdir)/$(gramfile)Lexer.py *.pyc $(outputdir)/$(gramfile)Parser.py *.o $(outputdir)/*.tokens 

