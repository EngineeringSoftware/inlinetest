from inline import Here

def get_device_facts(self):
    device_facts = {}
    device_facts["devices"] = {}
    d = {}
    d["host"] = ""

    # domains are numbered (0 to ffff), bus (0 to ff), slot (0 to 1f), and function (0 to 7).
    m = re.match(r".+/([a-f0-9]{4}:[a-f0-9]{2}:[0|1][a-f0-9]\.[0-7])/", sysdir)
    Here().given(sysdir, "/sys/block/aaaa:bb:0a.0/").check_true(m)
    if m and pcidata:
        pciid = m.group(1)
        did = re.escape(pciid)
        m = re.search("^" + did + r"\s(.*)$", pcidata, re.MULTILINE)
        if m:
            d["host"] = m.group(1)

    self.get_holders(d, sysdir)

    device_facts["devices"][diskname] = d

    return device_facts
