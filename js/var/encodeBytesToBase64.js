this.encodeBytesToBase64 = (function script() {
  "use strict";

  /*! encodeBytesToBase64.js Version 0.1.7

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeBytesToBase64(bytes) {
    return encodeBytesToBase64CodesChunkAlgorithm(bytes, 0, bytes.length, [], "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", [0, 0], true).join("");
  }
  encodeBytesToBase64.toScript = function () { return "(" + script.toString() + "())"; };
  encodeBytesToBase64._requiredGlobals = ["encodeBytesToBase64CodesChunkAlgorithm"];
  return encodeBytesToBase64;

}());

