this.encodeBytesToBase64CodesChunkAlgorithm = (function script() {
  "use strict";

  /*! encodeBytesToBase64CodesChunkAlgorithm.js Version 0.1.7

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeBytesToBase64CodesChunkAlgorithm(bytes, i, l, codes, schemeCodes, cache, close) {
    // bytes = [...]
    //   array of byte numbers
    // i = 0
    //   from where to start reading bytes
    // l = bytes.length
    //   to where to end reading bytes
    // codes = []
    //   where encoded codes will be written
    // cache = [0, 0]
    //   used by the algorithm
    // schemeCodes = [  // the algorithm assumes it perfect
    //     65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,  // A-Z
    //     97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122, // a-z
    //     48,49,50,51,52,53,54,55,56,57,  // 0-9
    //     43,47,
    //     61  // padding value
    //   ]
    // close = false (optional)
    // returns bytes of encoded base64
    for (; i < l; i += 1) {
      switch (cache[0]) {
        case 2:
          codes.push(schemeCodes[cache[1] | (bytes[i] >>> 4)]);
          cache[1] = (bytes[i] << 2) & 0x3C;
          cache[0] = 3;
          break;
        case 3:
          codes.push(
            schemeCodes[cache[1] | (bytes[i] >>> 6)],
            schemeCodes[bytes[i] & 0x3F]
          );
          cache[0] = 0;
          break;
        default:
          codes.push(schemeCodes[bytes[i] >>> 2]);
          cache[1] = (bytes[i] << 4) & 0x30;
          cache[0] = 2;
      }
    }
    if (close) {
      switch (cache[0]) {
        case 2:
          codes.push(schemeCodes[cache[1]], schemeCodes[64], schemeCodes[64]);
          cache[0] = 0;
          break;
        case 3:
          codes.push(schemeCodes[cache[1]], schemeCodes[64]);
          cache[0] = 0;
      }
    }
    return codes;
  }
  encodeBytesToBase64CodesChunkAlgorithm.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeBytesToBase64CodesChunkAlgorithm;

}());
