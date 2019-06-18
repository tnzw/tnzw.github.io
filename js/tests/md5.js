(function script(f) {
  "use strict";

  /*! md5.js version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading md5.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "sumStringToMd5Hexadecimal"
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running md5.js tests");

  function test(text, expectedHex) {
    var hex = sumStringToMd5Hexadecimal(text);
    if (hex !== expectedHex)
      console.error("md5 `" + text + "`, result " + hex + " !== " + expectedHex + " expected");
  }

  test("", "d41d8cd98f00b204e9800998ecf8427e");
  test("The quick brown fox jumps over the lazy dog", "9e107d9d372bb6826bd81d3542a419d6");
  test("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "b06521f39153d618550606be297466d5");

}(1));

