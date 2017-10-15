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

with open(os.path.join(output, "inter/CNS11643.txt"), "w") as f:
    for ucs in ucsl:
        cns = ucs_cns[ucs]
        f.write("01{}\t02{}\n".format(ucs, cns))

# ZH-COMP / ZH-DECOMP
compmap = {1111:"0400"}
with open(os.path.join(dataset, "Properties/CNS_component_word.txt"), encoding="UTF-16LE") as f:
    for l in f:
        l = l .strip().strip("\ufeff")
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
            compdata[cns] = cps
compl = sorted(compdata.keys())
with open(os.path.join(output, "inter/ZH-DECOMP.txt"), "w") as zhdecomp, open(os.path.join(output, "inter/ZH-COMP.txt"), "w") as zhcomp:
    for cns in compl:
        cps = compdata[cns]
        zhdecomp.write("02{}\t{}\n".format(cns, cps))
        zhcomp.write("{}\t02{}\n".format(cps, cns))
