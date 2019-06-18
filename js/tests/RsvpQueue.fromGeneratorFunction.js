(function script() {
  "use strict";

  /*! Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading RsvpQueue.fromGeneratorFunction.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "RsvpQueue"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running RsvpQueue.fromGeneratorFunction.js tests");

  /*jslint vars: true */
  var info = function () { console.info.apply(console, arguments); };
  var error = function () { console.error.apply(console, arguments); };
  function test(name, timeout, expected, testFn) {
    var res = [], timer, prefix = "RsvpQueue.fromGeneratorFunction";
    function end() {
      if (timer === undefined) return error("test `" + name + "`, `end` called twice");
      timer = clearTimeout(timer);  // timer should be set to undefined
      if (JSON.stringify(res) !== JSON.stringify(expected)) {
        error(prefix + " test: `" + name + "`, result `" + JSON.stringify(res) + "` !== `" + JSON.stringify(expected) + "` expected");
      }
    }
    timer = setTimeout(function () {
      try { if (typeof end.onbeforetimeout === "function") end.onbeforetimeout(); }
      catch (e) { error("test: " + name + ", error on before timeout ! `" + e + "`"); }
      if (timer === undefined) return;  // it has ended in before timeout
      error(prefix + " test: `" + name + "`, timeout ! result `" + JSON.stringify(res) + "` <-> `" + JSON.stringify(expected) + "` expected");
    }, timeout);
    setTimeout(function () {
      try { testFn(res, end); }
      catch (e) { error(prefix + " test: `" + name + "`, error ! result `" + e + "`"); }
    });
  }

  function deferred() { var d = {}; d.promise = new Promise(function (a, b) { d.resolve = a; d.reject = b; }); return d; }
  function sleep(ms) { return new Promise(function (resolve) { setTimeout(resolve, ms); }); }

  //////////////////////////////////////////////
  // RsvpQueue.fromGeneratorFunction tests
  test("should cancel the returned task", 1000, [], function (res, end) {
    var q = RsvpQueue.fromGeneratorFunction(function* () {
      return RsvpQueue.fromGeneratorFunction(function* () { yield; });
    });
    q.cancel();
    q.catch(end);
  });
  test("should not cancel before the non cancellable promise", 1000, [1], function (res, end) {
    var val = 0, task = RsvpQueue.fromGeneratorFunction(function* () {
      this.cancel();
      yield Promise.resolve().then(function () { val = 1; });
    });
    task.catch(function () {
      res.push(val);
      end();
    });
  });
  test("should fulfill before cancel", 1000, [1], function (res, end) {
    var task = RsvpQueue.fromGeneratorFunction(function* () {
      this.cancel();
      return Promise.resolve().then(function () { return 1; });
    });
    task.then(function (one) {
      res.push(one);
      end();
    });
  });
  test("how to use try catch with return in a task", 1000, ["errored"], function (res, end) {
    var task = RsvpQueue.fromGeneratorFunction(function* () {
      var ret;
      try {
        ret = yield Promise.reject("errored");
        return ret;  // because `return ret;` means the task is completed with `ret`
      } catch (reason) {
        res.push(reason);
      }
      // the best could be to put the return after the try catch.
    });
    task.then(end, end);
  });
  test("propagates error to the then", 1000, ["ok"], function (res, end) {
    RsvpQueue.fromGeneratorFunction(function* () {
      throw "ok";
    }).then(null, function (e) {
      res.push(e);
      end();
    });
  });
  test("how to be as synchronous as possible", 1000, ["start", "value 1", "tic end", "value 2", "value 3"], function (res, end) {
    // test preparation
    var i = 0;
    function* quick(v) { if (v && typeof v.then === "function") v = yield v; return v; }
    function sometimeAsync() { if ((i++) % 2) return Promise.resolve(i); return i; }
    // actual test
    RsvpQueue.fromGeneratorFunction(function* () {
      var v;
      res.push("start");
      v = yield* quick(sometimeAsync());
      res.push("value " + v);
      v = yield* quick(sometimeAsync());
      res.push("value " + v);
      v = yield* quick(sometimeAsync());
      res.push("value " + v);
      end();
    });
    res.push("tic end");
  });
  test("how to use defer to avoid cancellation before var assignment", 1000, ["defer close", "closer is closed"], function (res, end) {
    // test preparation
    var closerStatus = "not instanciated";
    var actualCloser = {close: function () { closerStatus = "closed"; }};
    var getCloserTask = function () { closerStatus = "not closed"; return Promise.resolve(actualCloser); };
    var defer = function (p, fn) { return p.then(fn, fn); }
    // actual test
    var closer, task = RsvpQueue.fromGeneratorFunction(function* () {
      var closerTask = getCloserTask();
      res.push("defer close");
      defer(this, function () { closerTask.then(function (closer) { closer.close(); }); });
      closer = yield closerTask;
      res.push("task bottom - task should be cancelled");
    });
    task.cancel();
    // test end
    end.onbeforetimeout = function () {
      res.push("closer is " + closerStatus);
      end();
    };
  });

}());
