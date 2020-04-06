# Aes.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

class Aes(object):

  _tables = []

  def __init__(self, key):
    """\
Aes([uint32]*4)
Aes([uint32]*6)
Aes([uint32]*8)
"""
    if not self._tables:
      Aes._precompute()

    sbox = self._tables[0][4]
    decTable = self._tables[1]
    keyLen = len(key)
    rcon = 1

    if keyLen != 4 and keyLen != 6 and keyLen != 8:
      raise ValueError("invalid aes key size")

    encKey = [0] * (4 * keyLen + 28)
    encKey[:keyLen] = key
    decKey = [0] * (4 * keyLen + 28)
    self._key = [encKey, decKey]

    # schedule encryption keys
    for i in range(keyLen, 4 * keyLen + 28):
      tmp = encKey[i-1]

      # apply sbox
      if i%keyLen == 0 or (keyLen == 8 and i%keyLen == 4):
        tmp = sbox[tmp>>24]<<24 ^ \
          sbox[tmp>>16&255]<<16 ^ \
          sbox[tmp>>8&255]<<8 ^   \
          sbox[tmp&255]
        #if tmp > MAX_UINT32: raise RuntimeError("tmp > MAX_UINT32")

        # shift rows and add rcon
        if i%keyLen == 0:
          #tmp = tmp<<8 ^ tmp>>24 ^ rcon<<24
          tmp = (tmp<<8)&0xFFFFFFFF ^ tmp>>24 ^ (rcon<<24)&0xFFFFFFFF
          rcon = rcon<<1 ^ (rcon>>7)*283
          #if rcon > MAX_UINT32: raise RuntimeError("rcon > MAX_UINT32")

      encKey[i] = encKey[i-keyLen] ^ tmp

    # schedule decryption keys
    for j, i in enumerate(range(4 * keyLen + 28, 0, -1)):
      tmp = encKey[i if j&3 else i - 4]
      if i<=4 or j<4:
        decKey[j] = tmp
      else:
        decKey[j] = decTable[0][sbox[tmp>>24       ]] ^ \
                    decTable[1][sbox[tmp>>16  & 255]] ^ \
                    decTable[2][sbox[tmp>>8   & 255]] ^ \
                    decTable[3][sbox[tmp      & 255]]

  def encrypt(self, block):
    "enciphered_4uint32 = aes.encrypt([uint32]*4)"
    return self._crypt(block, 0)

  def decrypt(self, block):
    "deciphered_4uint32 = aes.decrypt([uint32]*4)"
    return self._crypt(block, 1)

  @staticmethod
  def _precompute():
    #Aes._tables[:] = [[[],[],[],[],[]],[[],[],[],[],[]]]
    Aes._tables[:] = [[[None]*256,[None]*256,[None]*256,[None]*256,[None]*256],[[None]*256,[None]*256,[None]*256,[None]*256,[None]*256]]
    encTable, decTable = Aes._tables[0], Aes._tables[1]
    sbox, sboxInv = encTable[4], decTable[4]
    d, th = [None]*256, [None]*256

    # Compute double and third tables
    for i in range(256):
      d[i] = i<<1 ^ (i>>7)*283
      th[d[i] ^ i] = i

    x = xInv = 0
    while not sbox[x]:
      # Compute sbox
      s = xInv ^ xInv<<1 ^ xInv<<2 ^ xInv<<3 ^ xInv<<4
      s = s>>8 ^ s&255 ^ 99
      sbox[x] = s
      sboxInv[s] = x

      # Compute MixColumns
      x2 = d[x]
      x4 = d[x2]
      x8 = d[x4]
      tDec = x8*0x1010101 ^ x4*0x10001 ^ x2*0x101 ^ x*0x1010100
      tEnc = d[s]*0x101 ^ s*0x1010100

      for i in range(4):
        #encTable[i][x] = tEnc = tEnc<<24 ^ tEnc>>8
        #decTable[i][s] = tDec = tDec<<24 ^ tDec>>8
        encTable[i][x] = tEnc = (tEnc<<24)&0xFFFFFFFF ^ tEnc>>8
        decTable[i][s] = tDec = (tDec<<24)&0xFFFFFFFF ^ tDec>>8

      x ^= x2 or 1
      xInv = th[xInv] or 1

  def _crypt(self, input, dir):
    #print(input)
    if len(input) != 4:
      raise ValueError("invalid aes block size")

    key = self._key[dir]
    # state variables a,b,c,d are loaded with pre-whitened data
    a = input[0]               ^ key[0]
    b = input[3 if dir else 1] ^ key[1]
    c = input[2]               ^ key[2]
    d = input[1 if dir else 3] ^ key[3]

    nInnerRounds = len(key)//4 - 2
    kIndex = 4
    out = [0,0,0,0]
    table = self._tables[dir]

    # load up the tables
    t0    = table[0]
    t1    = table[1]
    t2    = table[2]
    t3    = table[3]
    sbox  = table[4]

    # Inner rounds.  Cribbed from OpenSSL.
    for i in range(nInnerRounds):
      a2 = t0[a>>24] ^ t1[b>>16 & 255] ^ t2[c>>8 & 255] ^ t3[d & 255] ^ key[kIndex]
      b2 = t0[b>>24] ^ t1[c>>16 & 255] ^ t2[d>>8 & 255] ^ t3[a & 255] ^ key[kIndex + 1]
      c2 = t0[c>>24] ^ t1[d>>16 & 255] ^ t2[a>>8 & 255] ^ t3[b & 255] ^ key[kIndex + 2]
      d  = t0[d>>24] ^ t1[a>>16 & 255] ^ t2[b>>8 & 255] ^ t3[c & 255] ^ key[kIndex + 3]
      kIndex += 4
      a=a2
      b=b2
      c=c2

    # Last round.
    for i in range(4):
      #out[3&-i if dir else i] =  \
      #  sbox[a>>24       ]<<24 ^ \
      #  sbox[b>>16  & 255]<<16 ^ \
      #  sbox[c>>8   & 255]<<8  ^ \
      #  sbox[d      & 255]     ^ \
      #  key[kIndex]
      out[3&-i if dir else i] =              \
        (sbox[a>>24      ]<<24)&0xFFFFFFFF ^ \
        (sbox[b>>16 & 255]<<16)&0xFFFFFFFF ^ \
        (sbox[c>> 8 & 255]<< 8)&0xFFFFFFFF ^ \
         sbox[d     & 255]                 ^ \
        key[kIndex]
      kIndex += 1
      a2=a
      a=b
      b=c
      c=d
      d=a2

    #print(out)
    return out
