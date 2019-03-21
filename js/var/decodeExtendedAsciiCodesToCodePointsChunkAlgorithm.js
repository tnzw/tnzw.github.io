(function script(global) {
  "use strict";

  /*! decodeExtendedAsciiCodesToCodePointsChunkAlgorithm.js Version 0.1.1

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeExtendedAsciiCodesToCodePointsChunkAlgorithm(extendedAsciiCodes, i, l, codePoints, events) {
    // API stability level: 1 - Experimental

    // XXX do documentation (extended ascii = Windows-1252)

    // extendedAsciiCodes = [...]
    //   an array of us ascii codes (uint8)
    // i or from = 0
    //   from which index to start reading extendedAsciiCodes
    // l or to = extendedAsciiCodes.length
    //   from which index to stop reading extendedAsciiCodes
    // codePoints = []
    //   where the code points (uint32) are pushed
    // events = []
    //   where the error events are pushed
    // returns codePoints

    // events:
    //   error
    //     invalid byte, errno 1

    var code, errorScheme = {  // externalize errorscheme ?
      129:1,141:1,143:1,144:1,157:1
    }, scheme = [  // externalize scheme ?
      0x20AC,0xFFFD,0x201A,0x0192,0x201E,0x2026,0x2020,0x2021, // 0x80-0x87
      0x02C6,0x2030,0x0160,0x2039,0x0152,0xFFFD,0x017D,0xFFFD, // 0x88-0x8F
      0xFFFD,0x2018,0x2019,0x201C,0x201D,0x2022,0x2013,0x2014, // 0x90-0x97
      0x02DC,0x2122,0x0161,0x203A,0x0153,0xFFFD,0x017E,0x0178  // 0x98-0x9F
    ];
    for (; i < l; i += 1) {
      if ((code = extendedAsciiCodes[i]) <= 0x7F) codePoints.push(code);
      else if (errorScheme[code]) { events.push({type: "error", message: "invalid byte", errno: 1, index: i}); return codePoints; }
      else if (code <= 0x9F) codePoints.push(scheme[code - 0x80]);
      else codePoints.push(code);
    }
    return codePoints;
  }
  global.decodeExtendedAsciiCodesToCodePointsChunkAlgorithm = decodeExtendedAsciiCodesToCodePointsChunkAlgorithm;

}(this));
