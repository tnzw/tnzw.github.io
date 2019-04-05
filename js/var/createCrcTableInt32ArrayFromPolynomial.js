this.createCrcTableInt32ArrayFromPolynomial = (function script() {
  "use strict";

  /*! createCrcTableInt32ArrayFromPolynomial.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createCrcTableInt32ArrayFromPolynomial(int32) {
    // https://simplycalc.com/crc32-source.php
    polynomial = polynomial|0;
    var table = new Array(256), i = 0, j = 0, n = 0;
    for (; i < 256; i = (i + 1)|0) {
      n = i;
      for (j = 0; j < 8; j = (j + 1)|0) {
        if (n & 1) n = (n >>> 1) ^ polynomial;
        else       n =  n >>> 1;
      }
      table[i] = n;
    }
    return table;
  }
  createCrcTableInt32ArrayFromPolynomial.toScript = function () { return "(" + script.toString() + "())"; };
  return createCrcTableInt32ArrayFromPolynomial;

}());
