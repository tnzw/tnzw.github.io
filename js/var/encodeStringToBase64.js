this.encodeStringToBase64 = (function script() {
  "use strict";

  /*! encodeStringToBase64.js Version 0.1.0

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeStringToBase64(text) {
    return encodeBytesToBase64(encodeStringToUtf8(text));
  }
  encodeStringToBase64.toScript = function () { return "(" + script.toString() + "())"; };
  encodeStringToBase64._requiredGlobals = [
    "encodeStringToUtf8",
    "encodeBytesToBase64"
  ];
  return encodeStringToBase64;

}());
