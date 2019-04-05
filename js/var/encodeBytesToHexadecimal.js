this.encodeBytesToHexadecimal = (function script() {
  "use strict";

  /*! encodeBytesToHexadecimal.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function encodeBytesToHexadecimal(bytes) {
    var i = 0, hex = "";
    for (; i < bytes.length; i += 1)
      hex += ("0" + bytes[i].toString(16)).slice(-2);
    return hex;
  }
  encodeBytesToHexadecimal.toScript = function () { return "(" + script.toString() + "())"; };
  return encodeBytesToHexadecimal;

}());
