this.sumBytesToMd5Hexadecimal = (function script() {
  "use strict";

  /*! sumBytesToMd5Hexadecimal.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function sumBytesToMd5Hexadecimal(bytes) {
    return encodeBytesToHexadecimal(sumBytesToMd5Bytes(bytes));
  }
  sumBytesToMd5Hexadecimal.toScript = function () { return "(" + script.toString() + "())"; };
  sumBytesToMd5Hexadecimal._requiredGlobals = [
    "sumBytesToMd5Bytes",
    "encodeBytesToHexadecimal"
  ];
  return sumBytesToMd5Hexadecimal;

}());
