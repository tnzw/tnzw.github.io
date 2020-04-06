this.readFile = (function script() {
  "use strict";

  /*! readFile-nodejs.js Version 1.0.0

      Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  var fs, _readFile = function (path, options, callback) {
    fs = require("fs");
    _readFile = function (path, options, callback) {
      // It's the same function as fs.readFile with extension to allow `options.start` and `options.end`.
      var length = 0, position = 0, fi = 0, ff, start, end, fd, buffer, bytesRead;
      if (typeof options === "object" && (options.start !== undefined || options.end !== undefined)) {
        if (options.encoding !== undefined && options.encoding !== "buffer") return callback(new Error("cannot seek with encoding : " + options.encoding));
        ff = [function () {
          if (options.end === undefined) return fs.stat(path, ff[fi++]);
          else end = options.end|0;
          ff[fi++]();
        }, function (err, stat) {
          if (err) return callback(err);
          if (stat) end = stat.size|0;
          if (options.start === undefined) start = 0;
          else start = options.start;
          length = end - start;
          position = start;
          if (typeof path === "number") ff[fi++](undefined, path);
          else fs.open(path, "r", ff[fi++]);
        }, function (err, _fd) {
          if (err) return callback(err);
          fd = _fd;
          fs.read(fd, Buffer.alloc(length), 0, length, position, ff[fi++]);
        }, function (err, _bytesRead, _buffer) {
          if (err) {
            if (typeof path === "number") return callback(err);
            return fs.close(fd, function (err2) { if (err2) console.error(err2); return callback(err); });
          }
          bytesRead = _bytesRead; buffer = _buffer;
          if (typeof path !== "number") fs.close(fd, ff[fi++]);
          else ff[fi++]();
        }, function (err) {
          if (err) return callback(err);
          return callback(undefined, buffer.slice(0, bytesRead));
        }]; return ff[fi++]();
      }
      return fs.readFile(path, options, callback);
    };
    return _readFile(path, options, callback);
  };
  function readFile(path, options, callback) { return _readFile(path, options, callback); }
  readFile.toScript = function () { return "(" + script.toString() + "())"; };
  return readFile;

}());
