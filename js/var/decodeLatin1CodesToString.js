this.decodeLatin1CodesToString = (function script() {
  "use strict";

  /*! decodeLatin1CodesToString.js Version 1.0.0

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeLatin1CodesToString(latin1Codes) {
    // XXX do documentation (latin-1 = iso-8859-1)
    // quicker than using `String.fromCodePoint.apply(String, codePoints)`
    //   (and 32766 was the amount limit of argument for a function call).
    // latin1Codes = [...]
    //   an array of latin-1 codes (uint8)
    // returns an array of code points (uint32)
    // V8 optimized (status 1)
    //   `return decodeLatin1CodesToString([0,0,0,0]);`
    var i = 0, l = latin1Codes.length, s = "";
    for (; i < l; i += 1) s += String.fromCharCode(latin1Codes[i]);
    return s;
  }
  decodeLatin1CodesToString.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeLatin1CodesToString;

}());
