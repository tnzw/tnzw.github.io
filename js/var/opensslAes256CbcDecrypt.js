this.opensslAes256CbcDecrypt = (function script() {
  "use strict";

  /*! opensslAes256CbcDecrypt.js Version 1.1.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function opensslAes256CbcDecrypt(ciphered, password, withSalt, desiredIv) {

    // ciphered = [uint8..]
    // password = "" or [uint8..]
    // withSalt = boolean  (optional)
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

    var key = new Array(32), iv = new Array(16), salt = null, n = 0, i = 1;
    if (typeof password === "string") password = new TextEncoder().encode(password);
    if (withSalt === undefined) { if(new TextDecoder().decode(new Uint8Array(ciphered.slice(0, 8))) === "Salted__") salt = ciphered.slice(8, 16); }
    else if (withSalt) { if(new TextDecoder().decode(new Uint8Array(ciphered.slice(0, 8))) === "Salted__") salt = ciphered.slice(8, 16); else return null; }
    //OPENSSL_EVP_BytesToKey(sumBytesToSha256Bytes, 32, salt, password, 1, key, 32, iv, 16);
    OPENSSL_EVP_BytesToKey(sumBytesToMd5Bytes, 16, salt, password, 1, key, 32, iv, 16);
    if (salt) return aesCbcPkcs7DecryptBytes(ciphered.slice(16), encode32BytesTo8Int32(key), encode16BytesTo4Int32(desiredIv === undefined ? iv : desiredIv));
    return aesCbcPkcs7DecryptBytes(ciphered, encode32BytesTo8Int32(key), encode16BytesTo4Int32(desiredIv === undefined ? iv : desiredIv));
  }
  opensslAes256CbcDecrypt.toScript = function () { return "(" + script.toString() + "())"; };
  opensslAes256CbcDecrypt._requiredGlobals = [
    "TextEncoder",
    "TextDecoder",
    "OPENSSL_EVP_BytesToKey",
    "sumBytesToMd5Bytes",
    "aesCbcPkcs7DecryptBytes"
  ];
  return opensslAes256CbcDecrypt;

}());
