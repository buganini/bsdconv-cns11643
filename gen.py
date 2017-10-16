import os
import sys
import bsdconv
import unicodedata

dataset = sys.argv[1]
output = sys.argv[2]

def p(s):
    s = s.lstrip("0")
    if len(s) & 1:
        return "0" + s
    return s

def in_unicode_pua(cp):
    cp = int(cp, 16)
    if 0xE000 <= cp and cp <= 0xF8FF:
        return True
    if 0xF0000 <= cp and cp <= 0xFFFFD:
        return True
    if 0x100000 <= cp and cp <= 0x10FFFD:
        return True
    return False

brepr = bsdconv.Bsdconv("utf-8:bsdconv")
def bsdconv_repr(s):
    return brepr.conv(s)

def chewing_normalize(s):
    if s[0]=="˙":
        s = s[1:] + s[0]
    if not s[-1] in "ˊˇˋ˙":
        s = s + " "
    return s

def ascii_fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

################################################################################
UNICODE_CNS_MAPPING_TABLE = (
    "MapingTables/Unicode/CNS2UNICODE_Unicode BMP.txt",
    "MapingTables/Unicode/CNS2UNICODE_Unicode 2.txt",
    "MapingTables/Unicode/CNS2UNICODE_Unicode 15.txt",
)
cns_ucs = {}
ucs_cns = {}
for tbl in UNICODE_CNS_MAPPING_TABLE:
    with open(os.path.join(dataset, tbl)) as f:
        for l in f:
            l = l.strip()
            if not l:
                continue
            la = l.split("\t")
            cns = "{}{}".format(p(la[0]), p(la[1]))
            ucs = "{}".format(p(la[2]))
            cns_ucs[cns] = ucs
            ucs_cns[ucs] = cns

with open(os.path.join(output, "inter/CNS11643-UNICODE.txt"), "w") as f, open(os.path.join(output, "inter/CNS11643-UNICODE-PUA.txt"), "w") as pua:
    for cns in sorted(cns_ucs.keys()):
        ucs = cns_ucs[cns]
        if in_unicode_pua(ucs):
            pua.write("02{}\t01{}\n".format(cns, ucs))
        else:
            f.write("02{}\t01{}\n".format(cns, ucs))

with open(os.path.join(output, "inter/CNS11643.txt"), "w") as f:
    for ucs in sorted(ucs_cns.keys()):
        cns = ucs_cns[ucs]
        f.write("01{}\t02{}\n".format(ucs, cns))

################################################################################
compmap = {1111:"0400"}
with open(os.path.join(dataset, "Properties/CNS_component_word.txt")) as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        la = l.split("\t")
        compmap[int(la[0])] = "04" + p("{:X}".format(int(la[1])))

compdata = {}
with open(os.path.join(dataset, "Properties/CNS_component.txt")) as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        la = l.split("\t")
        cns = "{}{}".format(p(la[0]), p(la[1]))
        ucs = cns_ucs[cns]
        cpss = la[2].split(";")
        error = False
        try:
            for i, c in enumerate(cpss):
                cpss[i] = [int(x) for x in c.split(",")]
                for j,t in enumerate(cpss[i]):
                    if not t in compmap:
                        error = True
                        print("Error:", l, "# undefined component", t)
        except:
            error = True
            print("Error:", l, "# unexpected format")
        if not error:
            cps = ",".join([compmap[int(x)] for x in cpss[0]])
            compdata[ucs] = cps

with open(os.path.join(output, "inter/ZH-DECOMP.txt"), "w") as zhdecomp, open(os.path.join(output, "inter/ZH-COMP.txt"), "w") as zhcomp:
    for ucs in sorted(compdata.keys(), key=lambda x: int(x, 16)):
        cps = compdata[ucs]
        zhdecomp.write("01{}\t{}\n".format(ucs, cps))
        zhcomp.write("{}\t01{}\n".format(cps, ucs))

################################################################################
chewing_raw = {}
chewing = {}
with open(os.path.join(dataset, "Properties/CNS_phonetic.txt")) as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        la = l.split("\t")
        cns = "{}{}".format(p(la[0]), p(la[1]))
        ucs = cns_ucs[cns]
        phonetic = ",".join([bsdconv_repr(x) for x in chewing_normalize(la[2])])
        chewing[ucs] = phonetic
        chewing_raw[ucs] = la[2]

with open(os.path.join(output, "inter/CHEWING.txt"), "w") as out:
    for ucs in sorted(chewing.keys()):
        phonetic = chewing[ucs]
        out.write("01{}\t{}\n".format(ucs, phonetic))

################################################################################
pinyin = {}
with open(os.path.join(dataset, "Properties/CNS_pinyin.txt")) as f:
    for l in f:
        l = l.strip()
        if not l:
            continue
        la = l.split("\t")
        chewing = la[0].replace("ˊ", "").replace("ˇ", "").replace("ˋ", "").replace("˙", "")
        chewing = ",".join([bsdconv_repr(x) for x in chewing])
        pinyin[chewing] = ascii_fold(la[1])

cwpy_table = [
    ("013105", "015B,0162,015D"),
    ("013106", "015B,0170,015D"),
    ("013107", "015B,016D,015D"),
    ("013108", "015B,0166,015D"),
    ("013109", "015B,0164,015D"),
    ("01310A", "015B,0174,015D"),
    ("01310B", "015B,016E,015D"),
    ("01310C", "015B,016C,015D"),
    ("01310D", "015B,0167,015D"),
    ("01310E", "015B,016B,015D"),
    ("01310F", "015B,0168,015D"),
    ("013110", "015B,0167,0169,015D"),
    ("013111", "015B,0163,0168,015D"),
    ("013112", "015B,0163,0173,015D"),
    ("013113", "015B,0174,017A,015D"),
    ("013114", "015B,0174,0163,0168,015D"),
    ("013115", "015B,0173,0168,015D"),
    ("013116", "015B,016A,0172,015D"),
    ("013117", "015B,017A,0168,015D"),
    ("013118", "015B,0174,0173,015D"),
    ("013119", "015B,0173,015D"),
    ("013127", "015B,0169,015D"),
    ("013128", "015B,0175,015D"),
    ("013129", "015B,0179,015D"),
    ("01311A", "015B,0161,015D"),
    ("01311B", "015B,016F,015D"),
    ("01311C", "015B,0175,0168,015D"),
    ("01311D", "015B,0161,0165,015D"),
    ("01311E", "015B,0161,0169,015D"),
    ("01311F", "015B,0165,0168,015D"),
    ("013120", "015B,0161,016F,015D"),
    ("013121", "015B,016F,0175,015D"),
    ("013122", "015B,0161,0165,016E,015D"),
    ("013123", "015B,0165,016E,015D"),
    ("013124", "015B,0161,0161,016E,015D"),
    ("013125", "015B,0175,016E,015D"),
    ("013126", "015B,0165,0172,015D"),
    ("0102CA", "0132"),
    ("0102C7", "0133"),
    ("0102CB", "0134"),
    ("0102D9", "0135"),
]
with open(os.path.join(output, "inter/HAN-PINYIN.txt"), "w") as out:
    for cw in sorted(pinyin.keys()):
        py = ",".join([bsdconv_repr(x) for x in pinyin[cw]])
        out.write("{}\t{}\n".format(cw, py))
    for cw, py in cwpy_table:
        out.write("{}\t{}\n".format(cw, py))
