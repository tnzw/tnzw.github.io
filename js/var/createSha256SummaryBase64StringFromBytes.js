this.createSha256SummaryBase64StringFromBytes = (function script() {
  "use strict";

  /*! createSha256SummaryBase64StringFromBytes.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createSha256SummaryBase64StringFromBytes(bytes) {
    return createBase64StringFromBytes(createSha256SummaryBytesFromBytes(bytes));
  }

  createSha256SummaryBase64StringFromBytes.toScript = function () { return "(" + script.toString() + "())"; };
  createSha256SummaryBase64StringFromBytes._requiredGlobals = [
    "createSha256SummaryBytesFromBytes",
    "createBase64StringFromBytes"
  ];
  return createSha256SummaryBase64StringFromBytes;

}());
