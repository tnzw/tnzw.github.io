this.encodeUint64ToLittleEndianBytes = (function script() {
  "use strict";

  /*! encodeUint64ToLittleEndianBytes.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeUint64ToLittleEndianBytes(i) {
    // XXX (2**56) === ((2**56) - 1) -> true
    //     max precise number (integer) is 2**53
    return [
      i & 0xFF,
      (i >>> 8) & 0xFF,
      (i >>> 16) & 0xFF,
      (i >>> 24)/* & 0xFF*/,
      (i / 4294967296) & 0xFF,  // 4294967296 = 2**32
      (i / 1099511627776) & 0xFF,  // 1099511627776 = 2**40
      (i / 281474976710656) & 0xFF,  // 281474976710656 = 2**48
      (i / 72057594037927936) & 0xFF  // 72057594037927936 = 2**56
    ];
  }

  encodeUint64ToLittleEndianBytes.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeUint64ToLittleEndianBytes;

}());
