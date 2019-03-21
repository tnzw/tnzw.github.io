(function (global) {
  "use strict";

  /*! parseBase64SchemeForStringEncoding.js Version 0.1.7

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function parseBase64SchemeForStringEncoding(scheme) {
    // scheme = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" +
    //          "="  // padding (optional)
    // returns ["A","B",...,"+","/","="]
    var i = 0, l = scheme.length, a = new Array(l);
    for (; i < l; i += 1) a[i] = scheme[i];
    if (i <= 64) a[64] = "=";
    return a;
  }
  global.parseBase64SchemeForStringEncoding = parseBase64SchemeForStringEncoding;

}(this));
