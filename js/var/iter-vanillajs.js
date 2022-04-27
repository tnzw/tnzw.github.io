this.iter = (function script() {
  "use strict";

  /*! iter-vanillajs.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function Iterator(object) { this.index = 0; this.object = object }
  Iterator.prototype.next = function () {
    var len = this.object.length;
    if (typeof len === "number" && this.index < len)
      return {value: this.object[this.index++], done: false};
    return {value: undefined, done: true};
  };
  //try { Iterator.prototype[Symbol.iterator] = function () { return this } } catch (_) {}

  function IteratorSentinel(iterator, sentinel) { this.iterator = iterator; this.sentinel = sentinel }
  IteratorSentinel.prototype.next = function () {
    var o = next(this.iterator);
    if (o.done) return o;
    if (o.value === this.sentinel) return {value: undefined, done: true};
    return o;
  };
  //try { IteratorSentinel.prototype[Symbol.iterator] = function () { return this } } catch (_) {}

  function iter(iterable, sentinel) {
    var it = undefined;
    try { it = iterable[Symbol.iterator] } catch (_) {}
    if (typeof it === "function")
      if (arguments.length > 1) return new IteratorSentinel(it.call(iterable), sentinel);
      return it.call(iterable);
    if (iterable !== undefined && iterable !== null) {
      // if (typeof iterable.next === "function") {
      //   if (arguments.length > 1) return new IteratorSentinel(iterable, sentinel);
      //   return iterable;
      // }
      if (typeof iterable.length === "number") {
        if (arguments.length > 1) return new IteratorSentinel(new Iterator(iterable), sentinel);
        return new Iterator(iterable);
      }
    }
    throw new TypeError((typeof iterable) + " is not iterable");
  }
  iter.Iterator = Iterator;
  iter.IteratorSentinel = IteratorSentinel;
  iter.toScript = function () { return "(" + script.toString() + "())"; };
  iter._requiredGlobals = ["next"];
  return iter;

}());
