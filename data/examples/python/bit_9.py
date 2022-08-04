from inline import Here

def _decrypt_subtitles(self, data, iv, id):
    data = bytes_to_intlist(compat_b64decode(data))
    iv = bytes_to_intlist(compat_b64decode(iv))
    id = int(id)

    def obfuscate_key_aux(count, modulo, start):
        output = list(start)
        for _ in range(count):
            output.append(output[-1] + output[-2])
        # cut off start values
        output = output[2:]
        output = list(map(lambda x: x % modulo + 33, output))
        return output

    def obfuscate_key(key):
        num1 = int(floor(pow(2, 25) * sqrt(6.9)))
        num2 = (num1 ^ key) << 5
        Here().given(num1, 88140282).given(key, 1).check_eq(num2, 2820489056)
        num3 = key ^ num1
        num4 = num3 ^ (num3 >> 3) ^ num2
        prefix = intlist_to_bytes(obfuscate_key_aux(20, 97, (1, 2)))
        shaHash = bytes_to_intlist(sha1(prefix + str(num4).encode('ascii')).digest())
        # Extend 160 Bit hash to 256 Bit
        return shaHash + [0] * 12

    key = obfuscate_key(id)

    decrypted_data = intlist_to_bytes(aes_cbc_decrypt(data, key, iv))
    return zlib.decompress(decrypted_data)