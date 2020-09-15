LYFILES = $(shell ls *.ly)
TARGET = $(LYFILES:%.ly=%.pdf)

all: $(TARGET)

%.pdf:%.ly
	echo "----------------------------------------------------"
	echo $@ $<

	# pdf
	lilypond $<

	# png
	$(eval RESOLUTION:=$(shell echo $< | awk '{ if ( $$0 ~ /jpn_accent/ ) print 140; else print 220} ' ) )
	echo "****" $< $(RESOLUTION)
	lilypond -dresolution=$(RESOLUTION) -dpixmap-format=pngalpha --png $<
#	lilypond -dresolution=$(RESOLUTION) -danti-alias-factor=10  --png $<

.PHONY:clean
clean:
	rm -f *.pdf *.png
	