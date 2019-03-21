this.transcodeUtf8CodeArrayFromUtf16CodeArray = (function script() {
  "use strict";

  /*! transcodeUtf8CodeArrayFromUtf16CodeArray.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function transcodeUtf8CodeArrayFromUtf16CodeArray(array, i, l) {
    // transcodeUtf8CodeArrayFromUtf16CodeArray(codes, 0, codes.length) -> {result, length, error}

    i = i|0;
    l = l|0;
    if (i >= l) return {result: null, length: 0, error: "unexpected empty data"};
    var c = array[i] & 0xFFFF, c1 = 0;

    if (c <= 0x7F) return {result: [c], length: 1, error: ""};
    if (c <= 0x7FF) return {result: [(c >> 6) | 0xc0, (c & 0x3f) | 0x80], length: 1, error: ""};
    if (0xd800 <= c && c <= 0xdbff) {
      i = (i + 1)|0; if (i >= l) return {result: null, length: 1, error: "unexpected end of data"};
      c1 = c|0;
      c = array[i] & 0xFFFF;
      if (0xdc00 <= c && c <= 0xdfff) {
        c1 = (c1 + 0x40)|0;
        return {result: [((c1 >> 8) & 0x7) | 0xf0, ((c1 >> 2) & 0x3f) | 0x80, ((c1 & 0x3) << 4) | ((c >> 6) & 0xf) | 0x80, (c & 0x3f) | 0x80], length: 2, error: ""};
        //c = (((c1 & 0x3FF) << 10) + (c & 0x3FF) + 0x10000)|0;
        //return {result: [((c >> 18) & 0x7) | 0xf0, ((c >> 12) & 0x3f) | 0x80, ((c >> 6) & 0x3f) | 0x80, (c & 0x3f) | 0x80], length: 2, error: ""};
      }
      return {result: null, length: 2, error: "invalid continuation code"};
    }
    if (0xdc00 <= c && c <= 0xdfff) return {result: null, length: 1, error: "invalid start code"};
    return {result: [((c >> 12) & 0xf) | 0xe0, ((c >> 6) & 0x3f) | 0x80, (c & 0x3f) | 0x80], length: 1, error: ""};
  }
  transcodeUtf8CodeArrayFromUtf16CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  return transcodeUtf8CodeArrayFromUtf16CodeArray;

}());
