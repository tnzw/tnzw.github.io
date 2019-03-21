this.decodeUtf8ToString = (function script() {
  "use strict";

  /*! decodeUtf8ToString.js Version 0.1.36

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeUtf8ToString(bytes) {
    // XXX do documentation
    return encodeCodePointsToString(decodeUtf8ToCodePoints(bytes));
  }
  decodeUtf8ToString.toScript = function () { return "(" + script.toString() + "())"; };
  decodeUtf8ToString._requiredGlobals = [
    "decodeUtf8ToCodePoints",
    "encodeCodePointsToString"
  ];
  return decodeUtf8ToString;

}());
