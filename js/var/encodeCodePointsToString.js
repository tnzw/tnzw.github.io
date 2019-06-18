this.encodeCodePointsToString = (function script() {
  "use strict";

  /*! encodeCodePointsToString.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointsToString(codePoints) {
    // XXX do documentation
    // quicker than using `String.fromCodePoint.apply(String, codePoints)`
    //   (and 32766 was the amount limit of argument for a function call).
    var i = 0, l = codePoints.length, code, s = "";
    for (; i < l; i += 1) {
      code = codePoints[i];
      //if (0xD800 <= code && code <= 0xDFFF) s += String.fromCharCode(0xFFFD); else
      if (code <= 0xFFFF) s += String.fromCharCode(code);
      else if (code <= 0x10FFFF) {  // surrogate pair
        code -= 0x10000;
        s += String.fromCharCode(0xD800 + ((code >>> 10) & 0x3FF), 0xDC00 + (code & 0x3FF));
      } else throw new Error("Invalid code point " + code);
    }
    return s;
  }
  encodeCodePointsToString.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeCodePointsToString;

}());
