/*jslint indent: 2 */
(function script() {
  "use strict";

  /*! openssl.js version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading openssl.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "opensslAes256CbcDecrypt",
      "opensslAes256CbcEncrypt"
    ).then(script).then(null, function (e) { console.error(e); });
  }
  console.log("running openssl.js tests");

  /*jslint vars: true */
  var info = function () { console.info.apply(console, arguments); };
  var error = function () { console.error.apply(console, arguments); };
  function test(name, timeout, expected, testFn) {
    var res = [], timer;
    function end() {
      if (timer === undefined) return error("test `" + name + "`, `end` called twice");
      timer = clearTimeout(timer);  // timer should be set to undefined
      if (JSON.stringify(res) !== JSON.stringify(expected)) {
        error("test `" + name + "`, result `" + JSON.stringify(res) + "` !== `" + JSON.stringify(expected) + "` expected");
      }
    }
    setTimeout(function () {
      timer = setTimeout(function () {
        try { if (typeof end.onbeforetimeout === "function") end.onbeforetimeout(); }
        catch (e) { error("test: " + name + ", error on before timeout ! `" + e + "`"); }
        if (timer === undefined) return;  // it has ended in before timeout
        error("test `" + name + "`, timeout ! result `" + JSON.stringify(res) + "` <-> `" + JSON.stringify(expected) + "` expected");
      }, timeout);
      try { testFn(res, end); }
      catch (e) { error("test `" + name + "`, error ! result `" + e + "`"); }
    });
  }

  function binaryStringToBytes(bs) {
    var a = new Array(bs.length), i = 0;
    for (; i < bs.length; i += 1) { a[i] = bs.charCodeAt(i); if (a[i] > 0xFF) throw new Error("invalid binaryString"); }
    return a;
  }
  function decodeHexadecimalToBytes(text) {
    var i = 0, bytes = new Array(text.length / 2);
    for (; i < bytes.length; i += 1)
      bytes[i] = parseInt(text.slice((i * 2), (i * 2) + 2), 16);
    return bytes;
  }

  function encrypt(message, password, desiredSalt, desiredIv, expectedBytes) {
    // function opensslAes256CbcEncrypt(message, password[, desiredSalt[, desiredIv]])
    // function opensslAes256CbcDecrypt(ciphered, password[, withSalt[, desiredIv]])
    var name = message;
    if (typeof message === "string") message = binaryStringToBytes(message);
    if (password === undefined) password = message;
    if (typeof desiredSalt === "string") desiredSalt = decodeHexadecimalToBytes(desiredSalt);
    if (typeof desiredIv === "string") desiredIv = decodeHexadecimalToBytes(desiredIv);
    if (typeof expectedBytes === "string") expectedBytes = decodeHexadecimalToBytes(expectedBytes);
    test("openssl " + name, 300, expectedBytes === undefined ? [message] : [expectedBytes, message], function (res, end) {
      var bytes = null;
      try {
        bytes = opensslAes256CbcEncrypt(message, password, desiredSalt, desiredIv);
        if (expectedBytes !== undefined) res.push(bytes);
        res.push(opensslAes256CbcDecrypt(bytes, password, desiredSalt, desiredIv));
      } catch (e) {
        res.push(e.message);
      }
      end();
    });
  }

  function randBytes(length) {
    var r = [], i = 0;
    while (i++ < length) r.push(parseInt(Math.random() * 256, 10));
    return r;
  }

  ///////////
  // tests

  // echo -n a | openssl aes-256-cbc -pass pass:a -S 6161616161616161 -iv 61616161616161616161616161616161 | hexdump -v -e '16/1 "%02x" "\n"'
  encrypt("a", "a",
          "6161616161616161",
          "61616161616161616161616161616161",
          "53616c7465645f5f6161616161616161" +
          "6382092d884dd85da60bba2e30cc6295");
  // echo -n a | openssl aes-256-cbc -pass pass:a -nosalt -iv 61616161616161616161616161616161 | hexdump -v -e '16/1 "%02x" "\n"'
  encrypt("a", "a",
          null,
          "61616161616161616161616161616161",
          "1d8257c833e7bdf4916f210f29b4c135");

  encrypt("a");
  encrypt(randBytes(Math.random() * 200));

}());
