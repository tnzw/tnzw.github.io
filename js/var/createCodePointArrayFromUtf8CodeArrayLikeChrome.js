this.createCodePointArrayFromUtf8CodeArrayLikeChrome = (function script() {
  "use strict";

  /*! createCodePointArrayFromUtf8CodeArrayLikeChrome.js Version 1.1.1

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createCodePointArrayFromUtf8CodeArrayLikeChrome(bytes, i, l) {
    // XXX do documentation

    var out = [],
        result = null,
        error = "",
        length = 0;

    if (i === undefined) i = 0;
    if (l === undefined) l = bytes.length;
    while (i < l) {
      result = decodeCodePointFromUtf8CodeArray(bytes, i, l);
      error = result.error || result.warnings;
      if (error) {
        out.push(0xFFFD);
        i += 1;
        length = result.length;

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
          if (result.expectedLength === 3) {
            if (length === 3) {
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
          } else if (result.expectedLength === 4) {
            if (length === 3) {
              // here bytes[i] is already between 0x80 <= and < 0xC0
              if (i + 2 < l) {  // have 4 bytes in a row
                if (bytes[i - 1] === 0xF0) {
                  if (bytes[i] < 0x90) {
                    if (bytes[i + 1] >= 0x80)
                      if (bytes[i + 1] < 0xC0) i += 1;
                  } else i += 1;
                } else if (bytes[i - 1] !== 0xF4 || bytes[i] < 0x90) i += 1;
              }
            } else if (length === 4) {
              // here bytes[i] and [i + 1] are already between 0x80 <= and < 0xC0
              if (bytes[i - 1] === 0xF0) {
                if (bytes[i] >= 0x90) i += 2;
              } else if (bytes[i - 1] !== 0xF4 || bytes[i] < 0x90) i += 2;
            }
          }
        }
      } else {
        out.push(result.result);
        i += result.length;
      }
    }
    return out;
  }
  createCodePointArrayFromUtf8CodeArrayLikeChrome.toScript = function () { return "(" + script.toString() + "())"; };
  createCodePointArrayFromUtf8CodeArrayLikeChrome._requiredGlobals = ["decodeCodePointFromUtf8CodeArray"];
  return createCodePointArrayFromUtf8CodeArrayLikeChrome;

}());
