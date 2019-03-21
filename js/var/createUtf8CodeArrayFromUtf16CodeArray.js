this.createUtf8CodeArrayFromUtf16CodeArray = (function script() {
  "use strict";

  /*! createUtf8CodeArrayFromUtf16CodeArray.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createUtf8CodeArrayFromUtf16CodeArray(utf16Codes, i, l) {
    // XXX do documentation

    i = i|0;
    l = l|0;
    var utf8Codes = [], r = null, w = 0;
    while (i < l) {
      r = transcodeUtf8CodeArrayFromUtf16CodeArray(utf16Codes, i, l);
      switch (r.error) {
        case "":
          for (w = 0; w < r.result.length; w = (w + 1)|0) utf8Codes.push(r.result[w]);
          i = (i + (r.length|0))|0;
          break;
        case "invalid continuation code":
          i = (i - 1)|0;
        case "unexpected end of data":
        case "invalid start code":
          utf8Codes.push(0xEF, 0xBF, 0xBD);
          i = (i + (r.length|0))|0;
          break;
        default:
          throw new Error("unhandled error " + r.error);
      }
    }
    return utf8Codes;
  }
  createUtf8CodeArrayFromUtf16CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  createUtf8CodeArrayFromUtf16CodeArray._requiredGlobals = ["transcodeUtf8CodeArrayFromUtf16CodeArray"];
  return createUtf8CodeArrayFromUtf16CodeArray;

}());
