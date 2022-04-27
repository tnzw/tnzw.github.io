this.imap = (function script() {
  "use strict";

  /*! imap-vanillajs.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function MapIterator(mapper, iterator, condition) { this.mapper = mapper; this.iterator = iterator; this.condition = condition }
  MapIterator.prototype.next = function () {
    var o = next(this.iterator);
    while (!o.done) {
      if (this.condition) {
        if (this.condition(o.value)) return {value: this.mapper(o.value), done: false};
      } else return {value: this.mapper(o.value), done: false};
      o = next(this.iterator);
    }
    return o;
  };
  //try { MapIterator.prototype[Symbol.iterator] = function () { return this } } catch (_) {}

  function imap(mapper, iterable, condition) {
    // Can do pythonic like list comprehension
    //   [i + 1 for i in iterable if i > 5]
    //   Array.from(imap(i => i + 1, iterable, i => i > 5))
    return new MapIterator(mapper, iter(iterable), condition);
  }
  imap.MapIterator = MapIterator;
  imap.toScript = function () { return "(" + script.toString() + "())"; };
  imap._requiredGlobals = ["iter", "next"];
  return imap;

}());
