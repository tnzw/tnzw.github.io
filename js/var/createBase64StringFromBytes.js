this.createBase64StringFromBytes = (function script() {
  "use strict";

  /*! createBase64StringFromBytes.js Version 1.0.0

      Copyright (c) 2015-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createBase64StringFromBytes(bytes) {
    return encodeBytesToBase64CodesChunkAlgorithm(bytes, 0, bytes.length, [], "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", [0, 0], true).join("");
  }

  createBase64StringFromBytes.toScript = function () { return "(" + script.toString() + "())"; };
  createBase64StringFromBytes._requiredGlobals = ["encodeBytesToBase64CodesChunkAlgorithm"];
  return createBase64StringFromBytes;

}());
