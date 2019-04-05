this.createReprStringFromBytes = (function script() {
  "use strict";

  /*! createReprStringFromBytes.js Version 1.0.0

      Copyright (c) 2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createReprStringFromBytes(bytes) {
    var s = "", i = 0, byte = 0;
    for (; i < bytes.length; i += 1) {
      byte = bytes[i] & 0xFF;
      if (byte === 0x0A) { s += "\\n"; }
      else if (byte === 0x09) { s += "\\t"; }
      else if (byte === 0x0D) { s += "\\r"; }
      else if (byte === 0x08) { s += "\\b"; }
      else if (byte === 0x0C) { s += "\\f"; }
      else if (byte === 0x0B) { s += "\\v"; }
      else if (byte === 0x22) { s += "\\\""; }
      else if (byte === 0x5C) { s += "\\\\"; }
      else if (byte < 0x10) { s += "\\x0" + byte.toString(16); }
      else if (byte < 0x20 || byte >= 0x80) { s += "\\x" + byte.toString(16); }
      else { s += String.fromCharCode(byte); }
    }
    return s;
  }
  createReprStringFromBytes.toScript = function () { return "(" + script.toString() + "())"; };
  return createReprStringFromBytes;

}());
