this.decodeUint32ArrayToLittleEndianBytes = (function script() {
  "use strict";

  /*! decodeUint32ArrayToLittleEndianBytes.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  //importScriptsAsync("encodeUint32ToLittleEndianBytes.js");

  function decodeUint32ArrayToLittleEndianBytes(uint32Array) {
    var i = 0, bytes = [];
    while (i < uint32Array.length) bytes.push.apply(bytes, encodeUint32ToLittleEndianBytes(uint32Array[i++]));
    return bytes;
  }
  decodeUint32ArrayToLittleEndianBytes.toScript = function () { return "(" + script.toString() + "())"; };
  decodeUint32ArrayToLittleEndianBytes._requiredGlobals = ["encodeUint32ToLittleEndianBytes"];
  return decodeUint32ArrayToLittleEndianBytes;

}());
