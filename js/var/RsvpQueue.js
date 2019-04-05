this.RsvpQueue = (function script() {
  "use strict";

  /*! RsvpQueue.js Version 1.4.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // Trick with Queues
  // 
  //   loop:
  // .then(function () {
  //   return new RsvpQueue(function loop(previousReturnedValue) {
  //     // do some synchronous code
  //     // [..]
  //     if (someCondition) return doLastThingAsyncOrNot();  // stop loop
  //     this.push(loop);  // continue loop
  //     return doThingAsyncOrNot();
  //   });
  // });

  function RsvpQueue(executor) {
    var it = this,
        resolve = null, reject = null,
        g = it._queue = [],
        o = {method: 0, prev: undefined};
    function magicPromise() {
      var res = null, promise = new Promise(function (r) { res = r; });
      promise.cancel = res;
      promise.resume = res;
      return promise;
    }
    function end(method, value) { it._queueEnd = true; method(value); }
    function recthen(v) { o.method = 0; o.prev = v; rec(); }
    function recfail(v) { o.method = 1; o.prev = v; rec(); }
    function rec() {
      if (g.length === 0) return end(o.method === 0 ? resolve : reject, o.prev);
      if (it._cancelled) { g = new Error("queue cancelled"); return end(reject, g); }
      if (it._paused) { (it._pending = magicPromise()).then(rec); return; }
      var next;
      try { next = g.splice(0, 2)[o.method].call(it, o.prev); o.method = 0; }
      catch (e) { next = e; o.method = 1; }
      it._pending = next;
      if (next && typeof next.then === "function") {
        if (it._cancelled && typeof next.cancel === "function") { try { next.cancel(); } catch (e) { return end(reject, e); } }
        if (it._paused && typeof next.pause === "function") { try { next.pause(); } catch (e) { return end(reject, e); } }
        next.then(recthen, recfail);
      } else
        Promise.resolve(o.prev = next).then(rec);
    }
    it._promise = new Promise(function (res, rej) { resolve = res; reject = rej; });
    if (typeof executor === "function") { it._queue.push(executor, null); rec(); }
    else Promise.resolve().then(rec);
  }
  RsvpQueue.prototype.then = function (fnOnResolve, fnOnReject) { return this._promise.then(fnOnResolve, fnOnReject); };
  RsvpQueue.prototype.catch = function (fnOnReject) { return this.then(null, fnOnReject); };
  RsvpQueue.prototype.push = function (fnOnResolve, fnOnReject) {
    if (this._queueEnd) throw new Error("queue ended");
    this._queue.push(fnOnResolve, fnOnReject);
    return this;
  };
  RsvpQueue.prototype.enqueue = RsvpQueue.prototype.push;
  RsvpQueue.prototype.cancel = function () {
    var p = this._pending;
    this._cancelled = true;
    if (p && typeof p.then === "function" && typeof p.cancel === "function") p.cancel();
    return this;
  };
  RsvpQueue.prototype.pause = function () {
    var p = this._pending;
    this._paused = true;
    if (p && typeof p.then === "function" && typeof p.pause === "function") p.pause();
    return this;
  };
  RsvpQueue.prototype.resume = function () {
    var p = this._pending;
    delete this._paused;
    if (p && typeof p.then === "function" && typeof p.resume === "function") p.resume();
    return this;
  };

  RsvpQueue.resolve = function (value) {
    return new RsvpQueue(function () { return value; });
  };
  RsvpQueue.reject = function (value) {
    return new RsvpQueue(function () { throw value; });
  };
  RsvpQueue.all = function (promises) {
    // Acts like Promise.all except that it propagates `cancel` and `pause`
    return new RsvpQueue._All(promises);
  };
  RsvpQueue.race = function (promises) {
    // Acts like Promise.race except that it propagates `cancel` and `pause`
    return new RsvpQueue._Race(promises);
  };
  RsvpQueue.wait = function (promises) {
    // Acts like RsvpQueue.all except that it does not propagate `cancel` and `pause`
    return new RsvpQueue._Wait(promises);
  };
  RsvpQueue.selectAll = function (promises) {  // XXX test it !
    // acts like RsvpQueue.all except that it cancel on failure 
    return new RsvpQueue._SelectAll(promises);
  };
  RsvpQueue.select = function (promises) {
    // acts like RsvpQueue.race except that it cancel losers
    return new RsvpQueue._Select(promises);
  };

  function RsvpQueuePromisesBase() {}
  RsvpQueuePromisesBase.prototype.then = function (fnOnResolve, fnOnReject) { return this._promise.then(fnOnResolve, fnOnReject); };
  RsvpQueuePromisesBase.prototype.catch = function (fnOnReject) { return this.then(null, fnOnReject); };
  RsvpQueuePromisesBase.prototype.cancel = function () {
    if (this._promises)
      for (var i = 0, p = null, a = this._promises; i < a.length; i += 1)
        if ((p = a[i]) && typeof p.then === "function" && typeof p.cancel === "function")
          p.cancel();  // XXX handle error ?
    return this;
  };
  RsvpQueuePromisesBase.prototype.pause = function () {
    if (this._promises)
      for (var i = 0, p = null, a = this._promises; i < a.length; i += 1)
        if ((p = a[i]) && typeof p.then === "function" && typeof p.pause === "function")
          p.pause();  // XXX handle error ?
    return this;
  };
  RsvpQueuePromisesBase.prototype.resume = function () {
    if (this._promises)
      for (var i = 0, p = null, a = this._promises; i < a.length; i += 1)
        if ((p = a[i]) && typeof p.then === "function" && typeof p.resume === "function")
          p.resume();  // XXX handle error ?
    return this;
  };
  RsvpQueue._PromisesBase = RsvpQueuePromisesBase;

  function RsvpQueueAll(promises) {
    var ths = this;
    this._promise = new Promise(function (resolve, reject) {
      var i = 0, p = null, count = promises.length, a = ths._promises = new Array(count);
      function mksolver(j) {
        return function (v) { a[j] = v; if (count === 1) resolve(a); else count -= 1; };
      }
      function mkrejecter(j) {
        return function (v) { a[j] = null; if (count > 0) { count = 0; reject(v); } };
      }
      for (; i < promises.length; i += 1) {
        if ((p = a[i] = promises[i]) && typeof p.then === "function") p.then(mksolver(i), mkrejecter(i));
        else count -= 1;
      }
      if (count === 0) resolve(a);
    });
  }
  RsvpQueueAll.prototype = Object.create(RsvpQueuePromisesBase.prototype);
  RsvpQueue._All = RsvpQueueAll;

  function RsvpQueueRace(promises) {
    var ths = this;
    this._promise = new Promise(function (resolve, reject) {
      var i = 0, a = ths._promises = new Array(promises.length), tmp = null, ongoing = true;
      function mksolver(j) {
        return function (v) { a[j] = v; if (ongoing) { ongoing = false; resolve(v); } };
      }
      function mkrejecter(j) {
        return function (v) { a[j] = null; if (ongoing) { ongoing = false; reject(v); } };
      }
      for (; i < promises.length; i += 1)
        if ((a[i] = promises[i]) && typeof a[i].then === "function") a[i].then(mksolver(i), mkrejecter(i));
        else if (ongoing) { ongoing = false; tmp = a[i]; }
      if (ongoing === false) resolve(tmp);
    });
  }
  RsvpQueueRace.prototype = Object.create(RsvpQueuePromisesBase.prototype);
  RsvpQueue._Race = RsvpQueueRace;

  function RsvpQueueWait(promises) {
    var ths = this, oncancel = null;
    this._promise = new Promise(function (resolve, reject) {
      var i = 0, p = null, count = promises.length, a = ths._promises = new Array(count);
      function mksolver(j) {
        return function (v) { a[j] = v; if (count === 1) resolve(a); else count -= 1; };
      }
      function mkrejecter(j) {
        return function (v) { a[j] = null; if (count > 0) { count = 0; reject(v); } };
      }
      for (; i < promises.length; i += 1) {
        if ((p = a[i] = promises[i]) && typeof p.then === "function") p.then(mksolver(i), mkrejecter(i));
        else count -= 1;
      }
      if (count === 0) resolve(a);
      oncancel = function () { if (count > 0) { count = 0; reject("wait cancelled"); } };
    });
    this._promise.cancel = oncancel;
  }
  RsvpQueueWait.prototype.then = function (fnOnResolve, fnOnReject) { return this._promise.then(fnOnResolve, fnOnReject); };
  RsvpQueueWait.prototype.catch = function (fnOnReject) { return this.then(null, fnOnReject); };
  RsvpQueueWait.prototype.cancel = function () {
    this._promise.cancel();
    return this;
  };
  RsvpQueue._Wait = RsvpQueueWait;

  function RsvpQueueSelectAll(promises) {  // allOrCancel
    var ths = this;
    this._promise = new Promise(function (resolve, reject) {
      var i = 0, p = null, count = promises.length, a = ths._promises = new Array(count);
      function mksolver(j) {
        return function (v) { a[j] = v; if (count === 1) resolve(a); else count -= 1; };
      }
      function mkrejecter(j) {
        return function (v) {
          var k = 0, q = null;
          a[j] = v;
          if (count > 0) {
            count = 0;
            reject(v);
            for (; k < a.length; k += 1)
              if (j !== k && (q = a[k]) && typeof q.then === "function" && typeof q.cancel === "function")
                q.cancel();  // XXX handle error ?
          }
        };
      }
      for (; i < promises.length; i += 1) {
        if ((p = a[i] = promises[i]) && typeof p.then === "function") p.then(mksolver(i), mkrejecter(i));
        else count -= 1;
      }
      if (count === 0) resolve(a);
      oncancel = function () { if (count > 0) { count = 0; reject("selectAll cancelled"); } };
    });
    this._promise.cancel = oncancel;
  }
  RsvpQueueSelectAll.prototype = Object.create(RsvpQueuePromisesBase.prototype);
  RsvpQueue._SelectAll = RsvpQueueSelectAll;

  function RsvpQueueSelect(promises) {  // raceAndCancel
    var ths = this;
    this._promise = new Promise(function (resolve, reject) {
      var i = 0, a = ths._promises = new Array(promises.length), s = true;
      // XXX do mksolver and mkrejecter like the others ! done, please review
      function mksolver(j) {
        return function (v) {
          var k = 0, q = null;
          a[j] = v;
          if (s) {
            s = false;
            resolve(v);
            for (; k < a.length; k += 1)
              if (j !== k && (q = a[k]) && typeof q.then === "function" && typeof q.cancel === "function")
                q.cancel();  // XXX handle error ?
          }
        };
      }
      function mkrejecter(j) {
        return function (v) {
          var k = 0, q = null;
          a[j] = v;
          if (s) {
            s = false;
            reject(v);
            for (; k < a.length; k += 1)
              if (j !== k && (q = a[k]) && typeof q.then === "function" && typeof q.cancel === "function")
                q.cancel();  // XXX handle error ?
          }
        };
      }
      for (; i < promises.length; i += 1) a[i] = promises[i];
      for (i = 0; i < a.length; i += 1) {
        if (a[i] && typeof a[i].then === "function") {}
        else return mksolver(i)(a[i]);
      }
      for (i = 0; i < a.length; i += 1)
        a[i].then(mksolver(i), mkrejecter(i));
    });
  }
  RsvpQueueSelect.prototype = Object.create(RsvpQueuePromisesBase.prototype);
  RsvpQueue._Select = RsvpQueueSelect;

  RsvpQueue.fromGeneratorFunction = function (gf) {
    // RsvpQueue.fromGeneratorFunction(function* () {
    //   result = yield doAsyncThing(); 
    //   return result + 1;
    // });
    return new RsvpQueue(function () {
      var q = this, g = gf.call(q);
      function next(v) { return h(g.next(v)); }
      function thrw(v) { return h(g.throw(v)); }
      function h(d) {
        if (d.done) return d.value;
        q.push(next, thrw);
        return d.value;
      }
      return next();
    });
  };

  RsvpQueue.toScript = function () { return "(" + script.toString() + "())"; };
  return RsvpQueue;

}());
