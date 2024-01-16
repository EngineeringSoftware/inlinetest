from inline import itest
import re

def get_package_details(self, package):
    # parse values of details that might extend over several lines
    raw_pkg_details = {}
    last_detail = None
    for line in package.splitlines():
        m = re.match(r"([\w ]*[\w]) +: (.*)", line)
        itest().given(line, "a : b").check_eq(m.group(1), "a").check_eq(m.group(2), "b")
        if m:
            last_detail = m.group(1)
            raw_pkg_details[last_detail] = m.group(2)
        else:
            # append value to previous detail
            raw_pkg_details[last_detail] = (
                raw_pkg_details[last_detail] + "  " + line.lstrip()
            )

    provides = None
    if raw_pkg_details["Provides"] != "None":
        provides = [p.split("=")[0] for p in raw_pkg_details["Provides"].split("  ")]

    return {
        "name": raw_pkg_details["Name"],
        "version": raw_pkg_details["Version"],
        "arch": raw_pkg_details["Architecture"],
        "provides": provides,
    }
