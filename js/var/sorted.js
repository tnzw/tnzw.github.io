this.sorted = (function script() {
  "use strict";

  /*! sorted.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function keyToCmp(callable) { return function (a, b) { a = callable(a); b = callable(b); return a < b ? -1 : a > b ? 1 : 0; } }

  function sorted(iterable, key) {
    iterable = Array.from(iterable);
    if (key !== undefined) iterable.sort(keyToCmp(key));
    else iterable.sort();
    return iterable;
  }
  sorted.keyToCmp = keyToCmp;
  sorted.toScript = function () { return "(" + script.toString() + "())"; };
  return sorted;

}());
