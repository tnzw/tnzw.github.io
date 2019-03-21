this.sumStringToMd5Hexadecimal = (function script() {
  "use strict";

  /*! sumStringToMd5Hexadecimal.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function sumStringToMd5Hexadecimal(text) {
    return encodeBytesToHexadecimal(
      sumBytesToMd5Bytes(
      encodeStringToUtf8(text)
    ));
  }
  sumStringToMd5Hexadecimal.toScript = function () { return "(" + script.toString() + "())"; };
  sumStringToMd5Hexadecimal._requiredGlobals = [
    "encodeStringToUtf8",
    "sumBytesToMd5Bytes",
    "encodeBytesToHexadecimal"
  ];
  return sumStringToMd5Hexadecimal;

}());
