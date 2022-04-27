this.iter = (function script() {
  "use strict";

  /*! iter.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function iter(iterable, sentinel) {
    // iter() is not a generator because it should raise immediatly if iterable is not iterable
    var i;
    if (arguments.length > 1) {
      return (function* (it) {
        for (let _ of {[Symbol.iterator]: _ => it}) {
          if (sentinel === _) return;
          yield _;
        }
      })(iter(iterable));
    }
    try { i = iterable[Symbol.iterator] } catch (_) {}
    if (typeof i === "function") return i.call(iterable);
    //if (iterable !== undefined && iterable !== null && typeof iterable.next === "function") return iterable;  // here iterable is an iterator
    throw new TypeError(iterable + " is not iterable");
  }
  iter.toScript = function () { return "(" + script.toString() + "())"; };
  return iter;

}());
