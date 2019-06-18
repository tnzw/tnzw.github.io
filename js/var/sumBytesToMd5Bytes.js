this.sumBytesToMd5Bytes = (function script() {
  "use strict";

  /*! sumBytesToMd5Bytes.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function sumBytesToMd5Bytes(bytes) {
    return decodeUint32ArrayToLittleEndianBytes(sumBytesToMd5Uint32Array(bytes));
  }
  sumBytesToMd5Bytes.toScript = function () { return "(" + script.toString() + "())"; };
  sumBytesToMd5Bytes._requiredGlobals = [
    "sumBytesToMd5Uint32Array",
    "decodeUint32ArrayToLittleEndianBytes"
  ];
  return sumBytesToMd5Bytes;

}());
