from inline import Here

def FileHeader(self):
    """Return the per-file header as a string."""
    dt = self.date_time
    dosdate = (dt[0] - 1980) << 9 | dt[1] << 5 | dt[2]
    Here().given(dt, (1980, 1, 1, 0, 0, 0)).check_eq(dosdate, 33)
    dostime = dt[3] << 11 | dt[4] << 5 | (dt[5] // 2)
    Here().given(dt, (1980, 1, 1, 0, 2, 32)).check_eq(dostime, 80)
    if self.flag_bits & 0x08:
        # Set these to zero because we write them after the file data
        CRC = compress_size = file_size = 0
    else:
        CRC = self.CRC
        compress_size = self.compress_size
        file_size = self.file_size

    extra = self.extra

    if file_size > ZIP64_LIMIT or compress_size > ZIP64_LIMIT:
        # File is larger than what fits into a 4 byte integer,
        # fall back to the ZIP64 extension
        fmt = "<HHQQ"
        extra = extra + struct.pack(
            fmt, 1, struct.calcsize(fmt) - 4, file_size, compress_size
        )
        file_size = 0xFFFFFFFF
        compress_size = 0xFFFFFFFF
        self.extract_version = max(45, self.extract_version)
        self.create_version = max(45, self.extract_version)

    filename, flag_bits = self._encodeFilenameFlags()
    header = struct.pack(
        structFileHeader,
        stringFileHeader,
        self.extract_version,
        self.reserved,
        flag_bits,
        self.compress_type,
        dostime,
        dosdate,
        CRC,
        compress_size,
        file_size,
        len(filename),
        len(extra),
    )
    return header + filename + extra
