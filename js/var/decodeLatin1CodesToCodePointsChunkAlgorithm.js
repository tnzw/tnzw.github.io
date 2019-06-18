(function script(global) {
  "use strict";

  /*! decodeLatin1CodesToCodePointsChunkAlgorithm.js Version 0.1.1

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeLatin1CodesToCodePointsChunkAlgorithm(latin1Codes, i, l, codePoints) {
    // API stability level: 1 - Experimental

    // XXX do documentation (latin-1 = iso-8859-1)

    // latin1Codes = [...]
    //   an array of latin-1 codes (uint8)
    // i or from = 0
    //   from which index to start reading latin1Codes
    // l or to = latin1Codes.length
    //   from which index to stop reading latin1Codes
    // codePoints = []
    //   where the code points (uint32) are pushed
    // returns codePoints

    for (; i < l; i += 1) codePoints.push(latin1Codes[i]);
    return codePoints;
  }
  global.decodeLatin1CodesToCodePointsChunkAlgorithm = decodeLatin1CodesToCodePointsChunkAlgorithm;

}(this));

