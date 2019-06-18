this.decodeStringFromUtf8CodeArray = (function script() {
  "use strict";

  /*! decodeStringFromUtf8CodeArray.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeStringFromUtf8CodeArray(array, i, l) {
    // decodeStringFromUtf8CodeArray(bytes, 0, bytes.length) -> {result, length, error, warnings, requiredLength, expectedLength}
    // decodeStringFromUtf8CodeArray([0xc3, 0xa9, 0x61, 0x62], 0, 4) -> {.: [233], .: 2, .: "", .: "", .: 0, .: 2}

    // Unpacks the first UTF-8 encoding in array and returns a string and its
    // width in bytes.

    // errors and warnings:
    //   see decodeCodePointFromUtf8CodeArray

    // Return value:
    // {
    //   result: "\uFFFD",  // the resulting string (default is "runeError")
    //   length: 0,  // nb of utf8code read/used
    //   error: "",  // error code
    //   warnings: "",  // comma seperated warning codes
    //   requiredLength: 0,  // additional nb of utf8code required to possibly fix the error
    //   expectedLength: 0,  // the length of the expected code point size
    // };

    // Reserved code points are handled like :
    // - [0xED, 0xA0, 0x80] -> "\uD800"
    // - [0xED, 0xBF, 0xBF] -> "\uDFFF"

    // This function is copied from decodeUtf16CodeArrayFromUtf8CodeArray.

    // XXX try to not use `decodeCodePointFromUtf8CodeArray` or keep like this ?
    //     is a pair of UTF-16 if UTF-8 is > `F0 9. .. ..`.

    var r = decodeCodePointFromUtf8CodeArray(array, i, l),
        result = {result: "", length: r.length|0, error:  "" + r.error, warnings: "" + r.warnings,
                  requiredLength: r.requiredLength|0, expectedLength: r.expectedLength|0};
    // all errors and warnings should be already handled by `decodeCodePointFromUtf8CodeArray`,
    // as the reserved code point are the same as in utf8.
    if (r.result <= 0xFFFF) {
      result.result = ""+String.fromCharCode(r.result);
    } else {
      r.result -= 0x10000;
      result.result = ""+String.fromCharCode(
        (0xD800 + ((r.result >>> 10) & 0x3FF))|0,
        (0xDC00 + (r.result & 0x3FF))|0
      );
    }
    r = null;
    return result;
  }
  decodeStringFromUtf8CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  decodeStringFromUtf8CodeArray._requiredGlobals = ["decodeCodePointFromUtf8CodeArray"];
  return decodeStringFromUtf8CodeArray;

}());
