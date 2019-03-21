(function (global) {
  "use strict";
  if (typeof global.File === "undefined")

global.File = (function script() {
  "use strict";

  /*! File-nodejs.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function File(chunks, fileName, options) {
    this.filename = ""+fileName;
    this.lastModifiedDate = new Date();
    this.lastModified = this.lastModifiedDate.getTime();
    if (options) {
      if (options.lastModified) {
        this.lastModifiedDate = new Date(options.lastModified);
        this.lastModified = this.lastModifiedDate.getTime() || 0;
        this.lastModifiedDate = new Date(this.lastModified);
      }
    }
    Blob.call(this, chunks, options);
  }
  File.prototype = Object.create(Blob.prototype);
  Object.defineProperty(File.prototype, "constructor", {
    value: File,
    enumerable: false,
    writable: true,
    configurable: true,
  });
  File.prototype.filename = 0;
  File.prototype.lastModified = 0;
  File.prototype.lastModifiedDate = null;

  File._fromPath = function (path, options) {
    var fs = require("fs"), p = require("path"),
        file = new File([], p.basename(path), options),
        stats = null;
    function statSync(path) {
      if (stats) return stats;
      stats = fs.statSync(path);
      Promise.resolve().then(function () { stats = null; });
    }
    Object.defineProperty(file, "size", {
      configurable: true,
      enumerable: true,
      get: function () {
        try {
          statSync(path);
          return stats.size;
        } catch (e) {
          return 0;
        }
      }
    });
    Object.defineProperty(file, "lastModified", {
      configurable: true,
      enumerable: true,
      get: function () {
        try {
          statSync(path);
          return stats.mtime.getTime();
        } catch (e) {
          return new Date().getTime();
        }
      }
    });
    Object.defineProperty(file, "lastModifiedDate", {
      configurable: true,
      enumerable: true,
      get: function () {
        try {
          statSync(path);
          return stats.mtime;
        } catch (e) {
          return new Date();
        }
      }
    });
    Object.defineProperty(file, "_data", {
      configurable: true,
      enumerable: true,
      get: function () {
        try {
          // not concurrent safe,
          // if this.size shows 3, then another process deletes file, this._data returns empty Buffer.
          return fs.readFileSync(path);
        } catch (e) {
          return Buffer.alloc(0);
        }
      }
    });
    return file;
  };

  return File;

}());

}(this));
