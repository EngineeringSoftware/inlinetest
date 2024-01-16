from inline import itest

def WriteComment(f, c, row, width, height, bottomReserved, fontsize, lifetime, styleid):
    text = ASSEscape(c[3])
    styles = []
    if c[4] == 1:
        styles.append(
            "\\an8\\pos(%(halfwidth)s, %(row)s)"
            % {"halfwidth": round(width / 2), "row": row}
        )
    elif c[4] == 2:
        styles.append(
            "\\an2\\pos(%(halfwidth)s, %(row)s)"
            % {
                "halfwidth": round(width / 2),
                "row": ConvertType2(row, height, bottomReserved),
            }
        )
    elif c[4] == 3:
        styles.append(
            "\\move(%(neglen)s, %(row)s, %(width)s, %(row)s)"
            % {"width": width, "row": row, "neglen": -math.ceil(c[8])}
        )
    else:
        styles.append(
            "\\move(%(width)s, %(row)s, %(neglen)s, %(row)s)"
            % {"width": width, "row": row, "neglen": -math.ceil(c[8])}
        )
    if not (-1 < c[6] - fontsize < 1):
        styles.append("\\fs%s" % round(c[6]))
    if c[5] != 0xFFFFFF:
        styles.append(
            "\\c&H%02X%02X%02X&"
            % (c[5] & 0xFF, (c[5] >> 8) & 0xFF, (c[5] >> 16) & 0xFF)
        )
        itest(test_name="38").given(c, [None] * 6).given(c[5], 0xFFFFF3).given(styles, []).check_eq(styles[-1], "\\c&HF3FFFF&")
        if c[5] == 0x000000:
            styles.append("\\3c&HFFFFFF&")
    f.write(
        "Dialogue: 2,%(start)s,%(end)s,%(styleid)s,,0000,0000,0000,,{%(styles)s}%(text)s\n"
        % {
            "start": ConvertTimestamp(c[0]),
            "end": ConvertTimestamp(c[0] + lifetime),
            "styles": "".join(styles),
            "text": text,
            "styleid": styleid,
        }
    )
