(function script() {
  "use strict";

  /*! ChunkViews.js version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading ChunkViews.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "ChunkView",
      "ChunkViews"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running ChunkViews.js tests");

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
  // ChunkViews tests
  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).get & set & getSize", 1000, [9,10,11,4,12,13,14,8,9,10,11,12,13,14,null,6], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]);
    [9,10,11,12,13,14,15].forEach(function (v, i) { cvv.set(i, v); });
    res.push.apply(res, a);
    res.push.apply(res, b);
    [9,10,11,12,13,14,15].forEach(function (v, i) { res.push(cvv.get(i)); });
    res.push(cvv.getSize());
    end();
  });

  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).append", 1000, [
    true, false,
    7, 11
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8], c = [9,10,11,12,13];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]);
    var cvv2 = cvv.append(new ChunkView(c, 2, 3));
    res.push(!!cvv2);
    res.push(cvv2 === cvv);
    res.push(cvv2.getSize());
    res.push(cvv2.get(6));
    end();
  });

  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).forEach", 1000, [
    1,0,true,["this"],
    2,1,true,["this"],
    3,2,true,["this"],
    5,3,true,["this"],
    6,4,true,["this"],
    7,5,true,["this"]
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8], m = ["this"];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]);
    cvv.forEach(function (v, i, t) { res.push(v, i, t === cvv, this); }, m);
    end();
  });

  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).slice(1, 2)", 1000, [
    false, 1, 2, 9
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]), cvvd = cvv;
    cvv = cvv.slice(1, 2);
    res.push(cvv === cvvd);
    res.push(cvv.getSize());
    res.push(cvv.get(0));
    cvv.set(0, 9);
    res.push(a[1]);
    end();
  });
  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).slice(4, 5)", 1000, [
    false, 1, 6, 9
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]), cvvd = cvv;
    cvv = cvv.slice(4, 5);
    res.push(cvv === cvvd);
    res.push(cvv.getSize());
    res.push(cvv.get(0));
    cvv.set(0, 9);
    res.push(b[2]);
    end();
  });
  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).slice(1, -1)", 1000, [
    false, 4,
    2, 5,
    9
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]), cvvd = cvv;
    cvv = cvv.slice(1, -1);
    res.push(cvv === cvvd);
    res.push(cvv.getSize());
    res.push(cvv.get(0));
    res.push(cvv.get(2));
    cvv.set(0, 9);
    res.push(a[1]);
    end();
  });
  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).slice(-1, 7)", 1000, [
    false, 1, 7, 9
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]), cvvd = cvv;
    cvv = cvv.slice(-1, 7);
    res.push(cvv === cvvd);
    res.push(cvv.getSize());
    res.push(cvv.get(0));
    cvv.set(0, 9);
    res.push(b[3]);
    end();
  });

  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).readIntoSlice", 1000, [
    6,6,5,4,3,2,1,0,
    1,1,1,1,1,1,1
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var buffer = new Array(7);
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]);
    res.push(cvv.readIntoSlice(buffer, 0, 7));
    res.push(cvv.readIntoSlice(buffer, 1, 7));
    res.push(cvv.readIntoSlice(buffer, 2, 7));
    res.push(cvv.readIntoSlice(buffer, 3, 7));
    res.push(cvv.readIntoSlice(buffer, 4, 7));
    res.push(cvv.readIntoSlice(buffer, 5, 7));
    res.push(cvv.readIntoSlice(buffer, 6, 7));
    res.push(cvv.readIntoSlice(buffer, 7, 7));
    res.push.apply(res, buffer);
    end();
  });

  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).readAsArray", 1000, [
    1,2,3,5,6,7,
    false
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]);
    var a2 = cvv.readAsArray();
    res.push.apply(res, a2);
    res.push(a === a2);
    end();
  });

  test("new ChunkViews([new ChunkView([1,2,3]), new ChunkView([4,5,6,7,8],1,4)]).pushInto", 1000, [
    0,1,2,3,5,6,7
  ], function (res, end) {
    var a = [1,2,3], b = [4,5,6,7,8],
        a2 = [0];
    var cvv = new ChunkViews([new ChunkView(a), new ChunkView(b, 1, 4)]);
    cvv.pushInto(a2);
    res.push.apply(res, a2);
    end();
  });

}());
