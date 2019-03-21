this.aesCbcPkcs7EncryptBytes = (function script() {
  "use strict";

  /*! aesCbcPkcs7EncryptBytes.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function aesCbcPkcs7EncryptBytes(bytes, key, iv) {
    // pad with PKCS#7

    // bytes = [..]
    //   an array of uint8
    // key = [..]
    //   an array of 4/6/8 int32
    // iv = [..]
    //   an array of 4 int32

    function memcpy(as, is, ad, id, l) {
      while (l--) ad[id + l] = as[is + l];
      return ad;
    }

    function encode16BytesTo4Int32(bytes) {  // big endian
      return [
        decodeBigEndianBytesToInt32(bytes.slice(0, 4)),
        decodeBigEndianBytesToInt32(bytes.slice(4, 8)),
        decodeBigEndianBytesToInt32(bytes.slice(8, 12)),
        decodeBigEndianBytesToInt32(bytes.slice(12, 16))
      ];
    }
    function decode4Int32To16Bytes(block) {  // big endian
      return encodeInt32ToBigEndianBytes(block[0])
        .concat(encodeInt32ToBigEndianBytes(block[1]))
        .concat(encodeInt32ToBigEndianBytes(block[2]))
        .concat(encodeInt32ToBigEndianBytes(block[3]));
    }

    var cipherBytes = [], aes = new Aes(key),
        block = null, n = 16, i = 0;

    if (bytes.length % 16) n = (16 - (bytes.length % 16));

    bytes = memcpy(bytes, 0, new Array(bytes.length + n), 0, bytes.length);
    i = bytes.length - n; while (i < bytes.length) bytes[i++] = n;
    // OR
    //block = new Array(n);
    //while (i < block.length) block[i++] = n;
    //bytes = bytes.concat(block);

    for (i = 0; i < bytes.length; i += 16) {
      block = encode16BytesTo4Int32(bytes.slice(i, i + 16));
      block = block.map((v, ii) => v ^ iv[ii]);
      cipherBytes = cipherBytes.concat(decode4Int32To16Bytes(iv = aes.encrypt(block)));
    }
    return cipherBytes;
  }
  aesCbcPkcs7EncryptBytes.toScript = function () { return "(" + script.toString() + "())"; };
  aesCbcPkcs7EncryptBytes._requiredGlobals = [
    "Aes",
    "decodeBigEndianBytesToInt32",
    "encodeInt32ToBigEndianBytes"
  ];
  return aesCbcPkcs7EncryptBytes;

}());
