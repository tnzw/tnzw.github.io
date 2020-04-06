# OPENSSL_EVP_BytesToKey.py Version 1.0.0
# Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def OPENSSL_EVP_BytesToKey(hash, nhash, salt, password, count, key, ksize, iv, vsize):
  """\
Original API : EVP_BytesToKey(hash, nhash, salt, data, dlen, count, key, ksize, iv, vsize)

https://stackoverflow.com/questions/9488919/password-to-key-function-compatible-with-openssl-commands
https://www.cryptopp.com/wiki/OPENSSL_EVP_BytesToKey

k, kl = [uint8] * 32, 32
iv, ivl = [uint8] * 16, 16
OPENSSL_EVP_BytesToKey(md5_sumbytes, 16, None, b"secret", 1, k, kl, iv, ivl);

see: openssl aes-256-cbc -nosalt -pass pass:b -P
openssl behavior -> nosalt with pass:b -> key=92eb5ffee6ae2fec3ad71c777531578f0de6129ea1427f7c2019d1c92ef7ef18 (nBits = 256), iv=0e9ecec7b878862e2df9f1731e96071c (128 bits)
openssl behavior -> nosalt with pass:c -> key=4a8a08f09d37b73795649038408b5f332e3d865650e0a9c3f2e75b6ad415fb95 (nBits = 256), iv=dacc5c7b132585205f74a5d5ee9d3526 (128 bits)

salt should be a list of 8 bytes or None

OpenSSL 1.1.0 changed the digest algorithm used in some internal components.
Formerly, MD5 was used, and 1.1.0c switched to SHA256. Be careful the change
is not affecting you in both EVP_BytesToKey and commands like openssl enc.

k, kl = [uint8] * 32, 32
iv, ivl = [uint8] * 16, 16
OPENSSL_EVP_BytesToKey(sha256_sumbytes, 32, None, b"secret", 1, k, kl, iv, ivl);
"""
  nkey = ksize
  niv = vsize
  addmd = 0
  i = 1
  ki = 0
  vi = 0
  update = b""
  digest = b""
  salt = b"" if salt is None else bytes(salt)
  password = b"" if password is None else bytes(password)
  while 1:
    update = b""
    if addmd: update += digest
    addmd += 1
    update += password
    if salt: update += salt
    digest = bytes(hash(update))
    for i in range(1, count): digest = bytes(hash(digest))
    i = 0;
    if nkey:
      while 1:
        if nkey == 0: break
        if i == nhash: break
        if key:
          key[ki] = digest[i]
          ki += 1
        nkey -= 1
        i += 1
    if niv and i != nhash:
      while 1:
        if niv == 0: break
        if i == nhash: break
        if iv:
          iv[vi] = digest[i]
          vi += 1
        niv -= 1
        i += 1
    if nkey == 0 and niv == 0: break
  return ksize
