this.rotateInt32BitsRight = (function script() {
  "use strict";

  /*! rotateInt32BitsRight.js Version 1.0.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function rotateInt32BitsRight(i, n) {
    // also works for uint32
    n %= 32;
    return ((i >>> n) | (i << (32 - n)))/* & 0xFFFFFFFF*/;
  }

  rotateInt32BitsRight.toScript = function () { return "(" + script.toString() + "())"; };
  return rotateInt32BitsRight;

}());
