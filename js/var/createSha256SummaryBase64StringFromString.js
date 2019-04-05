this.createSha256SummaryBase64StringFromString = (function script() {
  "use strict";

  /*! createSha256SummaryBase64StringFromString.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createSha256SummaryBase64StringFromString(string) {
    return createSha256SummaryBase64StringFromBytes(createBytesFromString(string));
  }

  createSha256SummaryBase64StringFromString.toScript = function () { return "(" + script.toString() + "())"; };
  createSha256SummaryBase64StringFromString._requiredGlobals = [
    "createSha256SummaryBase64StringFromBytes",
    "createBytesFromString"
  ];
  return createSha256SummaryBase64StringFromString;

}());
