this.encodeCodePointInUtf8Array = (function script() {
  "use strict";

  /*! encodeCodePointInUtf8Array.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointInUtf8Array(code, utf8Codes, i, l) {  // XXX rename vars XXX rename function s/Array/CodeArray/ ?
    // XXX do documentation

    // errors :
    //   reserved code point (if > U+D800 & < U+DFFF)
    //   invalid code point (if > U+10FFFF)
    //   no space on buffer
    //   no left space on buffer

    var b = 0, c = 0, d = 0, error = "";
    if (i >= l) { return {writeLength: 0, error: "no space on buffer"}; }
    if (code <= 0x7F) {
      utf8Codes[i] = code;
      return {writeLength: 1, error: ""};
    } else if (code <= 0x7FF) {
      // a = (0x1E << (6 - 1)) | (code & (0x3F >> 1));
      b = 0x80 | (code & 0x3F); code >>>= 6;
      utf8Codes[i++] = 0xC0 | (code & 0x1F);
      if (i >= l) { return {writeLength: 1, error: "no left space on buffer"}; }
      utf8Codes[i] = b;
      return {writeLength: 2, error: ""};
    } else if (code <= 0xFFFF) {
      if (0xD800 <= code && code <= 0xDFFF) error = "reserved code point";
      // a = (0x1E << (6 - 2)) | (code & (0x3F >> 2));
      c = 0x80 | (code & 0x3F); code >>>= 6;
      b = 0x80 | (code & 0x3F); code >>>= 6;
      utf8Codes[i++] = 0xE0 | (code & 0xF);
      if (i >= l) { return {writeLength: 1, error: "no left space on buffer"}; }  // conflicts with "reserved code point" error ?
      utf8Codes[i++] = b;
      if (i >= l) { return {writeLength: 2, error: "no left space on buffer"}; }  // conflicts with "reserved code point" error ?
      utf8Codes[i] = c;
      return {writeLength: 3, error: error};
    } else if (code <= 0x10FFFF) {
      // a = (0x1E << (6 - 3)) | (code & (0x3F >> 3));
      d = 0x80 | (code & 0x3F); code >>>= 6;
      c = 0x80 | (code & 0x3F); code >>>= 6;
      b = 0x80 | (code & 0x3F); code >>>= 6;
      utf8Codes[i++] = 0xF0 | (code & 0x7);
      if (i >= l) { return {writeLength: 1, error: "no left space on buffer"}; }
      utf8Codes[i++] = b;
      if (i >= l) { return {writeLength: 2, error: "no left space on buffer"}; }
      utf8Codes[i++] = c;
      if (i >= l) { return {writeLength: 3, error: "no left space on buffer"}; }
      utf8Codes[i] = d;
    } else {
      return {writeLength: 0, error: "invalid code point"};
    }
  }
  encodeCodePointInUtf8Array.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeCodePointInUtf8Array;

}());
