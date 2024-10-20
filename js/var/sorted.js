this.sorted = (function script() {
  "use strict";

  /*! sorted.js Version 1.1.0

      Copyright (c) 2021, 2024 <tnzw@github.triton.ovh>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function keyToCmp(callable) { return function (a, b) { a = callable(a); b = callable(b); return a < b ? -1 : a > b ? 1 : 0; } }

  function sorted(iterable, key, reverse) {
    if (key == null) return Array.from(iterable).sort(reverse ? ((a, b) => b < a ? -1 : b > a ? 1 : 0) : null);
    iterable = Array.from(iterable, v => [key(v), v]).sort(reverse ? ((a, b) => b[0] < a[0] ? -1 : b[0] > a[0] ? 1 : 0) : ((a, b) => a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : 0));
    iterable.forEach((v, i, a) => a[i] = v[1]);
    return iterable;
  }
  sorted.keyToCmp = keyToCmp;
  sorted.toScript = function () { return "(" + script.toString() + "())"; };
  return sorted;

}());
