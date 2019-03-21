this.createUint16StringFromBinaryString = (function script() {
  "use strict";

  /*! createUint16StringFromBinaryString.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createUint16StringFromBinaryString(binaryString) {
    return createStrictUint16StringFromLittleEndianBinaryString(binaryString);
  }

  createUint16StringFromBinaryString.toScript = function () { return "(" + script.toString() + "())"; };
  createUint16StringFromBinaryString._requiredGlobals = ["createStrictUint16StringFromLittleEndianBinaryString"];
  return createUint16StringFromBinaryString;

}());
