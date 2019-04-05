this.createInt32FromBigEndianBytes = (function script() {
  "use strict";

  /*! createInt32FromBigEndianBytes.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createInt32FromBigEndianBytes(bb) {
    return (bb[0] << 24) | (bb[1] << 16) | (bb[2] << 8) | bb[3];
  }

  createInt32FromBigEndianBytes.toScript = function () { return "(" + script.toString() + "())"; };
  return createInt32FromBigEndianBytes;

}());
