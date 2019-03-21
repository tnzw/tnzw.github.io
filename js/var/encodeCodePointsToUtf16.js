this.encodeCodePointsToUtf16 = (function script() {
  "use strict";

  /*! encodeCodePointsToUtf16.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointsToUtf16(codePoints) {
    // XXX do documentation

    // codePoints = [...]
    //   an array of code points (uint32)
    // returns an array of utf16 codes (uint16)

    var i = 0, l = codePoints.length, code, utf16Codes = [];
    for (; i < l; i += 1) {
      code = codePoints[i];
      //if (code <= 0xD7FF) utf16Codes.push(code);
      //else if (code <= 0xDFFF) accept reserved code points (like in chrome)
      if (code <= 0xFFFF) utf16Codes.push(code);
      else if (code <= 0x10FFFF) {  // surrogate pair
        code -= 0x10000;
        utf16Codes.push(0xD800 + ((code >>> 10) & 0x3FF), 0xDC00 + (code & 0x3FF));
      } else utf16Codes.push(0xFFFD);  // push code point error
    }
    return utf16Codes;
  }
  encodeCodePointsToUtf16.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeCodePointsToUtf16;

}());
