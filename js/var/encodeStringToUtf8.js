this.encodeStringToUtf8 = (function script() {
  "use strict";

  /*! encodeStringToUtf8.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeStringToUtf8(text) {
    // XXX do documentation
    var i = 0, l = text.length, utf16Codes = new Array(l);
    for (; i < l; i += 1) utf16Codes[i] = text.charCodeAt(i);
    return encodeUtf16ToUtf8(utf16Codes);
  }
  encodeStringToUtf8.toScript = function () { return "(" + script.toString() + "())"; };
  encodeStringToUtf8._requiredGlobals = ["encodeUtf16ToUtf8"];
  return encodeStringToUtf8;

}());
