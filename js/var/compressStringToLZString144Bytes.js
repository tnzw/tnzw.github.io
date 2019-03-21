this.compressStringToLZString144Bytes = (function script() {
  "use strict";

  /*! compressStringToLZString144Bytes.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function compressStringToLZString144Bytes(text) {
    // XXX expand text to bytes, and then compress
    text = LZString144.compress(text)
    var bytes = new Array(text.length * 2), i = 0, j = 0, c = 0;
    for (; i < text.length; i += 1) {
      c = text.charCodeAt(i);
      bytes[j++] = c & 0xFF;
      bytes[j++] = c >>> 8;
    }
    return bytes;
  }
  compressStringToLZString144Bytes.toScript = function () { return "(" + script.toString() + "())"; };
  compressStringToLZString144Bytes._requiredGlobals = ["LZString144"];
  return compressStringToLZString144Bytes;

}());
