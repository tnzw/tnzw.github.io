this.slice = (function script() {
  "use strict";

  /*! slice.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function slice(start, stop, step) {
    // slice(stop)
    // slice(start, stop[, step])
    // Create a slice object.  This is used for extended slicing (e.g. a.slice(0, 10)).
    if (arguments.length === 0) throw new TypeError("slice expected at least 1 argument, got 0");
    else if (arguments.length === 1) {
      if (!(this instanceof slice)) return new slice(start);
      this.start = null;
      this.stop = start;
      this.step = null;
    } else if (arguments.length === 2) {
      if (!(this instanceof slice)) return new slice(start, stop);
      this.start = start;
      this.stop = stop;
      this.step = null;
    } else {
      if (!(this instanceof slice)) return new slice(start, stop, step);
      this.start = start;
      this.stop = stop;
      this.step = step;
    }
  }
  slice.prototype.start = null;
  slice.prototype.stop = null;
  slice.prototype.step = null;
  slice.prototype.getLength = function (len) {
    function toint(v) { return typeof v === "bigint" ? v : v|0 }
    function cast(v,m) { return typeof m === "bigint" ? BigInt(v) : v|0 }
    var indices = this.indices(len),
        start = indices[0],
        stop = indices[1],
        step = indices[2],
        delta, d, m,
        _0 = cast(0, start),
        _1 = cast(1, start);
    if (step < _0) {
      delta = start - stop;
      if (step < _1) {
        d = toint(delta / -step);
        m = toint(delta % -step);
        delta = d + (m ? _1 : _0);
      }
    } else {
      delta = stop - start;
      if (step > _1) {
        d = toint(delta / -step);
        m = toint(delta % -step);
        delta = d + (m ? _1 : _0);
      }
    }
    return delta > _0 ? delta : _0;
  };
  slice.prototype.indices = function (len) {
    // S.indices(len) -> (start, stop, stride)
    // Assuming a sequence of length len, calculate the start and stop
    // indices, and the stride length of the extended slice described by
    // S. Out of bounds indices are clipped in a manner consistent with the
    // handling of normal slices.
    function toint(v) { return typeof v === "bigint" ? v : v|0 }
    function cast(v,m) { return typeof m === "bigint" ? BigInt(v) : v|0 }
    function isnull(v) { return v === null || v === undefined }
    var start = this.start,
        stop = this.stop,
        step = this.step,
        _0 = cast(0, len),
        _1 = cast(1, len);
    len = toint(len);
    if (isnull(step)) step = _1;
    else if (step === _0 || step === 0) throw new TypeError("slice step cannot be zero")
    if (isnull(start)) start = step < _0 ? len - _1 : _0;
    else if (start >= len) start = step < _0 ? len - _1 : len;
    else if (start < -len) start = step < _0 ? -_1 : _0;
    else if (start < _0) start += len;
    if (isnull(stop)) stop = step < _0 ? -_1 : len;
    else if (stop >= len) stop = step < _0 ? len - _1 : len;
    else if (stop < -len) stop = step < _0 ? -_1 : _0;
    else if (stop < _0) stop += len;
    return [start, stop, step]
  };
  slice.prototype.toString = function () { return slice.name + "(" + this.start + ", " + this.stop + ", " + this.step + ")"; };
  slice.toScript = function () { return "(" + script.toString() + "())"; };
  return slice;

})();
