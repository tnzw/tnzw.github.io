this.decodeUtf8ToCodePointsChunkAlgorithm = (function script() {
  "use strict";

  /*! decodeUtf8ToCodePointsChunkAlgorithm.js Version 0.1.36

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeUtf8ToCodePointsChunkAlgorithm(utf8Codes, i, l, codePoints, allowOverlongEncoding, events, cache, close) {
    // XXX do documentation

    // utf8Codes = [...]
    //   an array of utf8 codes (uint8)
    // i XXX
    // l XXX
    // codePoints = []
    //   where the code points (uint32) are pushed
    // allowOverlongEncoding = true
    //   allow overlong encoding error detection
    // cache = [state, utf8Codes...x4]
    //   used by the algorithm
    // events = []
    //   where the error events are pushed
    // close = false
    //   tells the algorithm to close the stream
    // returns codePoints

    // events :
    //   error
    //     invalid start byte, errno 1
    //     invalid continuation byte, errno 2
    //     overlong encoding, errno 3
    //     reserved code point, errno 4
    //     invalid code point, errno 5
    //     unexpected end of data, errno 6

    var code = 0, c = 0;
    for (; i < l; i += 1) {
      code = utf8Codes[i];
      switch (cache[0]) {
        case 2:
          if ((0xC0 & code) !== 0x80) { events.push({type: "error", message: "invalid continuation byte", errno: 2, length: 2, index: i, requiredUtf8CodeAmount: 2, requiredUtf8CodeIndex: 1}); return codePoints; }
          else { codePoints.push(((cache[1] << 6) | (code & 0x3F)) & 0x7FF); cache[0] = 0; } break;
        case 3:
          if ((0xC0 & code) !== 0x80) { events.push({type: "error", message: "invalid continuation byte", errno: 2, length: 2, index: i, requiredUtf8CodeAmount: 3, requiredUtf8CodeIndex: 1}); return codePoints; }
          else if ((c = cache[1]) === 0xE0 && code <= 0x9F && !allowOverlongEncoding) { events.push({type: "error", message: "overlong encoding", errno: 3, length: 2, index: i, requiredUtf8CodeAmount: 3, requiredUtf8CodeIndex: 1}); return codePoints; }
          else { cache[3] = code; cache[1] = (c << 6) | (code & 0x3F); cache[0] = 31; } break;
        case 31:
          if ((0xC0 & code) !== 0x80) { events.push({type: "error", message: "invalid continuation byte", errno: 2, length: 3, index: i, requiredUtf8CodeAmount: 3, requiredUtf8CodeIndex: 2}); return codePoints; }
          else if (0xD800 <= (c = ((cache[1] << 6) | (code & 0x3F)) & 0xFFFF) && c <= 0xDFFF) { events.push({type: "error", message: "reserved code point", errno: 4, length: 3, index: i, requiredUtf8CodeAmount: 3, requiredUtf8CodeIndex: 2}); return codePoints; }
          else { codePoints.push(c); cache[0] = 0; } break;
        case 4:
          if ((0xC0 & code) !== 0x80) { events.push({type: "error", message: "invalid continuation byte", errno: 2, length: 2, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 1}); return codePoints; }
          else if ((c = cache[1]) === 0xF0 && code <= 0x8F && !allowOverlongEncoding) { events.push({type: "error", message: "overlong encoding", errno: 3, length: 2, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 1}); return codePoints; }
          else { cache[3] = code; cache[1] = (c << 6) | (code & 0x3F); cache[0] = 41; } break;
        case 41:
          if ((0xC0 & code) !== 0x80) { events.push({type: "error", message: "invalid continuation byte", errno: 2, length: 3, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 2}); return codePoints; }
          else { cache[4] = code; cache[1] = (cache[1] << 6) | (code & 0x3F); cache[0] = 42; } break;
        case 42:
          if ((0xC0 & code) !== 0x80) { events.push({type: "error", message: "invalid continuation byte", errno: 2, length: 4, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 3}); return codePoints; }
          else if ((c = ((cache[1] << 6) | (code & 0x3F)) & 0x1FFFFF) > 0x10FFFF) { events.push({type: "error", message: "invalid code point", errno: 5, length: 4, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 3}); return codePoints; }
          else { codePoints.push(c); cache[0] = 0; } break;
        default:
          if (code <= 0x7F) codePoints.push(code);
          else if ((0xE0 & code) === 0xC0) {
            if (code < 0xC2 && !allowOverlongEncoding) { events.push({type: "error", message: "overlong encoding", errno: 3, length: 1, index: i, requiredUtf8CodeAmount: 2, requiredUtf8CodeIndex: 0}); return codePoints; }
            else { cache[2] = cache[1] = code; cache[0] = 2; }
          } else if ((0xF0 & code) === 0xE0) { cache[2] = cache[1] = code; cache[0] = 3; }
          else if ((0xF8 & code) === 0xF0) {
            if (code >= 0xF5) { events.push({type: "error", message: "invalid start byte", errno: 1, length: 1, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 0}); return codePoints; }
            else { cache[2] = cache[1] = code; cache[0] = 4; }
          } else { events.push({type: "error", message: "invalid start byte", errno: 1, length: 1, index: i}); return codePoints; }
      }
    }
    if (close) {
      switch (cache[0]) {
        case 2:  events.push({type: "error", message: "unexpected end of data", errno: 6, length: 2, index: i, requiredUtf8CodeAmount: 2, requiredUtf8CodeIndex: 1}); break;
        case 3:  events.push({type: "error", message: "unexpected end of data", errno: 6, length: 2, index: i, requiredUtf8CodeAmount: 3, requiredUtf8CodeIndex: 1}); break;
        case 31: events.push({type: "error", message: "unexpected end of data", errno: 6, length: 3, index: i, requiredUtf8CodeAmount: 3, requiredUtf8CodeIndex: 2}); break;
        case 4:  events.push({type: "error", message: "unexpected end of data", errno: 6, length: 2, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 1}); break;
        case 41: events.push({type: "error", message: "unexpected end of data", errno: 6, length: 3, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 2}); break;
        case 42: events.push({type: "error", message: "unexpected end of data", errno: 6, length: 4, index: i, requiredUtf8CodeAmount: 4, requiredUtf8CodeIndex: 3}); break;
      }
    }
    return codePoints;
  }
  decodeUtf8ToCodePointsChunkAlgorithm.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeUtf8ToCodePointsChunkAlgorithm;

}());
