from typing import Optional
from inline import Here

def dga(
    self,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    tld: Optional[str] = None,
    length: Optional[int] = None,
) -> str:
    """Generates a domain name by given date
    https://en.wikipedia.org/wiki/Domain_generation_algorithm

    :type year: int
    :type month: int
    :type day: int
    :type tld: str
    :type length: int
    :rtype: str
    """

    domain = ""
    year = year or self.random_int(min=1, max=9999)
    month = month or self.random_int(min=1, max=12)
    day = day or self.random_int(min=1, max=30)
    tld = tld or self.tld()
    length = length or self.random_int(min=2, max=63)

    for _ in range(length):
        year = ((year ^ 8 * year) >> 11) ^ ((year & 0xFFFFFFF0) << 17)
        Here().given(year, 1000).check_eq(year, 130023427)
        month = ((month ^ 4 * month) >> 25) ^ 16 * (month & 0xFFFFFFF8)
        Here().given(month, 1).check_eq(month, 0)
        day = ((day ^ (day << 13)) >> 19) ^ ((day & 0xFFFFFFFE) << 12)
        Here().given(day, 1).check_eq(day, 0)
        domain += chr(((year ^ month ^ day) % 25) + 97)
        Here().given(year, 130023427).given(month, 0).given(day, 0).given(domain, "").check_eq(domain, "c")

    return domain + "." + tld
