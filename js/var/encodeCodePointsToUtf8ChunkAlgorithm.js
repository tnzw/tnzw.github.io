this.encodeCodePointsToUtf8ChunkAlgorithm = (function script() {
  "use strict";

  /*! encodeCodePointsToUtf8ChunkAlgorithm.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointsToUtf8ChunkAlgorithm(codePoints, i, l, utf8Codes, allowReservedCodePoints, events) {
    // XXX do documentation

    // codePoints = [...]
    //   an array of code points (uint32)
    // i (from) = 0
    //   from which index to start reading codePoints
    // l (to) = codePoints.length
    //   from which index to stop reading codePoints
    // utf8Codes = []
    //   where the utf8 codes (uint8) are pushed
    // allowReservedCodePoints = false
    //   whether to ignore reserved code points or not
    // events = []
    //   where the error events are pushed
    // returns utf8Codes

    // events :
    //   error
    //     reserved code point, errno 1 (if > U+D800 & < U+DFFF)
    //     invalid code point, errno 2 (if > U+10FFFF)

    var code, b, c, d;
    for (; i < l; i += 1) {
      if ((code = codePoints[i]) <= 0x7F) utf8Codes.push(code);
      else if (code <= 0x7FF) {
        b = 0x80 | (code & 0x3F); code >>>= 6;
        utf8Codes.push(0xC0 | (code & 0x1F), b); // a = (0x1E << (6 - 1)) | (code & (0x3F >> 1));
      } else if (!allowReservedCodePoints && 0xD800 <= code && code <= 0xDFFF) { events.push({type: "error", message: "reserved code point", errno: 1, index: i}); return utf8Codes; }
      else if (code <= 0xFFFF) {
        c = 0x80 | (code & 0x3F); code >>>= 6;
        b = 0x80 | (code & 0x3F); code >>>= 6;
        utf8Codes.push(0xE0 | (code & 0xF), b, c); // a = (0x1E << (6 - 2)) | (code & (0x3F >> 2));
      } else if (code <= 0x10FFFF) {
        d = 0x80 | (code & 0x3F); code >>>= 6;
        c = 0x80 | (code & 0x3F); code >>>= 6;
        b = 0x80 | (code & 0x3F); code >>>= 6;
        utf8Codes.push(0xF0 | (code & 0x7), b, c, d); // a = (0x1E << (6 - 3)) | (code & (0x3F >> 3));
      } else { events.push({type: "error", message: "invalid code point", errno: 2, index: i}); return utf8Codes; }
    }
    return utf8Codes;
  }
  encodeCodePointsToUtf8ChunkAlgorithm.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeCodePointsToUtf8ChunkAlgorithm;

}());
