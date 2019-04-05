this.encodeCodePointsToUtf8 = (function script() {
  "use strict";

  /*! encodeCodePointsToUtf8.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointsToUtf8(codePoints) {
    // XXX do documentation

    // codePoints = [...]
    //   an array of code points (uint32)
    // returns an array of utf8 codes (uint8)

    var i = 0, l = codePoints.length, code, b, c, d, utf8Codes = [];
    for (; i < l; i += 1) {
      if ((code = codePoints[i]) <= 0x7F) utf8Codes.push(code);
      else if (code <= 0x7FF) {
        b = 0x80 | (code & 0x3F); code >>>= 6;
        utf8Codes.push(0xC0 | (code & 0x1F), b); // a = (0x1E << (6 - 1)) | (code & (0x3F >> 1));
      // } else if (0xD800 <= code && code <= 0xDFFF) accept reserved code points (like in chrome)
      } else if (code <= 0xFFFF) {
        c = 0x80 | (code & 0x3F); code >>>= 6;
        b = 0x80 | (code & 0x3F); code >>>= 6;
        utf8Codes.push(0xE0 | (code & 0xF), b, c); // a = (0x1E << (6 - 2)) | (code & (0x3F >> 2));
      } else if (code <= 0x10FFFF) {
        d = 0x80 | (code & 0x3F); code >>>= 6;
        c = 0x80 | (code & 0x3F); code >>>= 6;
        b = 0x80 | (code & 0x3F); code >>>= 6;
        utf8Codes.push(0xF0 | (code & 0x7), b, c, d); // a = (0x1E << (6 - 3)) | (code & (0x3F >> 3));
      } else utf8Codes.push(0xEF, 0xBF, 0xBD);  // push code point error
    }
    return utf8Codes;
  }
  encodeCodePointsToUtf8.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeCodePointsToUtf8;

}());

