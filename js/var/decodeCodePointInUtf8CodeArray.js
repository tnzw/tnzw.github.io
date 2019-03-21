this.decodeCodePointInUtf8CodeArray = (function script() {
  "use strict";

  /*! decodeCodePointInUtf8CodeArray.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeCodePointInUtf8CodeArray(array, i, l) {
    // decodeCodePointInUtf8CodeArray(bytes, 0, bytes.length) -> {result, readLength, error, requiredReadLength, expectedReadLength}
    // decodeCodePointInUtf8CodeArray([0xc3, 0xa9, 0x61, 0x62], 0, 4) -> {.: 233, .: 2, .: "", .: 0, .: 2}

    // Unpacks the first UTF-8 encoding in array and returns the rune and its
    // width in bytes.

    // Return value:
    // {
    //   result: 0xFFFD,  // the resulting codepoint (default is runeError)
    //   readLength: 0,  // nb of utf8code read/used
    //   error: "",  // error code
    //   requiredReadLength: 0,  // additional nb of utf8code required to fix the error
    //   expectedReadLength: 0,  // the length of the expected utf8code
    // };

    // XXX test utf8 '\xed\xb0\x80' -> '\udc00' (high surrogates)
    // XXX test utf8 '\xed\xbf\xbf' -> '\udfff' (low surrogates)

    // Benchmark shows that the speed is equal with old decodeUtf8XxxLikeChrome using decodeXxxAlgorithm.
    // XXX benchmark with return [runeError, 0, error, 1, 1]
    // XXX benchmark with decodeCodePointInUtf8CodeArray.Result = makeStruct("result,readLength,error,requiredReadLength,expectedReadLength");

    var code = 0,
        a = 0, c = 0,
        error = "",
        runeError = 0xFFFD;

    if (i >= l) { return {result: runeError|0, readLength: 0, error: "unexpected empty data", requiredReadLength: 1, expectedReadLength: 1}; }
    code = array[i];

    if (code <= 0x7F) { return {result: code|0, readLength: 1, error: "", requiredReadLength: 0, expectedReadLength: 1}; }  // one byte required
    if ((0xE0 & code) === 0xC0) {  // two bytes required
      if (code < 0xC2) { error = "overlong encoding"; }
      a = code;
      if (i + 1 >= l) { return {result: runeError|0, readLength: 2, error: "unexpected end of data", requiredReadLength: 1, expectedReadLength: 2}; }
      code = array[i + 1];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, readLength: 2, error: "invalid continuation byte", requiredReadLength: 0, expectedReadLength: 2}; }
      return {result: (((a << 6) | (code & 0x3F)) & 0x7FF)|0, readLength: 2, error: error, requiredReadLength: 0, expectedReadLength: 2};
    }
    if ((0xF0 & code) === 0xE0) {  // three bytes required
      a = code;
      if (i + 1 >= l) { return {result: runeError|0, readLength: 2, error: "unexpected end of data", requiredReadLength: 2, expectedReadLength: 3}; }
      code = array[i + 1];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, readLength: 2, error: "invalid continuation byte", requiredReadLength: 0, expectedReadLength: 3}; }
      if ((c = a) === 0xE0 && code <= 0x9F) { error = "overlong encoding"; }
      a = (c << 6) | (code & 0x3F);
      if (i + 2 >= l) { return {result: runeError|0, readLength: 3, error: "unexpected end of data", requiredReadLength: 1, expectedReadLength: 3}; }
      code = array[i + 2];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, readLength: 3, error: "invalid continuation byte", requiredReadLength: 0, expectedReadLength: 3}; }
      if (0xD800 <= (c = ((a << 6) | (code & 0x3F)) & 0xFFFF) && c <= 0xDFFF) { error = "reserved code point"; }  // XXX can conflicts with overlong encoding ?
      return {result: c|0, readLength: 3, error: error, requiredReadLength: 0, expectedReadLength: 3};
    }
    if ((0xF8 & code) === 0xF0) {  // four bytes required
      if (code >= 0xF5) { return {result: runeError|0, readLength: 1, error: "invalid start byte", requiredReadLength: 0, expectedReadLength: 4}; }
      a = code;
      if (i + 1 >= l) { return {result: runeError|0, readLength: 2, error: "unexpected end of data", requiredReadLength: 3, expectedReadLength: 4}; }
      code = array[i + 1];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, readLength: 2, error: "invalid continuation byte", requiredReadLength: 0, expectedReadLength: 4}; }
      if ((c = a) === 0xF0 && code <= 0x8F) { error = "overlong encoding"; }
      a = (c << 6) | (code & 0x3F);
      if (i + 2 >= l) { return {result: runeError|0, readLength: 3, error: "unexpected end of data", requiredReadLength: 2, expectedReadLength: 4}; }
      code = array[i + 2];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, readLength: 3, error: "invalid continuation byte", requiredReadLength: 0, expectedReadLength: 4}; }
      a = (a << 6) | (code & 0x3F);
      if (i + 3 >= l) { return {result: runeError|0, readLength: 4, error: "unexpected end of data", requiredReadLength: 1, expectedReadLength: 4}; }
      code = array[i + 3];
      if ((0xC0 & code) != 0x80) { return {result: runeError|0, readLength: 4, error: "invalid continuation byte", requiredReadLength: 0, expectedReadLength: 4}; }
      if ((c = ((a << 6) | (code & 0x3F)) & 0x1FFFFF) > 0x10FFFF) { return {result: runeError|0, readLength: 4, error: "invalid code point", requiredReadLength: 0, expectedReadLength: 4}; }
      return {result: c|0, readLength: 4, error: error, requiredReadLength: 0, expectedReadLength: 4};
    }
    return {result: runeError|0, readLength: 1, error: "invalid start byte", requiredReadLength: 0, expectedReadLength: 1};
  }
  decodeCodePointInUtf8CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeCodePointInUtf8CodeArray;

}());
