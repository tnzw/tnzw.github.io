this.decodeBase64ToString = (function script() {
  "use strict";

  /*! decodeBase64ToString.js Version 0.1.0

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeBase64ToString(text) {
    return decodeUtf8ToString(decodeBase64ToBytes(text));
  }
  decodeBase64ToString.toScript = function () { return "(" + script.toString() + "())"; };
  decodeBase64ToString._requiredGlobals = [
    "decodeBase64ToBytes",
    "decodeUtf8ToString"
  ];
  return decodeBase64ToString;

}());
