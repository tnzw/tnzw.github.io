this.createSha256SummaryBytesFromBytes = (function script() {
  "use strict";

  /*! createSha256SummaryBytesFromBytes.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createSha256SummaryBytesFromBytes(bytes) {
    // V8 optimized (status 1)
    //   `return createSha256SummaryBytesFromBytes([0,0,0,0]);`
    return createBigEndianBytesFromUint32Array(createSha256SummaryUint32ArrayFromBytes(bytes));
  }
  createSha256SummaryBytesFromBytes.toScript = function () { return "(" + string.toString() + "())"; };
  createSha256SummaryBytesFromBytes._requiredGlobals = [
    "createBigEndianBytesFromUint32Array",
    "createSha256SummaryUint32ArrayFromBytes"
  ];
  return createSha256SummaryBytesFromBytes;

}());
