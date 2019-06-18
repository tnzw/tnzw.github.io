this.OPENSSL_EVP_BytesToKey = (function script() {
  "use strict";

  /*! OPENSSL_EVP_BytesToKey.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function OPENSSL_EVP_BytesToKey(hash, nhash, salt, password, count, key, ksize, iv, vsize) {
    // Original API : EVP_BytesToKey(hash, nhash, salt, data, dlen, count, key, ksize, iv, vsize)

    // https://stackoverflow.com/questions/9488919/password-to-key-function-compatible-with-openssl-commands
    // https://www.cryptopp.com/wiki/OPENSSL_EVP_BytesToKey

    // OPENSSL_EVP_BytesToKey(sumBytesToMd5Bytes, 16, null, encode("secret"), 1, k = new Uint8Array(32), 32, iv = new Uint8Array(16), 16);

    // see: openssl aes-256-cbc -nosalt -pass pass:b -P
    // openssl behavior -> nosalt with pass:b -> key=92eb5ffee6ae2fec3ad71c777531578f0de6129ea1427f7c2019d1c92ef7ef18 (nBits = 256), iv=0e9ecec7b878862e2df9f1731e96071c (128 bits)
    // openssl behavior -> nosalt with pass:c -> key=4a8a08f09d37b73795649038408b5f332e3d865650e0a9c3f2e75b6ad415fb95 (nBits = 256), iv=dacc5c7b132585205f74a5d5ee9d3526 (128 bits)

    // salt should be an array of 8 bytes or null

    // OpenSSL 1.1.0 changed the digest algorithm used in some internal components.
    // Formerly, MD5 was used, and 1.1.0c switched to SHA256. Be careful the change
    // is not affecting you in both EVP_BytesToKey and commands like openssl enc.

    // OPENSSL_EVP_BytesToKey(sumBytesToSha256Bytes, 32, null, encode("secret"), 1, k = new Uint8Array(32), 32, iv = new Uint8Array(16), 16);

    var nkey = ksize, niv = vsize,
        addmd = 0, i = 1, ki = 0, vi = 0,
        update = null, digest = null;
    for (;;) {
      update = [];
      if (addmd++)
        update.push.apply(update, digest);
      update.push.apply(update, password);
      if (salt)
        update.push.apply(update, salt);
      digest = hash(update);
      for (i = 1; i < count; i += 1)
        digest = hash(digest);
      i = 0;
      if (nkey) {
        for (;;) {
          if (nkey === 0) break;
          if (i === nhash) break;
          if (key)
            key[ki++] = digest[i];
          nkey--;
          i++;
        }
      }
      if (niv && (i !== nhash)) {
        for (;;) {
          if (niv === 0) break;
          if (i === nhash) break;
          if (iv)
            iv[vi++] = digest[i];
          niv--;
          i++;
        }
      }
      if (nkey === 0 && niv === 0) break;
    }
    return ksize;
  }
  OPENSSL_EVP_BytesToKey.toScript = function () { return "(" + script.toString() + "())"; };
  return OPENSSL_EVP_BytesToKey;

}());
