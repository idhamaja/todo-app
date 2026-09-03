import os
import time
import uuid


def uuid7() -> str:
    """
    Generate UUID versi 7 (time-ordered UUID, sesuai draft RFC 9562).

    Layout 128-bit:
      - 48 bit  : unix timestamp (ms)
      - 4  bit  : version (0111 = 7)
      - 12 bit  : random A
      - 2  bit  : variant (10)
      - 62 bit  : random B

    Sifat penting: nilai yang dihasilkan urut berdasarkan waktu pembuatan,
    sehingga bagus dipakai sebagai primary key di database (index-friendly),
    berbeda dengan UUID v4 yang benar-benar acak.
    """
    unix_ts_ms = int(time.time() * 1000)
    rand_bytes = os.urandom(10)

    ts_bytes = unix_ts_ms.to_bytes(6, byteorder="big")

    rand_a = int.from_bytes(rand_bytes[0:2], "big") & 0x0FFF
    rand_a_bytes = (0x7000 | rand_a).to_bytes(2, byteorder="big")

    rand_b = int.from_bytes(rand_bytes[2:10], "big") & 0x3FFFFFFFFFFFFFFF
    rand_b |= 0x8000000000000000  # set variant bits menjadi '10'
    rand_b_bytes = rand_b.to_bytes(8, byteorder="big")

    uuid_bytes = ts_bytes + rand_a_bytes + rand_b_bytes
    return str(uuid.UUID(bytes=uuid_bytes))
