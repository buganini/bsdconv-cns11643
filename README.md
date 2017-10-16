* from/_CNS11643
```
$ printf "1234\x00\x01\x60\x41\x00\x01\x66\x5cabcd" | bsdconv cns11643:utf-8
1234測試abcd
```

* inter/CHEWING
```
$ printf "測試" | bsdconv utf-8:chewing:utf-8
ㄘㄜˋㄕˋ
```

* inter/CNS11643
```
$ printf "測" | bsdconv utf-8:bsdconv-output
016E2C ( FREE ) # Unicode

$ printf "測" | bsdconv utf-8:cns11643:bsdconv-output
02016041 # CNS11643

```

* inter/CNS11643-UNICODE
```
$ printf 02016041 | bsdconv bsdconv:bsdconv-output
02016041 # CNS11643

$ printf 02016041 | bsdconv bsdconv:unicode:bsdconv-output # `unicode` is an auto alias
016E2C # Unicode
```

* inter/CNS11643-UNICODE-PUA
```
$ printf 02097459 | bsdconv bsdconv:unicode:bsdconv-output
02097459

$ printf 02097459 | bsdconv bsdconv:unicode:cns11643-unicode-pua:bsdconv-output
010FFBA9
```

* inter/HAN-PINYIN
```
$ printf "測試" | bsdconv utf-8:chewing:han-pinyin:utf-8
ce4shi4
```

* inter/ZH-COMP
* inter/ZH-DECOMP
```
$ printf "功夫不好不要艹我" | bsdconv utf-8:zh-decomp:zh-comp:utf-8
巭孬嫑莪
```


* to/_CNS11643
```
$ printf 測試 | bsdconv utf-8:cns11643 | xxd -p
000160410001665c
```

* to/ASCII-HTML-CNS11643-IMG
```
$ printf 測 | bsdconv utf-8:ASCII-HTML-CNS11643-IMG
<img class="cns11643_img" src="http://www.cns11643.gov.tw/AIDB/png.do?page=1&code=6041" />
```
