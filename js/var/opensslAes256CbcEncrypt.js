this.opensslAes256CbcEncrypt = (function script() {
  "use strict";

  /*! opensslAes256CbcEncrypt.js Version 1.1.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function opensslAes256CbcEncrypt(message, password, desiredSalt, desiredIv) {

    // message = "" or [uint8..]
    // password = "" or [uint8..]
    // desiredSalt = null or [uint8 x8]  (optional)
    // desiredIv = null or [uint8 x16]  (optional)

    function encode32BytesTo8Int32(block) {  // big endian
      return [
        decodeBigEndianBytesToInt32(block.slice(0, 4)),
        decodeBigEndianBytesToInt32(block.slice(4, 8)),
        decodeBigEndianBytesToInt32(block.slice(8, 12)),
        decodeBigEndianBytesToInt32(block.slice(12, 16)),
        decodeBigEndianBytesToInt32(block.slice(16, 20)),
        decodeBigEndianBytesToInt32(block.slice(20, 24)),
        decodeBigEndianBytesToInt32(block.slice(24, 28)),
        decodeBigEndianBytesToInt32(block.slice(28, 32))
      ];
    }
    function encode16BytesTo4Int32(bytes) {  // big endian
      return [
        decodeBigEndianBytesToInt32(bytes.slice(0, 4)),
        decodeBigEndianBytesToInt32(bytes.slice(4, 8)),
        decodeBigEndianBytesToInt32(bytes.slice(8, 12)),
        decodeBigEndianBytesToInt32(bytes.slice(12, 16))
      ];
    }

    var i = 0, j = 0, result = null,
        key = new Array(32), iv = new Array(16),
        salt = desiredSalt === undefined ? crypto.getRandomValues(new Uint8Array(8)) : desiredSalt;
    //    salt = [0,0,0,0,0,0,0,0].map(_=>Math.floor(Math.random() * 0xFF));
    if (typeof message === "string") message = new TextEncoder().encode(message);
    if (typeof password === "string") password = new TextEncoder().encode(password);
    //OPENSSL_EVP_BytesToKey(sumBytesToSha256Bytes, 32, salt, password, 1, key, 32, iv, 16);
    OPENSSL_EVP_BytesToKey(sumBytesToMd5Bytes, 16, salt, password, 1, key, 32, iv, 16);
    message = aesCbcPkcs7EncryptBytes(message, encode32BytesTo8Int32(key), encode16BytesTo4Int32(desiredIv === undefined ? iv : desiredIv));
    if (message === null) return null;
    if (desiredSalt === null) return message;
    //return encodeStringToUtf8("Salted__").concat(salt).concat(message);  // bad if salt is Uint8Array
    result = new Array(8 + salt.length + message.length);
    while (j < 8) result[i++] = "Salted__".charCodeAt(j++);
    j = 0; while (j < salt.length) result[i++] = salt[j++];
    j = 0; while (j < message.length) result[i++] = message[j++];
    return result;
  }
  opensslAes256CbcEncrypt.toScript = function () { return "(" + script.toString() + "())"; };
  opensslAes256CbcEncrypt._requiredGlobals = [
    "TextEncoder",
    "OPENSSL_EVP_BytesToKey",
    "sumBytesToMd5Bytes",
    "aesCbcPkcs7EncryptBytes",
    "decodeBigEndianBytesToInt32"
  ];
  return opensslAes256CbcEncrypt;

}());
