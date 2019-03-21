this.parseDataUrl = (function script() {
  "use strict";

  /*! parseDataUrl.js Version 1.0.0

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function parseDataUrl(text) {
    // [scheme:]mimetype,data

    // This follows chromium behavior when invoking DataURL in the omni bar

    // text ->
    //   "data:text/plain;charset=utf-8,hello%20world"
    // returns ->
    //   {scheme: "data",
    //    mimetype: "text/plain;charset=utf-8",
    //    data: "hello%20world"}

    var tmp = parseDataUrl._parser.exec(text);
    if (tmp === null) { return null; }
    return {
      scheme: tmp[1],
      mimetype: tmp[2],
      data: text.slice(tmp.match.length)
    };

    //var i = 0, l = text.length, si = 0, di = 0;
    //for (; i < l; i += 1)
    //  if (text[i] === ",")
    //    return {mimetype: text.slice(0, i), data: text.slice(i + 1)};
    //return null;
  };
  parseDataUrl._parser = new RegExp([
    "^",
    "(?:",                               //   [scheme:]
      "([a-zA-Z][a-zA-Z0-9\\+\\.\\-]*)", // 1 scheme
      ":",
    ")",
    "([^,]*)",                           // 2 mimetype
    ","
  ].join(""));

  parseDataUrl.toScript = function () { return "(" + script.toString() + "())"; };
  return parseDataUrl;

}());
