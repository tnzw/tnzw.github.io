this.partition = (function script() {
  "use strict";

  /*! partition.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createReplacerMatch() {
    // arguments : match, p1, p2, ..., offset, string, groups
    // returns [ match, p1, p2, ..., index: offset, input: string, groups: groups ]
    var a = [], i = 0, n = 0, m = null;
    for (; i < arguments.length; ++i)
      a.push(arguments[i]);
    for (; i > 0; --i)
      if (typeof a[i] === "number")
        break;
    m = a.slice(0, i);
    m.index = a[i] || 0;
    m.input = a[i + 1];
    m.groups = a[i + 2];
    return m;
  }
  function partition(string, sep, replacer) {
    // partition(string, sep[, replacer])
    // partition("abcba", /b/g) is similar to partition("abcba", /b/g, m=>m[0])
    var _ = [], l = 0;
    string.replace(sep, function () {
      var m = createReplacerMatch.apply(null, arguments), i = m.index;
      _.push(string.slice(l, i), replacer ? replacer(m) : m[0]);
      l = i + m[0].length;
    });
    _.push(string.slice(l));
    return _;
  }
  partition.createReplacerMatch = createReplacerMatch;
  partition.toScript = function () { return "(" + script.toString() + "())"; };
  return partition;

})();
