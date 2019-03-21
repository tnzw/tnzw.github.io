this.createBigEndianBytesFromUint32Array = (function script() {
  "use strict";

  /*! createBigEndianBytesFromUint32Array.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createBigEndianBytesFromUint32Array(uint32Array) {
    var i = 0, j = 0,
        bytes = new Array(uint32Array.length * 4);
    for (; i < uint32Array.length; i += 1) {
      bytes[j++] =  uint32Array[i] >>> 24;  // & 0xFF;
      bytes[j++] = (uint32Array[i] >>> 16) & 0xFF;
      bytes[j++] = (uint32Array[i] >>>  8) & 0xFF;
      bytes[j++] =  uint32Array[i]         & 0xFF;
    }
    return bytes;
  }

  createBigEndianBytesFromUint32Array.toScript = function () { return "(" + script.toString() + "())"; };
  return createBigEndianBytesFromUint32Array;

}());
