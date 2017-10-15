import os
import sys

dataset = sys.argv[1]
output = sys.argv[2]

def p(s):
    s = s.lstrip("0")
    if len(s) & 1:
        return "0" + s
    return s

def inUnicodePUA(cp):
    cp = int(cp, 16)
    if 0xE000 <= cp and cp <= 0xF8FF:
        return True
    if 0xF0000 <= cp and cp <= 0xFFFFD:
        return True
    if 0x100000 <= cp and cp <= 0x10FFFD:
        return True
    return False

# Unicode - CNS11643 Mapping
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
cnsl = sorted(cns_ucs.keys())
ucsl = sorted(ucs_cns.keys())

with open(os.path.join(output, "inter/CNS11643-UNICODE.txt"), "w") as f, open(os.path.join(output, "inter/CNS11643-UNICODE-PUA.txt"), "w") as pua:
    for cns in cnsl:
        ucs = cns_ucs[cns]
        if inUnicodePUA(ucs):
            pua.write("02{}\t01{}\n".format(cns, ucs))
        else:
            f.write("02{}\t01{}\n".format(cns, ucs))
