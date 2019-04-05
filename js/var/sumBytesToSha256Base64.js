this.sumBytesToSha256Base64 = (function script() {
  "use strict";

  /*! sumBytesToSha256Base64.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function sumBytesToSha256Base64(bytes) {
    return encodeBytesToBase64(sumBytesToSha256Bytes(bytes));
  }
  sumBytesToSha256Base64.toScript = function () { return "(" + script.toString() + "())"; };
  sumBytesToSha256Base64._requiredGlobals = [
    "sumBytesToSha256Bytes",
    "encodeBytesToBase64"
  ];
  return sumBytesToSha256Base64;

}());
