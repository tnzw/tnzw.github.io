this.setEventNextTick = (function script() {
  "use strict";

  /*! createPasswordMagicEventListener.js Version 1.0.0-1

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function setEventNextTick(callback) {
    // priority: Promise ticks, setEventNextTick ticks, DOM event ticks, setTimeout/setInterval ticks

    var originalThen = null, args = null, i = 0;
    if (typeof callback !== "function") { return; }
    if ((setEventNextTick._eventTickCount|0) === 0) {
      originalThen = Promise.prototype.then;
      Promise.prototype.then = function (onfulfilled, onrejected) {
        function one(v) { setEventNextTick._promiseTickNumber = ((setEventNextTick._promiseTickNumber|0) + 1)|0; return typeof onfulfilled === "function" ? onfulfilled(v) : v; }
        function two(v) { setEventNextTick._promiseTickNumber = ((setEventNextTick._promiseTickNumber|0) + 1)|0; return typeof onrejected  === "function" ? onrejected(v)  : v; }
        return originalThen.call(this, one, two);
      };
      Promise.prototype.catch = function (onrejected) { this.then(undefined, onrejected); };
    }
    if (!setEventNextTick._promise) { setEventNextTick._promise = Promise.resolve(); }
    //setEventNextTick._eventTickCount = ((setEventNextTick._eventTickCount|0) + 1)|0;
    setEventNextTick._eventTickCount = -1;

    args = new Array(arguments.length - 1);
    for (; i < arguments.length; i = (i + 1)|0) { args[(i - 1)|0] = arguments[i]; }
    function run() {
      if ((setEventNextTick._eventTickNumber|0) === (setEventNextTick._promiseTickNumber|0))
        throw new Error("Promise class seems not overriden!");
      if ((setEventNextTick._eventTickNumber|0) === (((setEventNextTick._promiseTickNumber|0) - 1)|0)) {
        //setEventNextTick._eventTickCount = ((setEventNextTick._eventTickCount|0) - 1)|0;
        return callback.apply(this, args);
      }
      setEventNextTick._eventTickNumber = setEventNextTick._promiseTickNumber|0;
      setEventNextTick._promise = setEventNextTick._promise.then(run, run);
    }
    setEventNextTick._promise = setEventNextTick._promise.then(run, run);
  }

  setEventNextTick._promise = null;
  setEventNextTick._promiseTickNumber = 0;
  setEventNextTick._eventTickNumber = 0;
  setEventNextTick._eventTickCount = 0;

  setEventNextTick.toScript = function () { return "(" + script.toString() + "())"; };
  setEventNextTick._requiredGlobals = ["Promise"];
  return setEventNextTick;

  // XXX Test it !
  //this.setEventNextTick(function () {
  //  console.log(1);
  //  Promise.resolve().then(_=>console.log(3)).then().then(_=>console.log(4));
  //  console.log(2);
  //});
  //this.setEventNextTick(function () {
  //  console.log(5);
  //});

}());
