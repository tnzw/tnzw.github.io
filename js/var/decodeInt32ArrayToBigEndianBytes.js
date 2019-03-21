this.decodeInt32ArrayToBigEndianBytes = (function script() {
  "use strict";

  /*! decodeInt32ArrayToBigEndianBytes.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeInt32ArrayToBigEndianBytes(int32Array) {
    var i = 0, bytes = [];
    while (i < int32Array.length) bytes.push.apply(bytes, encodeInt32ToBigEndianBytes(int32Array[i++]));
    return bytes;
  }
  decodeInt32ArrayToBigEndianBytes.toScript = function () { return "(" + script.toString() + "())"; };
  decodeInt32ArrayToBigEndianBytes._requiredGlobals = [
    "encodeInt32ToBigEndianBytes"
  ];
  return decodeInt32ArrayToBigEndianBytes;

}());
