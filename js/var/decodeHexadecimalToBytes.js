this.decodeHexadecimalToBytes = (function script() {
  "use strict";

  /*! decodeHexadecimalToBytes.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeHexadecimalToBytes(text) {
    var i = 0, bytes = new Array(text.length / 2);
    for (; i < bytes.length; i += 1)
      bytes[i] = parseInt(text.slice((i * 2), (i * 2) + 2), 16);
    return bytes;
  }
  decodeHexadecimalToBytes.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeHexadecimalToBytes;

}());
