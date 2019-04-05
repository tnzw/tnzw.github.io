this.createUtf8CodeArrayFromString = (function script() {
  "use strict";

  /*! createUtf8CodeArrayFromString.js Version 1.0.1

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createUtf8CodeArrayFromString(text) {
    // XXX do documentation
    var i = 0, l = text.length, utf16Codes = new Array(l);
    for (; i < l; i += 1) utf16Codes[i] = text.charCodeAt(i);
    return createUtf8CodeArrayFromUtf16CodeArray(utf16Codes, 0, utf16Codes.length);
  }
  createUtf8CodeArrayFromString.toScript = function () { return "(" + script.toString() + "())"; };
  createUtf8CodeArrayFromString._requiredGlobals = ["createUtf8CodeArrayFromUtf16CodeArray"];
  return createUtf8CodeArrayFromString;

}());
