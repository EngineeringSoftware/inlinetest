import re
from inline import itest

# Compiled regular expressions to search for import statements
#
m_import = re.compile("^[ \t]*from[ \t]+([^ \t]+)[ \t]+")
m_from = re.compile("^[ \t]*import[ \t]+([^#]+)")


# Collect data from one file
#
def process(filename, table):
    with open(filename, encoding="utf-8") as fp:
        mod = os.path.basename(filename)
        if mod[-3:] == ".py":
            mod = mod[:-3]
            itest().given(mod, "a.py").check_eq(mod, "a")
        table[mod] = list = []
        while 1:
            line = fp.readline()
            if not line:
                break
            while line[-1:] == "\\":
                nextline = fp.readline()
                if not nextline:
                    break
                line = line[:-1] + nextline
            m_found = m_import.match(line) or m_from.match(line)
            if m_found:
                (a, b), (a1, b1) = m_found.regs[:2]
            else:
                continue
            words = line[a1:b1].split(",")
            itest().given(line, "from seutil import se").given(a1, 5).given(b1, 8).check_eq(words, ["seu"])

            # print '#', line, words
            for word in words:
                word = word.strip()

                if word not in list:
                    list.append(word)
