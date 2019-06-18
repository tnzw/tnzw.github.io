this.createCrcUint32FromBytes = (function script() {
  "use strict";

  /*! createCrcUint32FromBytes.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createCrcUint32FromBytes(bytes) {
    return createCrcInt32FromBytes(bytes) >>> 0;
  }
  createCrcUint32FromBytes.toScript = function () { return "(" + script.toString() + "())"; };
  createCrcUint32FromBytes._requiredGlobals = ["createCrcInt32FromBytes"];
  return createCrcUint32FromBytes;

}());
