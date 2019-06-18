this.transcodeUtf16CodeArrayInUtf8CodeArray = (function script() {
  "use strict";

  /*! transcodeUtf16CodeArrayInUtf8CodeArray.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function transcodeUtf16CodeArrayInUtf8CodeArray(utf16CodesArray, ai, al, utf8CodesArray, bi, bl) {
    // transcodeUtf16CodeArrayInUtf8CodeArray(...) -> {readLength, writeLength, error}
    // transcodeUtf16CodeArrayInUtf8CodeArray([0xe9, 0x0a], 0, 1, dst = [0, 0], 0, 2) -> {.: 1, .: 2, .: ""} -> dst: [0xc3, 0xa9]

    // Unpacks the first UTF-16 encoding in array, transcode to utf8 code and
    // write in the UTF-8 buffer the resulting transcoding.

    // Return value:
    // {
    //   readLength: 0,  // nb of utf16 code read/used
    //   writeLength: 0,  // nb of utf8 code written
    //   error: "",  // error code
    // };

    // errors :
    //   invalid start code
    //   invalid continuation code
    //   unexpected empty data
    //   unexpected end of data
    //   no space on buffer
    //   no space left on buffer

    var utf16Code = 0, c = 0;
    if (ai >= al) { return {readLength: 0, writeLength: 0, error: "unexpected empty data"}; }
    if (bi >= bl) { return {readLength: 0, writeLength: 0, error: "no space on buffer"}; }
    utf16Code = utf16CodesArray[ai];
    
    if (utf16Code <=  0x7F) {
      utf8CodesArray[bi] = utf16Code|0;
      return {readLength: 1, writeLength: 1, error: ""};
    } else if (utf16Code <= 0x7FF) {
      utf8CodesArray[bi] = ((utf16Code >> 6) | 0xc0)|0;
      if (++bi >= bl) { return {readLength: 1, writeLength: 1, error: "no left space on buffer"}; }
      utf8CodesArray[bi] = ((utf16Code & 0x3f) | 0x80)|0;
      return {readLength: 1, writeLength: 2, error: ""};
    } else if (0xD800 <= utf16Code && utf16Code <= 0xDBFF) {
      if (++ai >= al) { return {readLength: 1, writeLength: 0, error: "unexpected end of data"}; }
      c = utf16CodesArray[ai]|0;
      if (0xDC00 <= c && c <= 0xDFFF) {
        c = ((c - 0xD800) << 10) + (utf16Code - 0xDC00) + 0x10000;
        utf8CodesArray[bi] = ((c >> 18) | 0xf0)|0;
        if (++bi >= bl) { return {readLength: 2, writeLength: 1, error: "no left space on buffer"}; }
        utf8CodesArray[bi] = (((c >> 12) & 0x3f) | 0x80)|0;
        if (++bi >= bl) { return {readLength: 2, writeLength: 2, error: "no left space on buffer"}; }
        utf8CodesArray[bi] = (((c >> 6) & 0x3f) | 0x80)|0;
        if (++bi >= bl) { return {readLength: 2, writeLength: 3, error: "no left space on buffer"}; }
        utf8CodesArray[bi] = ((c & 0x3f) | 0x80)|0;
        return {readLength: 2, writeLength: 4, error: ""};
      } else {
        return {readLength: 2, writeLength: 0, error: "invalid continuation code"};
      }
    } else if (0xDC00 <= utf16Code && utf16Code <= 0xDFFF) {
      return {readLength: 1, writeLength: 0, error: "invalid start code"};
    } else {
      utf8CodesArray[bi] = (((utf16Code >> 12) & 0xf) | 0xe0)|0;
      if (++bi >= bl) { return {readLength: 1, writeLength: 1, error: "no left space on buffer"}; }
      utf8CodesArray[bi] = (((utf16Code >> 6) & 0x3f) | 0x80)|0
      if (++bi >= bl) { return {readLength: 1, writeLength: 2, error: "no left space on buffer"}; }
      utf8CodesArray[bi] = ((utf16Code & 0x3f) | 0x80)|0;
      return {readLength: 1, writeLength: 3, error: ""};
    }
    return {readLength: 1, writeLength: 0, error: "inconsistent behavior"};
  }
  transcodeUtf16CodeArrayInUtf8CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  return transcodeUtf16CodeArrayInUtf8CodeArray;

}());
