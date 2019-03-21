(function (global) {
  "use strict";

  /*! parseBase64SchemeForStringDecoding.js Version 0.1.7

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function parseBase64SchemeForStringDecoding(scheme) {
    // scheme = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" +
    //          "=" +  // padding (optional)
    //          " \t\r\n"  // ignored values (optional)
    // returns {A:0,B:1,..."+":62,"/":63,"=":64," ":65,"\t":66,"\r":67,"\n":68}
    var i = 0, d = {}, l = scheme.length;
    for (; i < l; i += 1) d[scheme[i]] = i;
    if (i <= 64) d["="] = 64;
    return d;
  }
  global.parseBase64SchemeForStringDecoding = parseBase64SchemeForStringDecoding;

}(this));
