this.encodeStringToLatin1Codes = (function script() {
  "use strict";

  /*! encodeStringToLatin1Codes.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeStringToLatin1Codes(text) {
    // XXX do documentation
    var i = 0, l = text.length, latin1Codes = new Array(l), c = 0;
    for (; i < l; i += 1) {
      c = text.charCodeAt(i);
      // 0x3F = "?"
      latin1Codes[i] = c > 0xFF ? 0x3F : c;
    }
    return latin1Codes;
  }
  encodeStringToLatin1Codes.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeStringToLatin1Codes;

}());
