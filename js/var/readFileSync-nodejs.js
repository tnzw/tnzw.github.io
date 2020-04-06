this.readFileSync = (function script() {
  "use strict";

  /*! readFileSync-nodejs.js Version 1.0.0

      Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  var fs, _readFileSync = function (path, options) {
    fs = require("fs");
    _readFileSync = function (path, options) {
      // It's the same function as fs.readFileSync with extension to allow `options.start` and `options.end`.
      var length = 0, position = 0, start, end, fd, buffer, bytesRead;
      if (typeof options === "object" && (options.start !== undefined || options.end !== undefined)) {
        if (options.encoding !== undefined && options.encoding !== "buffer") throw new Error("cannot seek with encoding : " + options.encoding);
        if (options.end === undefined) end = fs.statSync(path).size|0;
        else end = options.end|0;
        if (options.start === undefined) start = 0;
        else start = options.start;
        length = end - start;
        position = start;
        if (typeof path === "number") fd = path;
        else fd = fs.openSync(path, "r");
        try {
          bytesRead = fs.readSync(fd, buffer = Buffer.alloc(length), 0, length, position);
        } finally {
          if (typeof path !== "number") fs.closeSync(fd);
        }
        return buffer.slice(0, bytesRead);
      }
      return fs.readFileSync(path, options);
    };
    return _readFileSync(path, options);
  };
  function readFileSync(path, options) { return _readFileSync(path, options); }
  readFileSync.toScript = function () { return "(" + script.toString() + "())"; };
  return readFileSync;

}());
