this.decodeCodePointFromUtf8CodeArray = (function script() {
  "use strict";

  /*! decodeCodePointFromUtf8CodeArray.js Version 1.0.1

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeCodePointFromUtf8CodeArray(array, i, l) {
    // decodeCodePointFromUtf8CodeArray(bytes, 0, bytes.length) -> {result, length, error, warnings, requiredLength, expectedLength}
    // decodeCodePointFromUtf8CodeArray([0xc3, 0xa9, 0x61, 0x62], 0, 4) -> {.: 233, .: 2, .: "", .: "", .: 0, .: 2}

    // Unpacks the first UTF-8 encoding in array and returns the rune and its
    // width in bytes.

    // errors:
    //   invalid start byte
    //   invalid continuation byte
    //   invalid code point
    //   unexpected empty data
    //   unexpected end of data
    // warnings:
    //   overlong encoding
    //   reserved code point

    // Return value:
    // {
    //   result: 0xFFFD,  // the resulting codepoint (default is runeError)
    //   length: 0,  // nb of utf8code read/used
    //   error: "",  // error code
    //   warnings: "",  // comma seperated warning codes
    //   requiredLength: 0,  // additional nb of utf8code required to possibly fix the error
    //   expectedLength: 0,  // the length of the expected code point size
    // };

    // "reserved code point" warning never happens at the same time as with "overlong encoding"

    // Benchmark shows that the speed is equal with old decodeUtf8XxxLikeChrome using decodeXxxAlgorithm.
    // XXX benchmark with return [runeError, 0, error, 1, 1]
    // XXX benchmark with decodeCodePointFromUtf8CodeArray.Result = makeStruct("result,length,error,warnings,requiredLength,expectedLength");

    var code = 0,
        a = 0, c = 0,
        warnings = "",
        runeError = 0xFFFD;

    if (i >= l) { return {result: runeError|0, length: 0, error: "unexpected empty data", warnings: warnings, requiredLength: 1, expectedLength: 1}; }
    code = array[i];

    if (code <= 0x7F) { return {result: code|0, length: 1, error: "", warnings: warnings, requiredLength: 0, expectedLength: 1}; }  // one byte required
    if ((0xE0 & code) === 0xC0) {  // two bytes required
      if (code < 0xC2) { warnings = "overlong encoding"; }
      a = code;
      if (i + 1 >= l) { return {result: runeError|0, length: 1, error: "unexpected end of data", warnings: warnings, requiredLength: 1, expectedLength: 2}; }
      code = array[i + 1];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, length: 2, error: "invalid continuation byte", warnings: warnings, requiredLength: 0, expectedLength: 2}; }
      return {result: ((a << 6) | (code & 0x3F)) & 0x7FF, length: 2, error: "", warnings: warnings, requiredLength: 0, expectedLength: 2};
    }
    if ((0xF0 & code) === 0xE0) {  // three bytes required
      a = code;
      if (i + 1 >= l) { return {result: runeError|0, length: 1, error: "unexpected end of data", warnings: warnings, requiredLength: 2, expectedLength: 3}; }
      code = array[i + 1];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, length: 2, error: "invalid continuation byte", warnings: warnings, requiredLength: 0, expectedLength: 3}; }
      if ((c = a) === 0xE0 && code <= 0x9F) { warnings = "overlong encoding"; }
      a = (c << 6) | (code & 0x3F);
      if (i + 2 >= l) { return {result: runeError|0, length: 2, error: "unexpected end of data", warnings: warnings, requiredLength: 1, expectedLength: 3}; }
      code = array[i + 2];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, length: 3, error: "invalid continuation byte", warnings: warnings, requiredLength: 0, expectedLength: 3}; }
      if (0xD800 <= (c = ((a << 6) | (code & 0x3F)) & 0xFFFF) && c <= 0xDFFF) { warnings = (warnings ? "," : "") + "reserved code point"; }
      return {result: c|0, length: 3, error: "", warnings: warnings, requiredLength: 0, expectedLength: 3};
    }
    if ((0xF8 & code) === 0xF0) {  // four bytes required
      if (code >= 0xF5) { return {result: runeError|0, length: 1, error: "invalid start byte", warnings: warnings, requiredLength: 0, expectedLength: 4}; }
      a = code;
      if (i + 1 >= l) { return {result: runeError|0, length: 1, error: "unexpected end of data", warnings: warnings, requiredLength: 3, expectedLength: 4}; }
      code = array[i + 1];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, length: 2, error: "invalid continuation byte", warnings: warnings, requiredLength: 0, expectedLength: 4}; }
      if ((c = a) === 0xF0 && code <= 0x8F) { warnings = "overlong encoding"; }
      a = (c << 6) | (code & 0x3F);
      if (i + 2 >= l) { return {result: runeError|0, length: 2, error: "unexpected end of data", warnings: warnings, requiredLength: 2, expectedLength: 4}; }
      code = array[i + 2];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, length: 3, error: "invalid continuation byte", warnings: warnings, requiredLength: 0, expectedLength: 4}; }
      a = (a << 6) | (code & 0x3F);
      if (i + 3 >= l) { return {result: runeError|0, length: 3, error: "unexpected end of data", warnings: warnings, requiredLength: 1, expectedLength: 4}; }
      code = array[i + 3];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, length: 4, error: "invalid continuation byte", warnings: warnings, requiredLength: 0, expectedLength: 4}; }
      if ((c = ((a << 6) | (code & 0x3F)) & 0x1FFFFF) > 0x10FFFF) { return {result: runeError|0, length: 4, error: "invalid code point", warnings: warnings, requiredLength: 0, expectedLength: 4}; }
      return {result: c|0, length: 4, error: "", warnings: warnings, requiredLength: 0, expectedLength: 4};
    }
    return {result: runeError|0, length: 1, error: "invalid start byte", warnings: warnings, requiredLength: 0, expectedLength: 1};
  }
  decodeCodePointFromUtf8CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeCodePointFromUtf8CodeArray;

}());
