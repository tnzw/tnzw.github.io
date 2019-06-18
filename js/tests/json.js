(function script() {
  "use strict";

  /*! json.js version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading json.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "jsonStringify"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running json.js tests");

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

  function testStringify(value, replacer, space, expected) {
    if (arguments.length < 4) expected = JSON.stringify(value, replacer, space);
    test("jsonStringify", 1000, [expected], function (res, end) {
      try {
        res.push(jsonStringify(value, replacer, space));
      } catch (e) {
        res.push(e);
      }
      end();
    });
  }

  //////////////////////////////////////////////
  // jsonStringify tests
  testStringify({});
  testStringify(true);
  testStringify('foo');
  testStringify([1, 'false', false]);
  testStringify({x: 5});

  testStringify(new Date(2006, 0, 2, 15, 4, 5));

  testStringify({x: 5, y: 6});

  testStringify([new Number(3), new String('false'), new Boolean(false)]);
  function Foo() {}
  Foo.prototype = new Number(3);
  testStringify([new Foo(4)]);

  testStringify({x: [10, undefined, function () {}, Symbol('')]}); 
 
  testStringify({ x: undefined, y: Object, z: Symbol('') }); // '{}'
  testStringify({ [Symbol('foo')]: 'foo' }); // '{}'
  testStringify({ [Symbol.for('foo')]: 'foo' }, [Symbol.for('foo')]); // '{}'
  testStringify({ [Symbol.for('foo')]: 'foo' }, function(k, v) { if (typeof k === 'symbol') { return 'a symbol'; }}); // '{}'

  testStringify(Object.create(null, { x: { value: 'x', enumerable: false }, y: { value: 'y', enumerable: true } })); // '{"y":"y"}'

  testStringify({foundation: 'Mozilla', model: 'box', week: 45, transport: 'car', month: 7}, function (key, value) { if (typeof value === "string") return undefined; return value; });  // '{"week":45,"month":7}'

  testStringify({foundation: 'Mozilla', model: 'box', week: 46, transport: 'car', month: 8}, ['week', 'month']);  // '{"week":46,"month":8}', only keep "week" and "month" properties

  testStringify({a: 2}, null, ' ');

  testStringify({ uno: 1, dos: 2 }, null, '\t');

  testStringify({ uno: 1, dos: 2 }, null, 1);

  testStringify({ uno: 1, dos: 2 }, null, undefined);
  testStringify({ uno: 1, dos: 2 }, null, NaN);
  testStringify({ uno: 1, dos: 2 }, null, 1.1);
  testStringify({ uno: 1, dos: 2 }, null, null);
  testStringify({ uno: 1, dos: 2 }, null, true);
  testStringify({ uno: 1, dos: 2 }, null, Object);

/*
const bonnie = {
  name: 'Bonnie Washington',
  age: 17,
  class: 'Year 5 Wisdom',
  isMonitor: false,
  toJSON: function(key) {
    // Clone object to prevent accidentally performing modification on the original object
    const cloneObj = { ...this };

    delete cloneObj.age;
    delete cloneObj.isMonitor;
    cloneObj.year = 5;
    cloneObj.class = 'Wisdom';

    if (key) {
      cloneObj.code = key;
    }

    return cloneObj;
  }
}

JSON.stringify(bonnie);
// Returns '{"name":"Bonnie Washington","class":"Wisdom","year":5}'

const students = {bonnie};
JSON.stringify(students);
// Returns '{"bonnie":{"name":"Bonnie Washington","class":"Wisdom","year":5,"code":"bonnie"}}'

const monitorCandidate = [bonnie];
JSON.stringify(monitorCandidate)
// Returns '[{"name":"Bonnie Washington","class":"Wisdom","year":5,"code":"0"}]'
*/

}());
