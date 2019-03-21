this.parseBase64SchemeForDecoding = (function script() {
  "use strict";

  /*! parseBase64SchemeForDecoding.js Version 0.1.7

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  /*
  function parseBase64SchemeForDecoding(scheme) {
    // scheme = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" +
    //          "=" +  // padding (optional)
    //          " \t\r\n"  // ignored values (optional)
    // returns [-1,-1,...,0,1,2,3,4,..] (length 256)
    var i = 0, d = [
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
      -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1
    ], l = scheme.length;
    for (; i < l; i += 1) d[scheme.charCodeAt(i)] = i;
    if (i <= 64) d[61] = 64;
    return d;
  }
  */
  function parseBase64SchemeForDecoding(scheme) {
    // scheme = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" +
    //          "=" +  // padding (optional)
    //          " \t\r\n"  // ignored values (optional)
    // returns {65:0,66:1,...43:62,47:63,61:64,32:65,9:66,13:67,10:68}
    var i = 0, d = {}, l = scheme.length;
    for (; i < l; i += 1) d[scheme.charCodeAt(i)] = i;
    if (i <= 64) d[61] = 64;
    return d;
  }
  parseBase64SchemeForDecoding.toScript = function () { return "(" + script.toString() + "())"; };
  return parseBase64SchemeForDecoding;

}());
