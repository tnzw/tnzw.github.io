(function script(global) {
  "use strict";

  /*! decodeLatin1CodesToCodePoints.js Version 0.1.1

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeLatin1CodesToCodePoints(latin1Codes) {
    // API stability level: 1 - Experimental
    // XXX do documentation (latin-1 = iso-8859-1)
    // latin1Codes = [...]
    //   an array of latin-1 codes (uint8)
    // returns an array of code points (uint32)
    var i = 0, l = latin1Codes.length, codePoints = new Array(l);
    for (; i < l; i += 1) codePoints[i] = latin1Codes[i];
    return codePoints;
  }
  global.decodeLatin1CodesToCodePoints = decodeLatin1CodesToCodePoints;

}(this));

