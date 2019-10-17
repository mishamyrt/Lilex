UNAME := $(shell uname)

all: ttf otf vf

ttf:
	./scripts/build_ttf

otf:
	./scripts/build_otf

vf:
	./scripts/build_vf

install:
	 -@make install_$(UNAME)

install_Darwin:
	rm -rf ~/Library/Fonts/Lilex
	cp -r build/otf ~/Library/Fonts/Lilex

install_Linux:
	mkdir -p ~/.fonts
	rm -rf ~/.fonts/Lilex