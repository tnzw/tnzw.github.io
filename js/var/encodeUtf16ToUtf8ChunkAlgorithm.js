this.encodeUtf16ToUtf8ChunkAlgorithm = (function script() {
  "use strict";

  /*! encodeUtf16ToUtf8ChunkAlgorithm.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeUtf16ToUtf8ChunkAlgorithm(utf16Codes, i, l, utf8Codes, events, cache, close) {
    // XXX do documentation

    // utf16Codes = [...]
    //   an array of utf16 codes (uint16)
    // i (from) = 0
    //   from which index to start reading utf16Codes
    // l (to) = utf16Codes.length
    //   from which index to stop reading utf16Codes
    // utf8Codes = []
    //   where the utf8 codes (uint8) are pushed
    // events = []
    //   where the error events are pushed
    // cache = []
    //   used by the algorithm
    // close = false (optional)
    //   tells the algorithm to close the stream
    // returns utf8Codes

    // events :
    //   error
    //     invalid continuation code, errno 1
    //     invalid start code, errno 2
    //     unexpected end of data, errno 3

    var c, c1;
    for (; i < l; i += 1) {
      c = utf16Codes[i];
      if (cache.length) {
        if (0xdc00 <= c && c <= 0xdfff) {
          c1 = cache[0];
          c1 = ((c1 - 0xd800) << 10) + (c - 0xdc00) + 0x10000;
          utf8Codes.push((c1 >> 18) | 0xf0, ((c1 >> 12) & 0x3f) | 0x80, ((c1 >> 6) & 0x3f) | 0x80, (c1 & 0x3f) | 0x80);
          cache.shift();
        } else { events.push({type: "error", message: "invalid continuation code", errno: 1, index: i}); return utf8Codes; }
      } else if (c <= 0x7F) utf8Codes.push(c);
      else if (c <= 0x7FF) utf8Codes.push((c >> 6) | 0xc0, (c & 0x3f) | 0x80);
      else if (0xd800 <= c && c <= 0xdbff) cache[0] = c;
      else if (0xdc00 <= c && c <= 0xdfff) { events.push({type: "error", message: "invalid start code", errno: 2, index: i}); return utf8Codes; }
      else utf8Codes.push(((c >> 12) & 0xf) | 0xe0, ((c >> 6) & 0x3f) | 0x80, (c & 0x3f) | 0x80);
    }
    if (close && cache.length) { events.push({type: "error", message: "unexpected end of data", errno: 3, index: i}); return utf8Codes; }
    return utf8Codes;
  }
  encodeUtf16ToUtf8ChunkAlgorithm.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeUtf16ToUtf8ChunkAlgorithm;

}());
