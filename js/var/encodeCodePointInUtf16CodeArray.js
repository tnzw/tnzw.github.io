this.encodeCodePointInUtf16CodeArray = (function script() {
  "use strict";

  /*! encodeCodePointInUtf16CodeArray.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeCodePointInUtf16CodeArray(codePoint, utf16CodeArray, i, l) {
    // encodeCodePointInUtf16CodeArray(0xe9, dst = new Uint16Array(2), 0, 2) -> {writeLength: 1, error: "", requiredWriteLength: 0} -> dst = [0xe9, 0x00]

    // Return value:
    // {
    //   writeLength: 1,  // the number of code written in utf16CodeArray
    //   error: "",  // error code
    //   requiredWriteLength: 0,  // additional nb of utf16 code cells to fix the error
    // };

    // errors:
    //   reserved code point (if > U+D800 & < U+DFFF)
    //   invalid code point (if > U+10FFFF)

    if (i >= l) { return {writeLength: 0, error: "no space on buffer", requiredWriteLength: 1}; }
    else if (codePoint <= 0xD7FF) { utf16CodeArray[i] = codePoint|0; return {writeLength: 1, error: "", requiredWriteLength: 0}; }
    else if (codePoint <= 0xDFFF) { utf16CodeArray[i] = codePoint|0; return {writeLength: 1, error: "reserved code point", requiredWriteLength: 0}; }
    else if (codePoint <= 0xFFFF) { utf16CodeArray[i] = codePoint|0; return {writeLength: 1, error: "", requiredWriteLength: 0}; }
    else if (codePoint <= 0x10FFFF) {
      codePoint -= 0x10000;
      utf16CodeArray[i++] = (0xD800 + ((codePoint >>> 10) & 0x3FF))|0;
      if (i >= l) { return {writeLength: 1, error: "no left space on buffer", requiredWriteLength: 1}; }
      utf16CodeArray[i] = (0xDC00 + (codePoint & 0x3FF))|0;
    }
    return {writeLength: 0, error: "invalid code point", requiredWriteLength: 0};
  }
  encodeCodePointInUtf16CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeCodePointInUtf16CodeArray;

}());
