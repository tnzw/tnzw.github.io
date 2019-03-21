(function script(global) {
  "use strict";

  /*! encodeCodePointsToUtf16ChunkAlgorithm.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointsToUtf16ChunkAlgorithm(codePoints, i, l, utf16Codes, allowReservedCodePoints, events) {
    // XXX do documentation

    // codePoints = [...]
    //   an array of code points (uint32)
    // i (from) = 0
    //   from which index to start reading codePoints
    // l (to) = codePoints.length
    //   from which index to stop reading codePoints
    // utf16Codes = []
    //   where the utf16 codes (uint16) are pushed
    // allowReservedCodePoints = false
    //   whether to ignore reserved code points or not
    // events = []
    //   where the error events are pushed
    // returns utf16Codes

    // events :
    //   error
    //     reserved code point, errno 1 (if > U+D800 & < U+DFFF)
    //     invalid code point, errno 2 (if > U+10FFFF)

    var code;
    for (; i < l; i += 1) {
      code = codePoints[i];
      if (code <= 0xD7FF) utf16Codes.push(code);
      else if (!allowReservedCodePoints && code <= 0xDFFF) { events.push({type: "error", message: "reserved code point", errno: 1, index: i}); return utf16Codes; }
      else if (code <= 0xFFFF) utf16Codes.push(code);
      else if (code <= 0x10FFFF) {  // surrogate pair
        code -= 0x10000;
        utf16Codes.push(0xD800 + ((code >>> 10) & 0x3FF), 0xDC00 + (code & 0x3FF));
      } else { events.push({type: "error", message: "invalid code point", errno: 2, index: i}); return utf16Codes; }
    }
    return utf16Codes;
  }
  global.encodeCodePointsToUtf16ChunkAlgorithm = encodeCodePointsToUtf16ChunkAlgorithm;

}(this));

