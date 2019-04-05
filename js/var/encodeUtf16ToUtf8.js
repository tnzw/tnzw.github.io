this.encodeUtf16ToUtf8 = (function script() {
  "use strict";

  /*! encodeUtf16ToUtf8.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeUtf16ToUtf8(utf16Codes) {
    // XXX do documentation

    // utf16Codes = [...]
    //   an array of utf16 codes (uint16)
    // returns an array of utf8 codes (uint8)

    var cont = true, e, ee = [], i = 0, ei = 0, cache = [], utf8Codes = [];
    while (cont) {
      cont = false;
      encodeUtf16ToUtf8ChunkAlgorithm(utf16Codes, i, utf16Codes.length, utf8Codes, ee, cache, true);
      if ((e = ee[ei++]) !== undefined) {
        switch (e.errno) {
          case 1:  // invalid continuation code
            i = e.index;
            utf8Codes.push(0xEF, 0xBF, 0xBD);
            cache = [];
            break;
          case 2:  // invalid start code
          case 3:  // unexpected end of data
            i = e.index + 1;
            utf8Codes.push(0xEF, 0xBF, 0xBD);
            break;
          default:
            throw new Error("unhandled errno " + e.errno);
        }
        cont = i < utf16Codes.length;
      }
    }
    return utf8Codes;
  }
  encodeUtf16ToUtf8.toScript = function () { return "(" + script.toString() + "())"; };
  encodeUtf16ToUtf8._requiredGlobals = ["encodeUtf16ToUtf8ChunkAlgorithm"];
  return encodeUtf16ToUtf8;

}());
