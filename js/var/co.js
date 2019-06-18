this.co = (function script() {
  "use strict";

  /*! co.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function co(gfn) {
    // co(fn*).then( val => )
    return new Promise(function (resolve, reject) {
      var g = null, done = false, method = resolve;
      function recthen(v) { method = resolve; rec(v); }
      function recfail(v) { method = reject; rec(v); }
      function rec(prev) {
        var next = null;
        if (done)
          return method(prev);
        try {
          next = method === resolve ? g.next(prev) : g.throw(prev);
          method = resolve; done = next.done; next = next.value;
        } catch (e) {
          method = reject; done = true; next = e;
        }
        if (next && typeof next.then === "function")
          next.then(recthen, recfail);
        else
          Promise.resolve(next).then(rec);
      }
      try { g = gfn.call(this); } catch (e) { reject(e); return; }
      rec();
    });
  }
  co.wrap = function (gfn) {
    // var fn = co.wrap(fn*)
    return function () { return co(_=>gfn.apply(this, arguments)); };
  };

  co.toScript = function () { return "(" + script.toString() + "())"; };
  return co;

}());
