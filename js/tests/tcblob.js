/*jslint indent: 2 */
(function script() {
  "use strict";

  /*! tcblob.js version 0.2.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading tcblob.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "readBlob",  // for convenience
      "TcBlob",
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running tcblob.js tests");

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

  function testSlice(chunks, options, args) {
    var blob = new Blob(chunks, options).slice(args[0], args[1], args[2]);
    var result = {size: blob.size, type: blob.type};
    readBlob(blob, "text").then(function (text) {
      result.text = text;
      return readBlob(blob, "arraybuffer");
    }).then(function (ab) {
      result.arraybuffer = Array.from(new Uint8Array(ab));

    test("new TcBlob(" + chunks + ", " + JSON.stringify(options) + ").slice(" + args + ");", 300, [result], function (res, end) {
      res.push({}); res = res[0];
      var tcblob = new TcBlob(chunks, options).slice(args[0], args[1], args[2]);
      res.size = tcblob.size;
      res.type = tcblob.type;
      res.text = tcblob.readAsText();
      res.arraybuffer = Array.from(new Uint8Array(tcblob.readAsArrayBuffer()));
      
      end();
    });

    });
  }

  testSlice(["coucou"], {}, [1, 2]);
  testSlice(["coucou"], {}, [2, 4]);
  testSlice(["cou", "cou"], {}, [1, 4, "hello"]);
  testSlice(["cou", "cou", "cou"], {}, [1, 8, "hello"]);
  testSlice([String.fromCharCode(0xD83C, 0xDFAE)], {}, []);  // video game controller char
  testSlice([String.fromCharCode(0xD83C), String.fromCharCode(0xDFAE)], {}, []);

}());
