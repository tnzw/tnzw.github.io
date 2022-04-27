this.next = (function script() {
  "use strict";

  /*! next.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function next(iterator, defaut) {
    var o = iterator.next();
    // test: for (let _ of ({[Symbol.iterator]: _ => ({next(){ return X }})})) console.log(_);
    // https://developer.mozilla.org/en-US/docs/Glossary/Primitive
    switch (typeof o) { default: if (o !== null) break; case "undefined": case "boolean": case "number": case "string": case "symbol": case "bigint": throw new TypeError("Iterator result " + o + " is not an object"); }
    if (arguments.length > 1 && o.done) return {value: defaut, done: false};
    return o;
  }
  next.toScript = function () { return "(" + script.toString() + "())"; };
  return next;

}());
