this.encodeInt32ToBigEndianBytes = (function script() {
  "use strict";

  /*! encodeInt32ToBigEndianBytes.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeInt32ToBigEndianBytes(i) {
    // also works for uint32
    return [
      (i >>> 24)/* & 0xFF*/,
      (i >>> 16) & 0xFF,
      (i >>> 8) & 0xFF,
      i & 0xFF
    ];
  }
  encodeInt32ToBigEndianBytes.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeInt32ToBigEndianBytes;

}());
