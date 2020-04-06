# md5_as4uint32_sumbytes.py Version 1.0.1
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def md5_as4uint32_sumbytes(bytes_data):
  # Note: All variables are unsigned 32 bit and wrap modulo 2^32 when calculating

  # s specifies the per-round shift amounts
  s = (
    7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
    5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
    4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
    6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
  )
  # Use binary integer part of the sines of integers (Radians) as constants:
  # for i from 0 to 63
  #     K[i] := floor(232 × abs(sin(i + 1)))
  # end for
  # (Or just use the following precomputed table):
  K = (
    0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
    0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
    0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
    0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
    0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
    0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
    0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
    0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
    0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
    0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
    0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
    0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
    0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
    0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
    0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
    0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
  )

  # Initialize variables:
  a0 = 0x67452301
  b0 = 0xefcdab89
  c0 = 0x98badcfe
  d0 = 0x10325476

  # Pre-processing: adding a single 1 bit
  # append "1" bit to message
  # Notice: the input bytes are considered as bits strings,
  #  where the first bit is the most significant bit of the byte.[48]

  # Pre-processing: padding with zeros
  # append "0" bit until message length in bits ≡ 448 (mod 512)
  # append original length in bits mod 2**64 to message

  def iter_with_md5_padding(iterable):
    L = 0
    for _ in iterable:
      yield _
      L += 1
    yield 0x80
    p = L + 1
    while p % 64 != 56:
      yield 0
      p += 1
    for _ in uint64_littleendian_tobytes((L*8)%0x10000000000000000):  # (L*8)%(2**64)
      yield _

  def iter_block(iterable, block_size):
    block = [None]*block_size
    i = 0
    for _ in iterable:
      block[i] = _
      i += 1
      if i == block_size:
        yield block
        i = 0

  def transcode_uint8_to_uint32_littleendian(bytes_data):
    return [uint32_littleendian_frombytes(_) for _ in iter_block(bytes_data, 4)]

  # Process the message in successive 512-bit chunks:
  # for each 512-bit chunk of padded message
  for chunk in iter_block(iter_with_md5_padding(bytes_data), 64):
    #     break chunk into sixteen 32-bit words M[j], 0 ≤ j ≤ 15
    M = transcode_uint8_to_uint32_littleendian(chunk)

    # Initialize hash value for this chunk:
    a = a0
    b = b0
    c = c0
    d = d0

    # Main loop:
    #    for i from 0 to 63
    for i in range(64):
      #        var int F, g
      if i < 16:
        #        if 0 ≤ i ≤ 15 then
        #            F := (B and C) or ((not B) and D)
        f = (b & c) | ((~b) & d)
        #            g := i
        g = i
      elif i < 32:
        #        else if 16 ≤ i ≤ 31
        #            F := (D and B) or ((not D) and C)
        f = (d & b) | ((~d) & c);
        #            g := (5×i + 1) mod 16
        g = ((5 * i) + 1) % 16
      elif i < 48:
        #        else if 32 ≤ i ≤ 47
        #            F := B xor C xor D
        f = b ^ c ^ d;
        #            g := (3×i + 5) mod 16
        g = ((3 * i) + 5) % 16
      else:
        #        else if 48 ≤ i ≤ 63
        #            F := C xor (B or (not D))
        f = c ^ (b | (~d))
        #            g := (7×i) mod 16
        g = ((7 * i) % 16)
      # Be wary of the below definitions of a,b,c,d
      f = (f + a + K[i] + M[g]) & 0xFFFFFFFF
      a = d
      d = c
      c = b
      b = (b + uint32_rotateleft(f, s[i])) & 0xFFFFFFFF
    # Add this chunk's hash to result so far:
    a0 = (a0 + a) & 0xFFFFFFFF
    b0 = (b0 + b) & 0xFFFFFFFF
    c0 = (c0 + c) & 0xFFFFFFFF
    d0 = (d0 + d) & 0xFFFFFFFF

  #var char digest[16] := a0 append b0 append c0 append d0 //(Output is in little-endian)
  return a0, b0, c0, d0
md5_as4uint32_sumbytes._required_globals = [
  "uint32_littleendian_frombytes",
  "uint64_littleendian_tobytes",
  "uint32_rotateleft",
]
