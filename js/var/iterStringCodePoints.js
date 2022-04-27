this.iterStringCodePoints = (function script() {
  "use strict";

  /*! iterStringCodePoints.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function StringCodePointIterator(string) { this.index = 0; this.string = string }
  StringCodePointIterator.prototype.next = function () {
    var c = 0, c2 = 0, i = this.index, string = this.string, size = string.length;
    // https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Global_Objects/String/codePointAt
    if (i >= size) return {value: undefined, done: true};
    c = string.charCodeAt(i);
    if ( // check if it’s the start of a surrogate pair
      c >= 0xD800 && c <= 0xDBFF && // high surrogate
      size > i + 1 // there is a next code unit
    ) {
      c2 = string.charCodeAt(i + 1);
      if (c2 >= 0xDC00 && c2 <= 0xDFFF) { // low surrogate
        // https://mathiasbynens.be/notes/javascript-encoding#surrogate-formulae
        this.index += 2;
        return {value: (c - 0xD800) * 0x400 + c2 - 0xDC00 + 0x10000, done: false};
      }
    }
    this.index += 1;
    return {value: c, done: false};
  };

  function iterStringCodePoints(string) {
    // `for (let chars of string)` do the job
    // but for vanilla js, here's the code
    return new StringCodePointIterator(string);
  }
  iterStringCodePoints.StringCodePointIterator = StringCodePointIterator;
  iterStringCodePoints.toScript = function () { return "(" + script.toString() + "())"; };
  return iterStringCodePoints;

}());
