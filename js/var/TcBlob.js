this.TcBlob = (function script() {
  "use strict";

  /*! TcBlob.js Version 1.2.0

      Copyright (c) 2019, 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function TcBlob(chunks, options) {
    this.chunks = [];
    this.type = "";
    this.size = 0;
    if (options) {
      if (options.type !== undefined) this.type = "" + options.type;
    }
    if (chunks === undefined) chunks = [];
    var i = 0, c = null;
    for (; i < chunks.length; i += 1) {
      if (typeof chunks[i] === "string") {
        c = new Uint8Array(new TextEncoder("utf-8").encode(chunks[i]));  // copying data
        if (c.length) { this.chunks.push(c); this.size += c.length; }
      } else if (Object.getPrototypeOf(chunks[i]) === ArrayBuffer.prototype) {
        c = new Uint8Array(chunks[i]);  // sharing data
        if (c.length) { this.chunks.push(c); this.size += c.length; }
      } else if (ArrayBuffer.isView(chunks[i])) {
        c = new Uint8Array(chunks[i].buffer, chunks[i].byteOffset|0, chunks[i].byteLength|0);  // sharing data
        if (c.length) { this.chunks.push(c); this.size += c.length; }
      } else if (chunks[i] instanceof TcBlob) {
        this.chunks.push.apply(this.chunks, chunks[i].chunks);  // sharing data
        this.size += chunks[i].size;
      } else {
        c = new Uint8Array(new TextEncoder("utf-8").encode("" + chunks[i]));  // copying data
        if (c.length) { this.chunks.push(c); this.size += c.length; }
      }
    }
    Object.freeze(this.chunks);
    Object.freeze(this);
  }
  TcBlob.prototype.type = "";
  TcBlob.prototype.size = 0;
  TcBlob.prototype.slice = function (start, end, contentType) {
    var chunks = [], size = this.size|0,
        length = 0, delta = 0,
        cc = this.chunks, ci = 0, cl = cc.length|0,
        v = null, vi = 0, vl = 0;
    start = start|0;
    end = end === undefined ? size|0 : end|0;

    if (end >= size) end = size|0; else if (end <= ~size) return new TcBlob([], {type: contentType}); else if (end < 0) end = (size + end)|0;
    if (start >= size) return new TcBlob([], {type: contentType}); else if (start <= ~size) start = 0; else if (start < 0) start = (size + start)|0;
    if (start >= end) return new TcBlob([], {type: contentType});

    // seek for first eligible chunk, slice the chunk (copy not needed), if last return
    for (; ci < cl; ci += 1) {
      v = cc[ci];
      vl = v.length;
      if (((length + vl)|0) > start) {
        delta = (start - length)|0;
        if (((length + vl)|0) >= end) {
          v = v.slice(delta, (end - length)|0);
          chunks.push(v)
          cl = 0;  // exit all loops
          break;
        }
        v = v.slice(delta);
        chunks.push(v)
        length = (length + vl)|0;
        ci += 1;
        break;
      } else {
        length = (length + vl)|0;
      }
    }
    // push other full chunks (still no copy needed) until end, slice the last chunk (copy not needed)
    for (; ci < cl; ci += 1) {
      v = cc[ci];
      vl = v.length;
      if (((length + vl)|0) >= end) {
        v = v.slice(0, (end - length)|0);
        chunks.push(v)
        break;
      } else {
        chunks.push(v)
        length = (length + vl)|0;
      }
    }
    return new TcBlob(chunks, {type: contentType});
  };

  TcBlob.prototype.readAsBlob = function () {
    return new Blob(this.chunks, {type: this.type});
  };
  TcBlob.prototype.readAsArrayBuffer = function () {
    var n = new Uint8Array(this.size), j = 0, v = null, vi = 0,
        cc = this.chunks, ccl = cc.length, cci = 0;
    for (; cci < ccl; cci += 1) {
      v = cc[cci];
      vi = 0;
      while (vi < v.length) n[j++] = v[vi++];  // not protected from out of bound, as this.size is not writable
    }
    return n.buffer;
  };
  TcBlob.prototype.readAsText = function (encoding) {
    var s = "", d = new TextDecoder(encoding), cc = this.chunks, cci = 0, ccl = cc.length;
    while (cci < ccl) s += d.decode(cc[cci++], {stream: true});
    s += d.decode();
    return s;
  };
  TcBlob.prototype.readAsDataURL = function () {
    return "data:" + (this.type || "application/octet-stream") + ";base64," + btoa(this.readAsBinaryString());  // XXX really use btoa ?
  };
  TcBlob.prototype.readAsBinaryString = function () {
    var s = "", cc = this.chunks, cci = 0, ccl = cc.length, c = null, ci = 0, cl = 0;
    for (; cci < ccl; cci += 1)
      for (c = cc[cci], ci = 0, cl = c.length; ci < cl; ci += 1)
        s += String.fromCharCode(c[ci]);
    return s;
  };

  TcBlob.toScript = function () { return "(" + script.toString() + "())"; };
  TcBlob._requiredGlobals = [
    "btoa",  // XXX really use btoa ?
    "TextEncoder",
    "TextDecoder"
  ];
  return TcBlob;

}());
