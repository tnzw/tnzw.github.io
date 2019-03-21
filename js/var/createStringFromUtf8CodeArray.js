this.createStringFromUtf8CodeArray = (function script() {
  "use strict";

  /*! createStringFromUtf8CodeArray.js Version 1.0.0

      Copyright (c) 2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createStringFromUtf8CodeArray(utf8CodeArray) {
    return createStringFromCodePointArray(createCodePointArrayFromUtf8CodeArray(utf8CodeArray));
  }
  createStringFromUtf8CodeArray.toScript = function () { return "(" + script.toString() + "())"; };
  createStringFromUtf8CodeArray._requiredGlobals = [
    "createCodePointArrayFromUtf8CodeArray",
    "createStringFromCodePointArray"
  ];
  return createStringFromUtf8CodeArray;

}());
