this.sumBytesToSha256Bytes = (function script() {
  "use strict";

  /*! sumBytesToSha256Bytes.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function sumBytesToSha256Bytes(bytes) {
    // V8 optimized (status 1)
    //   `return sumBytesToSha256Bytes([0,0,0,0]);`
    return decodeUint32ArrayToBigEndianBytes(sumBytesToSha256Uint32Array(bytes));
  }
  sumBytesToSha256Bytes.toScript = function () { return "(" + string.toString() + "())"; };
  sumBytesToSha256Bytes._requiredGlobals = [
    "decodeUint32ArrayToBigEndianBytes",
    "sumBytesToSha256Uint32Array"
  ];
  return sumBytesToSha256Bytes;

}());
