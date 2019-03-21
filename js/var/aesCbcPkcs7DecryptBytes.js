this.aesCbcPkcs7DecryptBytes = (function script() {
  "use strict";

  /*! aesCbcPkcs7DecryptBytes.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function aesCbcPkcs7DecryptBytes(bytes, key, iv) {
    // checks PKCS#7 padding

    // bytes = [..]
    //   an array of uint8
    // key = [..]
    //   an array of 4/6/8 int32
    // iv = [..]
    //   an array of 4 int32

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

    var uncipherBytes = [], aes = new Aes(key),
        i = 0, block = null, n = 0;
    if (bytes.length % 16) return null;
    for (i = 0; i < bytes.length; i += 16) {
      block = encode16BytesTo4Int32(bytes.slice(i, i + 16));
      uncipherBytes = uncipherBytes.concat(decode4Int32To16Bytes(aes.decrypt(block).map((v, ii) => v ^ iv[ii])));
      iv = block;
    }
    n = uncipherBytes[uncipherBytes.length - 1];
    if (n > 16 || n === 0) return null;
    i = 1; while (i < n) { if (uncipherBytes[uncipherBytes.length - 1 - (i++)] !== n) return null; }
    return uncipherBytes.slice(0, -n);
  }
  aesCbcPkcs7DecryptBytes.toScript = function () { return "(" + script.toString() + "())"; };
  aesCbcPkcs7DecryptBytes._requiredGlobals = [
    "Aes",
    "decodeBigEndianBytesToInt32",
    "encodeInt32ToBigEndianBytes"
  ];
  return aesCbcPkcs7DecryptBytes;

}());

