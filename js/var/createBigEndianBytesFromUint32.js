this.createBigEndianBytesFromUint32 = (function script() {
  "use strict";

  /*! createBigEndianBytesFromUint32.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createBigEndianBytesFromUint32(i) {
    // also works for int32
    return [
      (i >>> 24)/* & 0xFF*/,
      (i >>> 16) & 0xFF,
      (i >>> 8) & 0xFF,
      i & 0xFF
    ];
  }
  createBigEndianBytesFromUint32.toScript = function () { return "(" + script.toString() + "())"; };
  return createBigEndianBytesFromUint32;

}());
