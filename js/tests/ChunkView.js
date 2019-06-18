(function script() {
  "use strict";

  /*! ChunkView.js version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading ChunkView.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "ChunkView"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running ChunkView.js tests");

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

  //////////////////////////////////////////////
  // ChunkView tests
  test("new ChunkView([1,2,3]).get & set & getSize", 1000, [4,5,6,4,5,6,null,3], function (res, end) {
    var a = [1,2,3];
    var cv = new ChunkView(a);
    [4,5,6,7].forEach(function (v, i) { cv.set(i, v); });
    res.push.apply(res, a);
    [4,5,6,7].forEach(function (v, i) { res.push(cv.get(i)); });
    res.push(cv.getSize());
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).get & set & getSize", 1000, [1,6,7,8,5,6,7,8,null,3], function (res, end) {
    var a = [1,2,3,4,5];
    var cv = new ChunkView(a, 1, 4);
    [6,7,8,9].forEach(function (v, i) { cv.set(i, v); });
    res.push.apply(res, a);
    [6,7,8,9].forEach(function (v, i) { res.push(cv.get(i)); });
    res.push(cv.getSize());
    end();
  });

  test("new ChunkView([1,2,3]).forEach", 1000, [
    1,0,true,["this"],
    2,1,true,["this"],
    3,2,true,["this"]
  ], function (res, end) {
    var a = [1,2,3], m = ["this"];
    var cv = new ChunkView(a);
    cv.forEach(function (v, i, t) { res.push(v, i, t === cv, this); }, m);
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).forEach", 1000, [
    2,0,true,["this"],
    3,1,true,["this"],
    4,2,true,["this"]
  ], function (res, end) {
    var a = [1,2,3,4,5], m = ["this"];
    var cv = new ChunkView(a, 1, 4);
    cv.forEach(function (v, i, t) { res.push(v, i, t === cv, this); }, m);
    end();
  });

  test("new ChunkView([1,2,3]).slice(1, 2)", 1000, [false,1,2,4], function (res, end) {
    var a = [1,2,3];
    var cv = new ChunkView(a), cvd = cv;
    cv = cv.slice(1, 2);
    res.push(cv === cvd);
    res.push(cv.getSize());
    res.push(cv.get(0));
    cv.set(0,4);
    res.push(a[1]);
    end();
  });
  test("new ChunkView([1,2,3]).slice(1, -1)", 1000, [false,1,2,4], function (res, end) {
    var a = [1,2,3];
    var cv = new ChunkView(a), cvd = cv;
    cv = cv.slice(1, -1);
    res.push(cv === cvd);
    res.push(cv.getSize());
    res.push(cv.get(0));
    cv.set(0,4);
    res.push(a[1]);
    end();
  });
  test("new ChunkView([1,2,3]).slice(-1, 4)", 1000, [false,1,3,4], function (res, end) {
    var a = [1,2,3];
    var cv = new ChunkView(a), cvd = cv;
    cv = cv.slice(-1, 4);
    res.push(cv === cvd);
    res.push(cv.getSize());
    res.push(cv.get(0));
    cv.set(0,4);
    res.push(a[2]);
    end();
  });

  test("new ChunkView([1,2,3,4,5],1,4).slice(1, 2)", 1000, [false,1,3,6], function (res, end) {
    var a = [1,2,3,4,5];
    var cv = new ChunkView(a, 1, 4), cvd = cv;
    cv = cv.slice(1, 2);
    res.push(cv === cvd);
    res.push(cv.getSize());
    res.push(cv.get(0));
    cv.set(0,6);
    res.push(a[2]);
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).slice(1, -1)", 1000, [false,1,3,6], function (res, end) {
    var a = [1,2,3,4,5];
    var cv = new ChunkView(a, 1, 4), cvd = cv;
    cv = cv.slice(1, -1);
    res.push(cv === cvd);
    res.push(cv.getSize());
    res.push(cv.get(0));
    cv.set(0,6);
    res.push(a[2]);
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).slice(-1, 6)", 1000, [false,1,4,6], function (res, end) {
    var a = [1,2,3,4,5];
    var cv = new ChunkView(a, 1, 4), cvd = cv;
    cv = cv.slice(-1, 6);
    res.push(cv === cvd);
    res.push(cv.getSize());
    res.push(cv.get(0));
    cv.set(0,6);
    res.push(a[3]);
    end();
  });

  test("new ChunkView([1,2,3]).readIntoSlice", 1000, [3,3,2,1,0,1,1,1,1], function (res, end) {
    var a = [1,2,3];
    var buffer = new Array(4);
    var cv = new ChunkView(a);
    res.push(cv.readIntoSlice(buffer, 0, 4));
    res.push(cv.readIntoSlice(buffer, 1, 4));
    res.push(cv.readIntoSlice(buffer, 2, 4));
    res.push(cv.readIntoSlice(buffer, 3, 4));
    res.push(cv.readIntoSlice(buffer, 4, 4));
    res.push.apply(res, buffer);
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).readIntoSlice", 1000, [3,3,2,1,0,2,2,2,2], function (res, end) {
    var a = [1,2,3,4,5];
    var buffer = new Array(4);
    var cv = new ChunkView(a, 1, 4);
    res.push(cv.readIntoSlice(buffer, 0, 4));
    res.push(cv.readIntoSlice(buffer, 1, 4));
    res.push(cv.readIntoSlice(buffer, 2, 4));
    res.push(cv.readIntoSlice(buffer, 3, 4));
    res.push(cv.readIntoSlice(buffer, 4, 4));
    res.push.apply(res, buffer);
    end();
  });

  test("new ChunkView([1,2,3]).readAsArray", 1000, [1,2,3,false], function (res, end) {
    var a = [1,2,3];
    var cv = new ChunkView(a);
    var a2 = cv.readAsArray();
    res.push.apply(res, a2);
    res.push(a === a2);
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).readAsArray", 1000, [2,3,4,false], function (res, end) {
    var a = [1,2,3,4,5];
    var cv = new ChunkView(a, 1, 4);
    var a2 = cv.readAsArray();
    res.push.apply(res, a2);
    res.push(a === a2);
    end();
  });

  test("new ChunkView([1,2,3]).pushInto", 1000, [0,1,2,3], function (res, end) {
    var a = [1,2,3], a2 = [0];
    var cv = new ChunkView(a);
    cv.pushInto(a2);
    res.push.apply(res, a2);
    end();
  });
  test("new ChunkView([1,2,3,4,5],1,4).pushInto", 1000, [0,2,3,4], function (res, end) {
    var a = [1,2,3,4,5], a2 = [0];
    var cv = new ChunkView(a, 1, 4);
    cv.pushInto(a2);
    res.push.apply(res, a2);
    end();
  });

}());
