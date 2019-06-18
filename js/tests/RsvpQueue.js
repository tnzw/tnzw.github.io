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
    console.log("loading RsvpQueue.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "RsvpQueue"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running RsvpQueue.js tests");

  /*jslint vars: true */
  var info = function () { console.info.apply(console, arguments); };
  var error = function () { console.error.apply(console, arguments); };
  function test(name, timeout, expected, testFn) {
    var res = [], timer;
    function end() {
      if (timer === undefined) return error("test `" + name + "`, `end` called twice");
      timer = clearTimeout(timer);  // timer should be set to undefined
      if (JSON.stringify(res) !== JSON.stringify(expected)) {
        error("test `" + name + "`, result `" + JSON.stringify(res) + "` !== `" + JSON.stringify(expected) + "` expected");
      }
    }
    timer = setTimeout(function () {
      try { if (typeof end.onbeforetimeout === "function") end.onbeforetimeout(); }
      catch (e) { error("test: " + name + ", error on before timeout ! `" + e + "`"); }
      if (timer === undefined) return;  // it has ended in before timeout
      error("test `" + name + "`, timeout ! result `" + JSON.stringify(res) + "` <-> `" + JSON.stringify(expected) + "` expected");
    }, timeout);
    setTimeout(function () {
      try { testFn(res, end); }
      catch (e) { error("test `" + name + "`, error ! result `" + e + "`"); }
    });
  }

  function deferred() { var d = {}; d.promise = new Promise(function (a, b) { d.resolve = a; d.reject = b; }); return d; }
  function sleep(ms) { return new Promise(function (resolve) { setTimeout(resolve, ms); }); }

  //////////////////////////////////////////////
  // RsvpQueue tests
  test("RsvpQueue: should be enqueuable before next tick", 1000, ["enqueued"], function (res, end) {
    var q = new RsvpQueue();
    q.push(function () {
      res.push("enqueued");
      end();
    });
  });
  test("RsvpQueue: cannot enqueue after fulfillment", 1000, ["queue ended"], function (res, end) {
    var q = new RsvpQueue();
    q.then(function () {
      try {
        q.push(function () { res.push("+ call !"); });
        res.push("queue enqueued");
      } catch (reason) { res.push(reason.message); }
    }).then().then(end);
  });

  test("RsvpQueue: propagates error to the then", 1000, ["ok"], function (res, end) {
    new RsvpQueue(function () {
      throw "ok";
    }).then(null, function (e) {
      res.push(e);
      end();
    });
  });


  test("RsvpQueue: should cancel the returned queue", 1000, [], function (res, end) {
    var q = new RsvpQueue(function () {
      return new RsvpQueue(function () {}).push(function () {});
    });
    q.cancel();
    q.catch(end);
  });
  test("RsvpQueue: should not cancel before the non cancellable promise", 1000, [1], function (res, end) {
    var val = 0, q = new RsvpQueue(function () {
      this.cancel();
      return Promise.resolve().then(function () { val = 1; });
    }).push(function () {});
    q.catch(function () {
      res.push(val);
      end();
    });
  });
  test("RsvpQueue: should fulfill before cancel", 1000, [1], function (res, end) {
    var q = new RsvpQueue(function () {
      this.cancel();
      return Promise.resolve().then(function () { return 1; });
    });
    q.then(function (one) {
      res.push(one);
      end();
    });
  });
  test("RsvpQueue: how to use defer to avoid cancellation before var assignment", 1000, ["defer close", "closer is closed"], function (res, end) {
    // test preparation
    var closerStatus = "not instanciated";
    var actualCloser = {close: function () { closerStatus = "closed"; }};
    var getCloserTask = function () { closerStatus = "not closed"; return Promise.resolve(actualCloser); };
    var defer = function (p, fn) { return p.then(fn, fn); }
    // actual test
    var closer, q = new RsvpQueue(function () {
      var closerTask = getCloserTask();
      res.push("defer close");
      defer(this, function () { closerTask.then(function (closer) { closer.close(); }); });
      return closerTask;
    }).push(function (_closer) {
      closer = _closer;
      res.push("queue bottom - queue should be cancelled");
    });
    q.cancel();
    // test end
    end.onbeforetimeout = function () {
      res.push("closer is " + closerStatus);
      end();
    };
  });

  test("RsvpQueue: all should propagate cancel", 1000, ["closed", "closed"], function (res, end) {
    // test preparation
    function mkdefer() {
      var d = deferred();
      d.promise.cancel = function () { d.closed = "closed"; d.reject(); };
      d.closed = "not closed";
      return d;
    }
    // actual test
    var one = mkdefer(), three = mkdefer();
    var q = RsvpQueue.all([
      one.promise,
      three.promise,
    ]);
    q.cancel();
    q.catch(function () {
      res.push(one.closed, three.closed);
      end();
    });
  });
  test("RsvpQueue: race should propagate cancel", 1000, ["closed", "closed"], function (res, end) {
    // test preparation
    function mkdefer() {
      var d = deferred();
      d.promise.cancel = function () { d.closed = "closed"; d.reject(); };
      d.closed = "not closed";
      return d;
    }
    // actual test
    var one = mkdefer(), three = mkdefer();
    var q = RsvpQueue.race([
      one.promise,
      three.promise,
    ]);
    q.cancel();
    q.catch(function () {
      res.push(one.closed, three.closed);
      end();
    });
  });
  // No
  /*test("RsvpQueue: race should not cancel if already won ?", 1000, ["not closed", "wins", "not closed"], function (res, end) {
    // test preparation
    function mkdefer() {
      var d = deferred();
      d.promise.cancel = function () { d.closed = "closed"; d.reject(); };
      d.closed = "not closed";
      return d;
    }
    // actual test
    var one = mkdefer(), three = mkdefer();
    var q = RsvpQueue.race([
      one.promise,
      "wins",
      three.promise,
    ]);
    q.cancel();
    q.then(function (value) {
      res.push(one.closed, value || "failed to win", three.closed);
      end();
    });
  });*/
  test("RsvpQueue: race should not cancel loosers just after first wins", 1000, ["not closed", "wins", "not closed"], function (res, end) {
    // test preparation
    function mkdefer() {
      var d = deferred();
      d.promise.cancel = function () { d.closed = "closed"; };
      d.closed = "not closed";
      return d;
    }
    // actual test
    var one = mkdefer(), three = mkdefer();
    RsvpQueue.race([
      one.promise,
      "wins",
      three.promise,
    ]).then(function (value) {
      res.push(one.closed, value || "failed to win", three.closed);
      end();
    });
  });
  test("RsvpQueue: select should cancel loosers just after first wins", 1000, ["closed", "wins", "closed"], function (res, end) {
    // test preparation
    function mkdefer() {
      var d = deferred();
      d.promise.cancel = function () { d.closed = "closed"; };
      d.closed = "not closed";
      return d;
    }
    // actual test
    var one = mkdefer(), three = mkdefer();
    RsvpQueue.select([
      one.promise,
      "wins",
      three.promise,
    ]).then(function (value) {
      res.push(one.closed, value || "failed to win", three.closed);
      end();
    });
  });
  test("RsvpQueue: wait should not cancel waiting promises", 1000, ["not closed", "not closed"], function (res, end) {
    // test preparation
    function mkdefer() {
      var d = deferred();
      d.promise.cancel = function () { d.closed = "closed"; };
      d.closed = "not closed";
      return d;
    }
    // actual test
    var one = mkdefer(), three = mkdefer();
    var q = RsvpQueue.wait([
      one.promise,
      "wins",
      three.promise,
    ])
    q.cancel();
    q.catch(function () {
      res.push(one.closed, three.closed);
      end();
    });
  });

}());
