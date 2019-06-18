/*jslint indent: 2 */
(function script() {
  "use strict";

  /*! arrayview.js version 0.2.0

      Copyright (c) 2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading arrayview.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "ArrayView",
      "ArrayViews"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running arrayview.js tests");

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
    setTimeout(function () {
      timer = setTimeout(function () {
        try { if (typeof end.onbeforetimeout === "function") end.onbeforetimeout(); }
        catch (e) { error("test: " + name + ", error on before timeout ! `" + e + "`"); }
        if (timer === undefined) return;  // it has ended in before timeout
        error("test `" + name + "`, timeout ! result `" + JSON.stringify(res) + "` <-> `" + JSON.stringify(expected) + "` expected");
      }, timeout);
      try { testFn(res, end); }
      catch (e) { error("test `" + name + "`, error ! result `" + e + "`"); }
    });
  }

  function mkArray(length, add) { add = add|0; var a = new Array(length); for (var i = 0; i < a.length; i += 1) a[i] = i + add; return a; };
  function randomInt(from, to) { return ((Math.random() * (to - from)) + from)|0; }
  function joinArgs(args, sep) {
    var a = [], i = 0;
    for (; i < args.length; i += 1) {
      if (typeof args[i] === "function") a.push("<func>");
      else a.push(""+args[i]);
    }
    return a.join(sep);
  }
  function mkRandomArrayViews() {
    var views = new Array(randomInt(0, 4)), addition = 10;
    views.fill(null);
    views.forEach(function (_, vi, views) {
      var array = mkArray(randomInt(5, 11), addition),
          offset = randomInt(0, array.length),
          length = randomInt(0, array.length - offset);
      views[vi] = {array: array, viewOffset: offset, viewLength: length};
      addition += 10
    });
    return views;
  }

  function testArrayViewReadAsArray(array, offset, length, result) {
    test("new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").readAsArray();", 300, result, function (res, end) {
      var av = new ArrayView(array, offset, length);
      res.push.apply(res, av.readAsArray());
      end();
    });
  }

  function testArrayView_callback1(methodName, stopatfunc) { return function () {
    var array = arguments[0] || mkArray(randomInt(5, 11), 10),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, offset, length),
        slice = av.readAsArray(),
        stopat = randomInt(0, array.length - offset),
        expected = [],
        thisArg = 0,
        args = [function (v, i, a) {
          expected.push([v, i, a === slice, this === thisArg]);
          if (stopatfunc) return stopatfunc(stopat, i);
        }],
        msg = "";
    if (arguments.length > 3) args.push(thisArg = arguments[3]);
    else if (randomInt(0, 2)) args.push(thisArg = [undefined, null, {1:2}][randomInt(0, 3)]);
    //if (args[1] === undefined) thisArg === window;
    expected.push(slice[methodName].apply(slice, args));
    msg = "new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ")." + methodName + "(" + joinArgs(args, ", ") + ");"
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      args[0] = function (v, i, a) {
        res.push([v, i, a === av, this === thisArg]);
        if (stopatfunc) return stopatfunc(stopat, i);
      };
      res.push(av[methodName].apply(av, args));
      //console.log(JSON.stringify(res));
      end();
    });
  }; }


  function testArrayViewCopyWithin() {
    var array = arguments[0] || mkArray(randomInt(5, 11)),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, offset, length),
        slice = av.readAsArray(),
        args = arguments[3] || new Array(randomInt(0, 4)),
        splicedarray = array.slice(),
        i = 0;
    splicedarray.splice(offset, length);
    if (!arguments[3]) for (; i < args.length; i += 1) args[i] = randomInt(-12, 13);
    test("new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").copyWithin(" + args.join(", ") + ");", 300, [slice.copyWithin.apply(slice, args), splicedarray], function (res, end) {
      av.copyWithin.apply(av, args);
      res.push(av.readAsArray());
      array.splice(offset, length);
      res.push(array);
      end();
    });
  }

  function testArrayViewEvery() {
    return testArrayView_callback1("every", function (stopat, i) { return i < stopat; })();
  }

  function testArrayViewFill() {
    var array = arguments[0] || mkArray(randomInt(5, 11)),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, offset, length),
        slice = av.readAsArray(),
        args = arguments[3] || new Array(randomInt(0, 4)),
        splicedarray = array.slice(),
        expected = null,
        i = 0;
    splicedarray.splice(offset, length);
    if (!arguments[3]) for (; i < args.length; i += 1) args[i] = randomInt(-12, 13);
    expected = [slice.fill.apply(slice, args), splicedarray];
    //console.log(JSON.stringify(expected));
    test("new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").fill(" + args.join(", ") + ");", 300, expected, function (res, end) {
      av.fill.apply(av, args);
      res.push(av.readAsArray());
      array.splice(offset, length);
      res.push(array);
      //console.log(JSON.stringify(res));
      end();
    });
  }

  function testArrayViewFilter() {
    var array = arguments[0] || mkArray(randomInt(5, 11)),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, offset, length),
        slice = av.readAsArray(),
        filter = [],
        expected = [],
        thisArg = null,
        args = [function (v, i, a) {
          expected.push([v, i, a === slice, this === thisArg]);
          return filter[i];
        }],
        i = 0;
    if (arguments.length > 3) args.push(arguments[3]);
    else if (randomInt(0, 2)) args.push([undefined, null, {1:2}][randomInt(0, 3)]);
    if (args[1] === undefined) thisArg === window;
    for (; i < slice.length; i += 1) filter.push(randomInt(0, 2));
    expected.push(slice.filter.apply(slice, args));
    //console.log(JSON.stringify(filter));
    //console.log(JSON.stringify(expected));
    test("new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").filter(" + joinArgs(args, ", ") + ");", 300, expected, function (res, end) {
      args[0] = function (v, i, a) {
        res.push([v, i, a === av, this === thisArg]);
        return filter[i];
      };
      res.push(av.filter.apply(av, args).readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }

  function testArrayViewFind() {
    return testArrayView_callback1("find", function (stopat, i) { return stopat > i; })();
  }
  function testArrayViewFindIndex() {
    return testArrayView_callback1("findIndex", function (stopat, i) { return stopat > i; })();
  }
  function testArrayViewForEach() {
    return testArrayView_callback1("forEach")();
  }

  function testArrayViewIncludes() {
    var array = arguments[0] || mkArray(randomInt(5, 11), 10),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, offset, length),
        slice = av.readAsArray(),
        args = [],
        expected = [],
        msg = "";
    if (arguments[3]) args = arguments[3];
    else { if (randomInt(0, 4)) { args.push(randomInt(10, 20)); if (randomInt(0, 2)) { args.push(randomInt(-12, 13)); }}}
    expected = [slice.includes.apply(slice, args)];
    msg = "new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").includes(" + args.join(", ") + ");"
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      res.push(av.includes.apply(av, args));
      end();
    });
  }

  function testArrayViewJoin() {
    var array = arguments[0] || mkArray(randomInt(5, 11), 10),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, offset, length),
        slice = av.readAsArray(),
        args = [],
        expected = [],
        msg = "";
    if (arguments[3]) args = arguments[3];
    else if (randomInt(0, 2)) args.push(", ");
    expected = [slice.join.apply(slice, args)];
    msg = "new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").join(" + args.join(", ") + ");"
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      res.push(av.join.apply(av, args));
      end();
    });
  }

  function testArrayViewSlice() {
    var array = arguments[0] || mkArray(randomInt(5, 11), 10),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, 0, array.length),
        args = arguments[3] || new Array(randomInt(0, 3)),
        expected = [false, false, null],
        msg = "", i = 0;
    if (!arguments[3]) for (; i < args.length; i += 1) args[i] = randomInt(-12, 13);
    expected[2] = array.slice.apply(array, args);
    msg = "new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").slice(" + args.join(", ") + ");";
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      var av2 = av.slice.apply(av, args);
      res.push(av === av2, av.array === av2.array, av2.readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }
  function testArrayViewSubarray() {
    var array = arguments[0] || mkArray(randomInt(5, 11), 10),
        offset = arguments[1] || randomInt(0, array.length),
        length = arguments[2] || randomInt(0, array.length - offset),
        av = new ArrayView(array, 0, array.length),
        args = arguments[3] || new Array(randomInt(0, 3)),
        expected = [false, true, null],
        msg = "", u = null, i = 0;
    if (!arguments[3]) for (; i < args.length; i += 1) args[i] = randomInt(-12, 13);
    u = new Uint8Array(array);
    expected[2] = Array.from(u.subarray.apply(u, args));
    msg = "new ArrayView(" + JSON.stringify(array) + ", " + offset + ", " + length + ").subarray(" + args.join(", ") + ");";
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      var av2 = av.subarray.apply(av, args);
      res.push(av === av2, av.array === av2.array, av2.readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }

  function testArrayViewsReadAsArray(views, result) {
    var msg = "new ArrayViews(" + JSON.stringify(views) + ").readAsArray();";
    //console.log(msg + " " + JSON.stringify(result));
    test(msg, 300, result, function (res, end) {
      var avv = new ArrayViews(views);
      res.push.apply(res, avv.readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }

  function testArrayViewsCopyWithin() {
    var avv = new ArrayViews(arguments[0] || mkRandomArrayViews()),
        args = arguments[1] || new Array(randomInt(0, 4)),
        array = avv.readAsArray(),
        expected = [null],
        msg = "", i = 0;
    if (!arguments[1]) for (; i < args.length; i += 1) args[i] = randomInt(-array.length-1, array.length+2);
    expected[0] = array.copyWithin.apply(array, args);
    msg = "new ArrayViews(" + JSON.stringify(avv.views) + ").copyWithin(" + args.join(", ") + ");";
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      avv.copyWithin.apply(avv, args);
      res.push(avv.readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }

  function testArrayViewsSubarray() {
    var avv = new ArrayViews(arguments[0] || mkRandomArrayViews()),
        args = arguments[1] || new Array(randomInt(0, 3)),
        expected = [false, null],
        msg = "", u = null, i = 0;
    u = new Uint8Array(avv.readAsArray());
    if (!arguments[1]) for (; i < args.length; i += 1) args[i] = randomInt(-u.length-1, u.length+2);
    expected[1] = Array.from(u.subarray.apply(u, args));
    msg = "new ArrayViews(" + JSON.stringify(avv.views) + ").subarray(" + args.join(", ") + ");";
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      var avv2 = avv.subarray.apply(avv, args);
      res.push(avv === avv2, avv2.readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }

  function testArrayViewsFill() {
    var avv = new ArrayViews(arguments[0] || mkRandomArrayViews()),
        args = arguments[1] || new Array(randomInt(0, 4)),
        expected = [true, null],
        msg = "", u = null, i = 0;
    u = avv.readAsArray();
    if (!arguments[1]) for (; i < args.length; i += 1) args[i] = randomInt(-u.length-1, u.length+2);
    expected[1] = u.fill.apply(u, args);
    msg = "new ArrayViews(" + JSON.stringify(avv.views) + ").fill(" + args.join(", ") + ");";
    //console.log(msg + " " + JSON.stringify(expected));
    test(msg, 300, expected, function (res, end) {
      var avv2 = avv.fill.apply(avv, args);
      res.push(avv === avv2, avv2.readAsArray());
      //console.log(JSON.stringify(res));
      end();
    });
  }

  //////////////////////////////////////////////
  // ArrayView
  testArrayViewReadAsArray([0,1,2,3,4,5,6,7,8,9], 0, 10, [0,1,2,3,4,5,6,7,8,9]);
  testArrayViewReadAsArray([0,1,2,3,4,5,6,7,8,9], 1, 8, [1,2,3,4,5,6,7,8]);
  testArrayViewReadAsArray([0,1,2,3,4,5,6,7,8,9], 1, 0, []);
  //testArrayViewReadAsArray([0,1,2,3,4,5,6,7,8,9], 1, -1, []);

  testArrayViewCopyWithin();
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, []);
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, [1]);
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, [1, 3]);
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, [1, 3, 5]);
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, [-5, -3, -1]);
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, [-16, -16, -16]);
  testArrayViewCopyWithin([0,1,2,3,4,5], 1, 2, []);
  testArrayViewCopyWithin([0,1,2,3,4,5,6,7,8,9], 1, 8, [7, -9, 3]);
  testArrayViewCopyWithin([0,1,2,3,4,5], 1, 4, [-5, -2]);
  testArrayViewEvery();
  testArrayViewFill();
  testArrayViewFill([0,1,2,3,4,5,6,7,8], 8, 0, [-6, 2, 6]);
  testArrayViewFilter();
  testArrayViewFind();
  testArrayViewFindIndex();
  testArrayViewForEach();
  testArrayViewIncludes();
  //testArrayViewIndexOf();
  testArrayViewJoin();
  testArrayViewJoin([undefined, NaN, null, 1, 1.1, "str", function () {}, {1:2}, ["lol"]]);
  //testArrayViewLastIndexOf();
  //testArrayViewReverse();
  testArrayViewSlice();
  testArrayViewSlice([10,11,12,13,14,15,16], 5, 1, [-1, 0]);
  testArrayViewSubarray();
  testArrayViewSubarray([10,11,12,13,14,15,16], 5, 1, [-1, 0]);

  // XXX test other methods !!!!!!!!!

  //////////////////////////////////////////////
  // ArrayViews
  testArrayViewsReadAsArray([
    {array: [10,11,12,13,14,15,16,17,18,19], viewOffset: 0, viewLength: 10},
    {array: [20,21,22,23,24,25,26,27,28,29], viewOffset: 1, viewLength: 8},
    {array: [30,31,32,33,34,35,36,37,38,39], viewOffset: 3, viewLength: 0},
    {array: [40,41,42,43,44,45,46,47,48,49], viewOffset: 9, viewLength: 1},
  ], [10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,49]);

  testArrayViewsCopyWithin();
  testArrayViewsCopyWithin([{"array":[10,11,12,13,14,15,16,17],"viewOffset":0,"viewLength":7},{"array":[20,21,22,23,24,25,26,27,28],"viewOffset":1,"viewLength":3},{"array":[30,31,32,33,34,35,36],"viewOffset":3,"viewLength":3}], [-4, -5]);
  testArrayViewsCopyWithin([{"array":[10,11,12,13,14,15,16,17,18,19],"viewOffset":6,"viewLength":3}], [0, 2, 0]);
  testArrayViewsCopyWithin([{"array":[10,11,12,13,14,15,16,17],"viewOffset":2,"viewLength":0},{"array":[20,21,22,23,24,25,26,27],"viewOffset":2,"viewLength":3},{"array":[30,31,32,33,34],"viewOffset":3,"viewLength":1}], [2, -3, -1]);
  testArrayViewsCopyWithin([{"array":[10,11,12,13,14,15,16,17],"viewOffset":2,"viewLength":3},{"array":[20,21,22,23,24,25,26,27,28,29],"viewOffset":0,"viewLength":3},{"array":[30,31,32,33,34,35],"viewOffset":5,"viewLength":0}], [0, -4, 0]);
  testArrayViewsCopyWithin([{"array":[10,11,12,13,14],"viewOffset":2,"viewLength":2},{"array":[20,21,22,23,24,25,26,27,28],"viewOffset":0,"viewLength":2}], [-1]);
  testArrayViewsFill();
  testArrayViewsFill([{"array":[10,11,12,13,14],"viewOffset":2,"viewLength":2}], []);
  testArrayViewsFill([{"array":[10,11,12,13,14,15,16,17,18,19],"viewOffset":2,"viewLength":2},{"array":[20,21,22,23,24,25,26,27,28],"viewOffset":7,"viewLength":0},{"array":[30,31,32,33,34,35,36],"viewOffset":1,"viewLength":2}], [5, -4, 3]);
  //testArrayViewsReverse();
  testArrayViewsSubarray();
  testArrayViewsSubarray([{"array":[10,11,12,13,14,15,16,17],"viewOffset":0,"viewLength":7},{"array":[20,21,22,23,24,25,26,27,28],"viewOffset":1,"viewLength":3},{"array":[30,31,32,33,34,35,36],"viewOffset":6,"viewLength":0}], [9]);
  testArrayViewsSubarray([{"array":[10,11,12,13,14,15],"viewOffset":4,"viewLength":1},{"array":[20,21,22,23,24,25,26,27,28],"viewOffset":6,"viewLength":1},{"array":[30,31,32,33,34,35,36],"viewOffset":4,"viewLength":2}], [0, 4]);
  testArrayViewsSubarray([{"array":[10,11,12,13],"viewOffset":1,"viewLength":2},{"array":[20,21,22,23],"viewOffset":1,"viewLength":2},{"array":[30,31,32,33],"viewOffset":1,"viewLength":2},{"array":[40,41,42,43],"viewOffset":1,"viewLength":2}], [0, 6]);

  // XXX test other methods !!!!!!!!!

}());
