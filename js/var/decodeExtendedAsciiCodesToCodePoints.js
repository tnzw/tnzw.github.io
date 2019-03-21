this.decodeExtendedAsciiCodesToCodePoints = (function script() {
  "use strict";

  /*! decodeExtendedAsciiCodesToCodePoints.js Version 0.1.1

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeExtendedAsciiCodesToCodePoints(extendedAsciiCodes) {
    // API stability level: 1 - Experimental
    // XXX do documentation (extended ascii = Windows-1252)
    // extendedAsciiCodes = [...]
    //   an array of us ascii codes (uint8)
    // returns an array of code points (uint32)
    var i = 0, l = extendedAsciiCodes.length, codePoints = new Array(l), code, scheme = [
      0x20AC,0xFFFD,0x201A,0x0192,0x201E,0x2026,0x2020,0x2021, // 0x80-0x87
      0x02C6,0x2030,0x0160,0x2039,0x0152,0xFFFD,0x017D,0xFFFD, // 0x88-0x8F
      0xFFFD,0x2018,0x2019,0x201C,0x201D,0x2022,0x2013,0x2014, // 0x90-0x97
      0x02DC,0x2122,0x0161,0x203A,0x0153,0xFFFD,0x017E,0x0178  // 0x98-0x9F
    ];
    for (; i < l; i += 1) {
      if ((code = extendedAsciiCodes[i]) <= 0x7F) codePoints[i] = code;
      else if (code <= 0x9F) codePoints[i] = scheme[code - 0x80];
      else codePoints[i] = code;
    }
    return codePoints;
  }
  decodeExtendedAsciiCodesToCodePoints.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeExtendedAsciiCodesToCodePoints;

}());
