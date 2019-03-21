this.decodeUtf8ToCodePointsLikeFirefox = (function script() {
  "use strict";

  /*! decodeUtf8ToCodePointsLikeFirefox.js Version 0.1.37

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeUtf8ToCodePointsLikeFirefox(bytes) {
    // XXX do documentation
    var cont = true, ret = [], ee = [], e, cache = [0,0,0,0,0], i = 0, ei = 0;
    while (cont) {
      cont = false;
      decodeUtf8ToCodePointsChunkAlgorithm(bytes, i, bytes.length, ret, false, ee, cache, true);
      if ((e = ee[ei++]) !== undefined) {
        ret.push(0xFFFD);
        cache[0] = 0; //cache.splice(0);
        i = e.index - e.length + 2;

        // Strange case for invalid continuation bytes
        //     legend: C: valid continuation byte,
        //             X: invalid continuation byte,
        //             S: start byte,
        //             E: error code (i.e. 0xFFFD or 65533),
        //             ?: random byte
        //     showing cases were bytes sequences are always invalid
        //   decode([S, C, C]) => [E] + decode([C, C]) as if only [S] is consumed
        //   decode([S, C, X]) => [E] + decode([X]) as if [S, C] are consumed
        //   decode([S, X, ?]) => [E] + decode([X, ?]) as if [S] is consumed
        //
        //   decode([S, C, C, C]) => [E] + decode([C, C, C]) as if only [S] is consumed
        //   decode([S, C, C, X]) => [E] + decode([X]) as if [S, C, C] are consumed
        //   decode([S, C, X, ?]) => [E] + decode([X, ?]) as if [S, C] are consumed
        //   decode([S, X, ?, ?]) => [E] + decode([X, ?, ?]) as if [S] is consumed
        //
        // this works for many cases, not all.

        if (e.errno === 2) {  // invalid continuation byte
          if (e.requiredUtf8CodeAmount === 3) {
            if (e.length === 3) {
              // here bytes[i] is already between 0x80 and 0xBF
              if (bytes[i - 1] != 0xED || bytes[i] <= 0x9F) ++i;
            }
          } else if (e.requiredUtf8CodeAmount === 4) {
            if (e.length === 3) {
              // here bytes[i] is already between 0x80 and 0xBF
              if (bytes[i - 1] !== 0xF4 || bytes[i] <= 0x8F) ++i;
            } else if (e.length === 4) {
              // here bytes[i] and [i + 1] are already between 0x80 and 0xBF
              if (bytes[i - 1] !== 0xF4 || bytes[i] <= 0x8F) i += 2;
            }
          }
        } else if (e.errno === 6) {  // unexpected end of data
          if (e.requiredUtf8CodeAmount === 3) ++i;
          else if (e.requiredUtf8CodeAmount === 4) {
            if (bytes[i - 1] !== 0xF4) i += 2;
          }
        }

        cont = i < bytes.length;
      }
    }
    return ret;
  }
  decodeUtf8ToCodePointsLikeFirefox.toScript = function () { return "(" + script.toString() + "())"; };
  decodeUtf8ToCodePointsLikeFirefox._requiredGlobals = [
    "decodeUtf8ToCodePointsChunkAlgorithm"
  ];
  return decodeUtf8ToCodePointsLikeFirefox;

}());
