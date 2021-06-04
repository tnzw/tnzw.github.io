this.slice = (function script() {
  "use strict";

  /*! slice.js Version 1.0.1

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
    // S.getLength(len) -> <int32|BigInt>length
    function toint(v) { return typeof v === "bigint" ? v : v|0 }
    function cast(v, m) { return typeof m === "bigint" ? BigInt(v) : v|0 }
    var indices = this.indices(len),  // throws if step is 0 or if len is < 0
        start = indices[0],
        stop = indices[1],
        step = indices[2],
        delta, d, m,
        _0 = cast(0, len),
        _1 = cast(1, len);
    if (step < _0) {
      delta = start - stop;
      if (step < _1) {
        d = toint(delta / -step);
        m = delta % -step;
        delta = d + (m ? _1 : _0);
      }
    } else {  // step is never 0 here
      delta = stop - start;
      if (step > _1) {
        d = toint(delta / step);
        m = delta % step;
        delta = d + (m ? _1 : _0);
      }
    }
    return delta > _0 ? delta : _0;
  };
  slice.prototype.indices = function (len) {
    // S.indices(len) -> <int32|BigInt>(start, stop, stride)
    // Assuming a sequence of length len, calculate the start and stop
    // indices, and the stride length of the extended slice described by
    // S. Out of bounds indices are clipped in a manner consistent with the
    // handling of normal slices.
    function toint(v) { return typeof v === "bigint" ? v : v|0 }
    function cast(v, m) { return typeof m === "bigint" ? BigInt(v) : v|0 }
    function isnull(v) { return v === null || v === undefined }
    var start = this.start,
        stop = this.stop,
        step = this.step,
        _0 = cast(0, len),
        _1 = cast(1, len);
    len = toint(len);
    if (len < _0) throw new TypeError("length should not be negative")
    if (isnull(step)) step = _1;
    else if ((step = cast(step, len)) === _0) throw new TypeError("slice step cannot be zero")
    if (isnull(start)) start = step < _0 ? len - _1 : _0;
    else if ((start = cast(start, len)) >= len) start = step < _0 ? len - _1 : len;
    else if (start < -len) start = step < _0 ? -_1 : _0;
    else if (start < _0) start += len;
    if (isnull(stop)) stop = step < _0 ? -_1 : len;
    else if ((stop = cast(stop, len)) >= len) stop = step < _0 ? len - _1 : len;
    else if (stop < -len) stop = step < _0 ? -_1 : _0;
    else if (stop < _0) stop += len;
    return [start, stop, step]
  };
  slice.prototype.toString = function () { return slice.name + "(" + this.start + ", " + this.stop + ", " + this.step + ")"; };
  slice.toScript = function () { return "(" + script.toString() + "())"; };
  return slice;

})();
