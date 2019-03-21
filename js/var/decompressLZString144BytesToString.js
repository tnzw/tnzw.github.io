this.decompressLZString144BytesToString = (function script() {
  "use strict";

  /*! decompressLZString144BytesToString.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decompressLZString144BytesToString(bytes) {
    // XXX expand bytes to text, then decompress
    var text = "", i = 0;
    for (; i < bytes.length; i += 2)
      text += String.fromCharCode(bytes[i] | (bytes[i + 1] << 8));
    return LZString144.decompress(text);
  }
  decompressLZString144BytesToString.toScript = function () { return "(" + script.toString() + "())"; };
  decompressLZString144BytesToString._requiredGlobals = ["LZString144"];
  return decompressLZString144BytesToString;

}());
