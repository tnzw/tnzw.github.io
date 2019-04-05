this.sumBytesToSha256Hexadecimal = (function script() {
  "use strict";

  /*! sumBytesToSha256Hexadecimal.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function sumBytesToSha256Hexadecimal(bytes) {
    return encodeBytesToHexadecimal(sumBytesToSha256Bytes(bytes));
  }
  sumBytesToSha256Bytes.toScript = function () { return "(" + script.toString + "())"; };
  sumBytesToSha256Bytes._requiredGlobals = [
    "sumBytesToSha256Bytes",
    "encodeBytesToHexadecimal"
  ];
  return sumBytesToSha256Hexadecimal;

}());
