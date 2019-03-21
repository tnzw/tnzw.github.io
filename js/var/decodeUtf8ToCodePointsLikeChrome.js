this.decodeUtf8ToCodePointsLikeChrome = (function script() {
  "use strict";

  /*! decodeUtf8ToCodePointsLikeChrome.js Version 1.0.1

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeUtf8ToCodePointsLikeChrome(bytes) {
    // XXX do documentation

    var out = [],
        result = null,
        error = "",
        readLength = 0,
        i = 0;

    while (i < bytes.length) {
      result = decodeCodePointInUtf8CodeArray(bytes, i, bytes.length);
      error = result.error;
      readLength = result.readLength;
      if (error) {
        out.push(0xFFFD);
        i += 1;

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

        if (error === "invalid continuation byte") {
          if (result.expectedReadLength === 3) {
            if (readLength === 3) {
              // here bytes[i] is already between 0x80 <= and < 0xC0
              if (bytes[i - 1] === 0xE0) {
                if (bytes[i] >= 0xA0)
                  if (bytes[i + 1] < 0x80 || bytes[i + 1] >= 0xC0) i += 1;
              } else if (bytes[i - 1] === 0xED) {
                if (bytes[i] < 0xA0)
                  if (bytes[i + 1] < 0x80 || bytes[i + 1] >= 0xC0) i += 1;
              } else {
                if (bytes[i + 1] < 0x80 || bytes[i + 1] >= 0xC0) i += 1;
                else i += 2;
              }
            }
          } else if (result.expectedReadLength === 4) {
            if (readLength === 3) {
              // here bytes[i] is already between 0x80 <= and < 0xC0
              if (i + 2 < bytes.length) {  // have 4 bytes in a row
                if (bytes[i - 1] === 0xF0) {
                  if (bytes[i] < 0x90) {
                    if (bytes[i + 1] >= 0x80)
                      if (bytes[i + 1] < 0xC0) i += 1;
                  } else i += 1;
                } else if (bytes[i - 1] !== 0xF4 || bytes[i] < 0x90) i += 1;
              }
            } else if (readLength === 4) {
              // here bytes[i] and [i + 1] are already between 0x80 <= and < 0xC0
              if (bytes[i - 1] === 0xF0) {
                if (bytes[i] >= 0x90) i += 2;
              } else if (bytes[i - 1] !== 0xF4 || bytes[i] < 0x90) i += 2;
            }
          }
        }
      } else {
        out.push(result.result);
        i += readLength;
      }
    }
    return out;
  }
  decodeUtf8ToCodePointsLikeChrome.toScript = function () { return "(" + script.toString() + "())"; };
  decodeUtf8ToCodePointsLikeChrome._requiredGlobals = [
    "decodeCodePointInUtf8CodeArray"
  ];
  return decodeUtf8ToCodePointsLikeChrome;

}());
