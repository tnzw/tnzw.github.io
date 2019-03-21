(function (global) {
  "use strict";

  /*! encodeBytesToBase64Bytes.js Version 0.1.7

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  //importScriptsAsync("encodeBytesToBase64CodesChunkAlgorithm.js");

  function encodeBytesToBase64Bytes(bytes) {
    return encodeBytesToBase64CodesChunkAlgorithm(bytes, 0, bytes.length, [], [
      65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,  // A-Z
      97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122, // a-z
      48,49,50,51,52,53,54,55,56,57,  // 0-9
      43,47,  // standard way
      //45,95,  // url way
      61  // padding value
      // built by `parseBase64SchemeForEncoding("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")`
    ], [0, 0], true);
  }
  global.encodeBytesToBase64Bytes = encodeBytesToBase64Bytes;
  encodeBytesToBase64Bytes._requiredGlobals = ["encodeBytesToBase64CodesChunkAlgorithm"];

}(this));

