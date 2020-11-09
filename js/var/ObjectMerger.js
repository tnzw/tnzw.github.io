this.ObjectMerger = (function script() {
  "use strict";

  /*! ObjectMerger.js Version 1.0.0

      Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // new ObjectMerger().merge(a, b);

  // om = new ObjectMerger();
  // r = om.merge(a={a:1,b:2},b={b:3}); -> {a:1,b:3} (r === a)

  // om = new ObjectMerger();
  // om.objectObjectMerger = ObjectMerger.anyAnyReference;
  // r = om.merge(a={a:1,b:2},b={b:3}); -> {b:3} (r === b)

  // om = new ObjectMerger();
  // r = om.merge(a=[1,2,3],b=[4,5]); -> [4,5] (r === b)

  // om = new ObjectMerger();
  // om.anyArrayMerger = ObjectMerger.anyArrayMerge
  // om.arrayArrayMerger = ObjectMerger.arrayArrayMerge
  // r = om.merge(a=[1,2,3],b=[4,5]); -> [4,5,3] (r === a)

  // om = new ObjectMerger();
  // om.anyArrayMerger = ObjectMerger.anyArrayMerge
  // om.arrayArrayMerger = ObjectMerger.arrayArrayExtend
  // r = om.merge(a=[1,2,3],b=[4,5],c=[6]); -> [1,2,3,4,5,6] (r === a)

  function ObjectMerger() {}
  ObjectMerger.prototype.merge = function (first) {
    var i = 1, k, kf, ka;
    if (arguments.length === 0) return undefined;
    function cap(s) { return s.slice(0,1).toUpperCase() + s.slice(1).toLowerCase(); }
    for (; i < arguments.length; i++) {
      kf = this.typeof(first).toLowerCase();
      ka = cap(this.typeof(arguments[i]));
      k = kf + ka + "Merger";
      console.log(k, first, arguments[i]);
      if (this[k]) { first = this[k](first, arguments[i]); continue; }
      k = "any" + ka + "Merger";
      console.log(k, first, arguments[i]);
      if (this[k]) { first = this[k](first, arguments[i]); continue; }
      console.log("anyAnyMerger", first, arguments[i]);
      first = this.anyAnyMerger(first, arguments[i]);
    }
    return first;
  };
  ObjectMerger.prototype.typeof = function (o) {
    if (o === undefined) return "undefined";
    if (o === null) return "null";
    if (Array.isArray(o)) return "array";
    // symbol
    // function
    // string
    // number (int, float, NaN, Infinity)
    // boolean
    // ...
    return typeof o;
  };
  ObjectMerger.anyAnyReference = function (a, b) { return b; };
  ObjectMerger.anyArrayCopy = function (a, b) { a = []; a.push.apply(a, b); return a; };
  //ObjectMerger.anyArrayMerge = function (a, b) { a = []; for (let v of b) a.push(this.merge(undefined, v)); return a; };
  ObjectMerger.anyArrayMerge = function (a, b) { return this.merge([], b); };
  ObjectMerger.arrayArrayMerge = function (a, b) { for (let i = 0; i < b.length; i++) a[i] = this.merge(a[i], b[i]); return a; };
  ObjectMerger.arrayArrayExtend = function (a, b) { for (let v of b) a.push(this.merge(undefined, v)); return a; };
  ObjectMerger.anyObjectMerge = function (a, b) { return this.merge({}, b); };
  ObjectMerger.objectObjectMerge = function (a, b) { for (let k of Object.keys(b)) a[k] = this.merge(a[k], b[k]); return a; };
  ObjectMerger.prototype.anyAnyMerger = ObjectMerger.anyAnyReference;
  ObjectMerger.prototype.anyObjectMerger = ObjectMerger.anyObjectMerge;
  ObjectMerger.prototype.objectObjectMerger = ObjectMerger.objectObjectMerge;
  ObjectMerger.prototype.anyArrayMerger = ObjectMerger.anyArrayCopy;

  ObjectMerger.toScript = function () { return "(" + script.toString() + "())"; };
  return ObjectMerger;

}());
