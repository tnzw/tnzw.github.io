(function (global) {
  "use strict";
  if (typeof global.Blob === "undefined")

global.Blob = (function () { try { return require("buffer").Blob } catch (_) {} })() || (function script() {
  "use strict";

  /*! Blob-nodejs.js Version 1.1.0

      Copyright (c) 2019, 2022 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function Blob(chunks, options) {
    this._data = null;
    this.type = "";
    this.size = 0;
    if (options) {
      if (options.type !== undefined) this.type = "" + options.type;
    }

    function max(a, b) { return a > b ? a : b; }
    function cpy(s, d, di) { for (var si = 0; si < s.length; si = ((si + 1)|0), di = (di + 1)|0) d[di] = s[si]; return di; }
    var strings = [], i = 0, j = 0, c = null;

    // get size

    for (; i < chunks.length; i = (i + 1)|0) {
      if (typeof chunks[i] === "string") {
        strings.push(c = Buffer.from(chunks[i], "UTF-8"));
        this.size += c.length;
      } else if ((chunks[i] instanceof Blob)) {
        this.size += chunks[i].size;
      } else if ((chunks[i] instanceof Buffer) ||
                 (chunks[i] instanceof ArrayBuffer)) {
        this.size += chunks[i].length;
      } else if ((chunks[i] instanceof Int8Array) ||
                 (chunks[i] instanceof Uint8Array) ||
                 (chunks[i] instanceof Uint8ClampedArray) ||
                 (chunks[i] instanceof Int16Array) ||
                 (chunks[i] instanceof Uint16Array) ||
                 (chunks[i] instanceof Int32Array) ||
                 (chunks[i] instanceof Uint32Array) ||
                 (chunks[i] instanceof Float32Array) ||
                 (chunks[i] instanceof Float64Array)) {
        this.size += chunks[i].byteLength;
      } else {
        strings.push(c = Buffer.from(""+chunks[i], "UTF-8"));
        this.size += c.length;
      }
    }

    // copy data

    //this._data = new Uint8Array(this.size);
    this._data = Buffer.alloc(this.size);

    for (i = 0; i < chunks.length; i = (i + 1)|0) {
      if (typeof chunks[i] === "string") {
        j = cpy(strings.unshift(), this._data, j);
      } else if ((chunks[i] instanceof Blob)) {
        j = cpy(chunks[i]._data, this._data, j);
      } else if ((chunks[i] instanceof Buffer) ||
                 (chunks[i] instanceof Uint8Array) ||
                 (chunks[i] instanceof Uint8ClampedArray)) {
        j = cpy(chunks[i], this._data, j);
      } else if ((chunks[i] instanceof ArrayBuffer) ||
                 (chunks[i] instanceof Int8Array) ||
                 (chunks[i] instanceof Int16Array) ||
                 (chunks[i] instanceof Uint16Array) ||
                 (chunks[i] instanceof Int32Array) ||
                 (chunks[i] instanceof Uint32Array) ||
                 (chunks[i] instanceof Float32Array) ||
                 (chunks[i] instanceof Float64Array)) {
        j = cpy(new Uint8Array(chunks[i]), this._data, j);
      } else {
        j = cpy(strings.unshift(), this._data, j);
      }
    }
  }
  Blob.prototype.type = "";
  Blob.prototype.size = 0;
  Blob.prototype.slice = function (start, end, contentType) {
    var n = new Blob([], {type: contentType});
    n._data = this._data.slice(start, end);
    n.size = n._data.length;
    return n;
  };

  Blob.prototype.arrayBuffer = async function () {
    return this._readAsArrayBuffer();
  };
  Blob.prototype.text = async function () {
    return this._readAsText();
  };

  Blob.prototype._readAsBuffer = function () {
    return Buffer.from(this._data);
  };
  Blob.prototype._readAsArrayBuffer = function () {
    var data = new Uint8Array(this._data.length), i = 0;
    for (; i < data.length; i = (i + 1)|0) data[i] = this._data[i];
    return data.buffer;
  };
  Blob.prototype._readAsText = function () {
    return this._data.toString("UTF-8");
  };
  Blob.prototype._readAsDataURL = function () {
    if (this.type.indexOf(",") !== -1) throw new Error("not implemented");
    return "data:" + this.type + ";base64," + this._data.toString("base64");
  };
  Blob.prototype._readAsBinaryString = function () {
    var bs = "", i = 0;
    for (; i < this._data.length; i = (i + 1)|0) bs += String.fromCharCode(this._data[i]);
    return bs;
  };

  return Blob;

}());

}(this));
