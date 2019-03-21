this.decodeUint32ArrayToBigEndianBytes = (function script() {
  "use strict";

  /*! decodeUint32ArrayToBigEndianBytes.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeUint32ArrayToBigEndianBytes(uint32Array) {
    var i = 0, bytes = [];
    while (i < uint32Array.length) bytes.push.apply(bytes, encodeUint32ToBigEndianBytes(uint32Array[i++]));
    return bytes;
  }

  decodeUint32ArrayToBigEndianBytes._requiredGlobals = [
    "encodeUint32ToBigEndianBytes"
  ];
  decodeUint32ArrayToBigEndianBytes.toScript = function () { return "(" + lib.toString() + "())"; };
  return decodeUint32ArrayToBigEndianBytes;

}());
