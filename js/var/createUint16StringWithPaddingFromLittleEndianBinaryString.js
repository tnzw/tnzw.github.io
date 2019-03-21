this.createUint16StringWithPaddingFromLittleEndianBinaryString = (function script() {
  "use strict";

  /*! createUint16StringWithPaddingFromLittleEndianBinaryString.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createUint16StringWithPaddingFromLittleEndianBinaryString(binaryString, padding) {
    var uint16String = "", i = 0, l = (binaryString.length - 1)|0;
    for (; i < l; i = (i + 2)|0)
      uint16String += String.fromCharCode((binaryString.charCodeAt(i) & 0xFF) | ((binaryString.charCodeAt((i + 1)|0) & 0xFF) << 8));
    if (i < uint16String.length)
      uint16String += String.fromCharCode((binaryString.charCodeAt(i) & 0xFF) | ((padding & 0xFF) << 8));
    return uint16String;
  }

  createUint16StringWithPaddingFromLittleEndianBinaryString.toScript = function () { return "(" + script.toString() + "())"; };
  return createUint16StringWithPaddingFromLittleEndianBinaryString;

}());
