DESTDIR?=
PREFIX?=/usr/local
LOCALBASE?=${PREFIX}

CFLAGS=-g -Wall -D_BSDCONV_INTERNAL -I${LOCALBASE}/include
LIBS=-L${LOCALBASE}/lib -lbsdconv

TODO_CODECS=
TODO_CODECS+=from/_CNS11643
TODO_CODECS+=inter/CHEWING
TODO_CODECS+=inter/CNS11643
TODO_CODECS+=inter/CNS11643-UNICODE
TODO_CODECS+=inter/CNS11643-UNICODE-PUA
TODO_CODECS+=inter/HAN-PINYIN
TODO_CODECS+=inter/ZH-COMP
TODO_CODECS+=inter/ZH-DECOMP
TODO_CODECS+=to/_CNS11643
TODO_CODECS+=to/ASCII-HTML-CNS11643-IMG

all: build

builddir:
	mkdir -p build/share/bsdconv/from
	mkdir -p build/share/bsdconv/inter
	mkdir -p build/share/bsdconv/to

installdir:
	mkdir -p ${DESTDIR}${PREFIX}/share/bsdconv/from
	mkdir -p ${DESTDIR}${PREFIX}/share/bsdconv/inter
	mkdir -p ${DESTDIR}${PREFIX}/share/bsdconv/to

build: | builddir
	for item in ${TODO_CODECS} ; do \
		bsdconv-mktable modules/$${item}.txt ./build/share/bsdconv/$${item} ; \
		if [ -e modules/$${item}.man ]; then cp modules/$${item}.man ./build/share/bsdconv/$${item}.man ; fi ; \
		if [ -e modules/$${item}.c ]; then echo Build $${item}.so; $(CC) ${CFLAGS} -fPIC -shared -o ./build/share/bsdconv/$${item}.so modules/$${item}.c ${LIBS} ; fi ; \
	done

install: | installdir
	for item in ${TODO_CODECS} ; do \
		install -m 444 build/share/bsdconv/$${item} ${DESTDIR}${PREFIX}/share/bsdconv/$${item} ; \
		if [ -e build/share/bsdconv/$${item}.man ]; then install -m 444 build/share/bsdconv/$${item}.man ${DESTDIR}${PREFIX}/share/bsdconv/$${item}.man ; fi ; \
		if [ -e build/share/bsdconv/$${item}.so ]; then install -m 444 build/share/bsdconv/$${item}.so ${DESTDIR}${PREFIX}/share/bsdconv/$${item}.so ; fi ; \
	done

clean:
	rm -rf build

# Source: https://data.gov.tw/dataset/5961

work/data.zip:
	mkdir -p work
	wget -O work/data.zip http://www.cns11643.gov.tw/AIDB/Open_Data.zip

work/data: work/data.zip
	mkdir -p work/data
	unzip -d work/data work/data.zip

gen: work/data
	python3 gen.py work/data/Open_Data modules
