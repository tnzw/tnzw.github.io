this.decodeUtf8ToCodePoints = (function script() {
  "use strict";

  /*! decodeUtf8ToCodePoints.js Version 0.1.35

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeUtf8ToCodePoints(utf8Codes) {
    return decodeUtf8ToCodePointsLikeChrome(utf8Codes);
  }
  decodeUtf8ToCodePoints.toScript = function () { return "(" + script.toString() + "())"; };
  decodeUtf8ToCodePoints._requiredGlobals = ["decodeUtf8ToCodePointsLikeChrome"];
  return decodeUtf8ToCodePoints;

}());
