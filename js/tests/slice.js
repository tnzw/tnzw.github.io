(function script() {
  "use strict";

  /*! slice.js version 0.1.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // inspire test with : https://github.com/minimaxir/big-list-of-naughty-strings/blob/master/blns.txt

  const MODULE = "slice.js";

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log(`loading ${MODULE} dependencies`);
    return loadVarScripts(
      {baseUrl: "../var/"},
      "slice",
    ).then(script, function (e) { console.error(e); });
  }
  console.log(`running ${MODULE} tests`);

  var info = function () { console.info.apply(console, arguments); };
  var error = function () { console.error.apply(console, arguments); };
  function test(name, timeout, expected, testFn) {
    var res = [], timer;
    function end() {
      if (timer === undefined) return error("test `" + name + "`, `end` called twice");
      timer = clearTimeout(timer);  // timer should be set to undefined
      BigInt.prototype.toJSON = function () { return `BigInt(${this})` };  // XXX GLOBAL MODIFIED
      if (JSON.stringify(res) !== JSON.stringify(expected)) {
        error("test `" + name + "`, result `" + JSON.stringify(res) + "` !== `" + JSON.stringify(expected) + "` expected");
      }
    }
    setTimeout(function () {
      timer = setTimeout(function () {
        try { if (typeof end.onbeforetimeout === "function") end.onbeforetimeout(); }
        catch (e) { error("test: " + name + ", error on before timeout ! `" + e + "`"); }
        if (timer === undefined) return;  // it has ended in before timeout
        error("test `" + name + "`, timeout ! result `" + JSON.stringify(res) + "` ←→ `" + JSON.stringify(expected) + "` expected");
      }, timeout);
      try { testFn(res, end); }
      catch (e) { error("test `" + name + "`, error ! result `" + e + "`"); }
    });
  }

  function testEqual(fn, expected) {
    test(fn, 0, [expected], function (res, end) {
      let v = fn();
      if (v instanceof slice) v = [v.start, v.stop, v.step];
      res.push(v);
      end();
    });
  }
  function testThrow(fn, expected) {
    test(fn, 0, [expected], function (res, end) {
      try {
        let v = fn();
        if (v instanceof slice) v = [v.start, v.stop, v.step];
        res.push(`${expected} expected, but found ->`, v);
      } catch (e) {
        res.push(e.name);
      }
      end();
    });
  }

  testThrow(_=> slice(), "TypeError");  // TypeError: slice expected at least 1 argument, got 0
  testEqual(_=> slice(1), [null, 1, null]);
  testEqual(_=> slice(1, 2), [1, 2, null]);
  testEqual(_=> slice(1, 2, 3), [1, 2, 3]);
  testThrow(_=> slice(1, 2, 3).indices(-4), "TypeError");  // ValueError: length should not be negative

  testEqual(_=> slice(1, 2, 3).indices(4), [1, 2, 3]);
  testEqual(_=> slice(1, 2, 3).getLength(4), 1);

  testEqual(_=> slice(1, -2, 3).indices(0), [0, 0, 3]);
  testEqual(_=> slice(1, -2, 3).indices(10), [1, 8, 3]);
  testEqual(_=> slice(1, -2, 3).getLength(10), 3);

  testEqual(_=> slice(-3, 0, -3).indices(10), [7, 0, -3]);
  testEqual(_=> slice(-3, 0, -3).getLength(10), 3);

  testEqual(_=> slice(1, -2, -3).indices(0), [-1, -1, -3]);
  testEqual(_=> slice(1, -2, -3).indices(10), [1, 8, -3]);
  testEqual(_=> slice(1, -2, -3).getLength(10), 0);

  // type handling

  testEqual(_=> slice(1, 2, 3).indices(undefined), [0, 0, 3]);  // XXX should throw ? undefined is zeroed
  testEqual(_=> slice("1", "2", "3").indices("4"), [1, 2, 3]);

  testEqual(_=> slice(1.1, 2.2, 3.3), [1.1, 2.2, 3.3]);
  testEqual(_=> slice(undefined, "lol", true), [undefined, "lol", true]);

  testEqual(_=> slice(1.1, 2.2, 3.3).indices(4), [1, 2, 3]);
  testEqual(_=> slice(1.1, 2.2, 3.3).indices(4.4), [1, 2, 3]);
  testEqual(_=> slice(1, 2, 3).indices(4n), [1n, 2n, 3n]);

  testEqual(_=> slice(1.1, 2.2, 3.3).getLength(4), 1);
  testEqual(_=> slice(1.1, 2.2, 3.3).getLength(4.4), 1);
  testEqual(_=> slice(1, 2, 3).getLength(4n), 1n);

  //testEqual(_=> slice(1000000000000n, 2000000000000n, 3000000000000n).indices(4), [4n, 4n, 3000000000000n]);
  testThrow(_=> slice(1000000000000n, 2000000000000n, 3000000000000n).indices(4), "TypeError");  // TypeError: can't convert BigInt to number

}());
