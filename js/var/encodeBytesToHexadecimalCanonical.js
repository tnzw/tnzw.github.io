this.encodeBytesToHexadecimalCanonical = (function script() {
  "use strict";

  /*! encodeBytesToHexadecimalCanonical.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeBytesToHexadecimalCanonical(bytes) {
    // 00000000  63 6f 75 63 6f 75 63 6f  75 63 6f 75 63 6f 75 63  |coucoucoucoucouc|
    // 00000010  6f 75                                             |ou|
    // 00000012
    var res = "", memi = 0, bi = 0, ai = 0, l = bytes.length;
    for (memi = 0; memi < l; memi += 0x10) {
      res += ("0000000" + memi.toString(16)).slice(-8) + "  ";
      res += ("0" + bytes[bi++].toString(16)).slice(-2) + " ";
      while (bi < l && bi % 0x08) { res += ("0" + bytes[bi++].toString(16)).slice(-2) + " "; }
      res += " ";
      while (bi < l && bi % 0x10) { res += ("0" + bytes[bi++].toString(16)).slice(-2) + " "; }
      if (bi % 0x10) res += "   ".repeat(0x10 - (bi % 0x10)) + " |";
      else res += " |";
      do {
        if (bytes[ai] >= 32 && bytes[ai] <= 126) res += String.fromCharCode(bytes[ai]);
        else res += ".";
        ai += 1;
      } while (ai < l && ai % 0x10);
      res += "|\n";
    }
    res += ("0000000" + bytes.length.toString(16)).slice(-8);
    return res;
  }
  encodeBytesToHexadecimalCanonical.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeBytesToHexadecimalCanonical;

}());
