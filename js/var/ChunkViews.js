this.ChunkViews = (function script() {

  /*! ChunkViews.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */


  // XXX https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array
  //     why not use `length` instead of `getSize` on ChunkView ?
  //     what about `map` ?
  //     replace `slice` by `subarray` !
  //     reimplement `set` ! https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/set

function ChunkViews(views) {
  this.views = views;
}
ChunkViews.prototype.getSize = function () {
  var vi = 0, l = 0;
  while (vi < this.views.length)
    l += this.views[vi++].getSize();
  return l;
};
ChunkViews.prototype.get = function (index) {
  var vi = 0, s = 0;
  for (; vi < this.views.length; vi += 1) {
    s = this.views[vi].size;
    if (s > index) return this.views[vi].get(index);
    else index -= s;
  }
};
ChunkViews.prototype.set = function (index, value) {
  var vi = 0, s = 0;
  for (; vi < this.views.length; vi += 1) {
    s = this.views[vi].size;
    if (s > index) return this.views[vi].set(index, value);
    else index -= s;
  }
};

ChunkViews.prototype.append = function (view) {
  var a = new Array(this.views.length + 1), vi = 0;
  for (; vi < this.views.length; vi += 1) a[vi] = this.views[vi];
  a[vi] = view;
  return new ChunkViews(a);
};

ChunkViews.prototype.forEach = function (fn, thisArg) {
  var ths = this, n = 0, i = -1, vi = 0;
  function chunkViewsForEach(v, _i) {
    return fn.call(this, v, (i = _i) + n, ths);
  }
  for (; vi < this.views.length; vi += 1) {
    i = -1
    this.views[vi].forEach(chunkViewsForEach, thisArg);
    n += i + 1;
  }
};
ChunkViews.prototype.slice = function (start, end) {
  var vi = 0, views = [],
      s = 0;

  if (start === undefined) start = 0;
  else if (start < 0) start = (s = this.getSize()) + start;
  if (end === undefined) end = (s || this.getSize());
  else if (end < 0) end = (s || this.getSize()) + end;

  for (; vi < this.views.length; vi += 1) {
    s = this.views[vi].getSize();
    if (start < s) {
      if (end < s) {
        views.push(this.views[vi].slice(start, end));
        return new ChunkViews(views);
      }
      views.push(this.views[vi].slice(start));
      end -= s;
      vi += 1;
      break;
    } else {
      start -= s;
      end -= s;
    }
  }
  for (; vi < this.views.length; vi += 1) {
    s = this.views[vi].getSize();
    if (end < s) {
      views.push(this.views[vi].slice(0, end));
      return new ChunkViews(views);
    }
    views.push(this.views[vi].slice());
  }
  return new ChunkViews(views);
};

ChunkViews.prototype.readIntoSlice = function (a, start, end) {
  var vi = 0,
      ai = start;
  while (vi < this.views.length)
    if ((ai += this.views[vi++].readIntoSlice(a, ai, end)) >= end)
      break;
  return ai - start;
};
ChunkViews.prototype.readAsArray = function () {
  var a = new Array(this.getSize());
  this.readIntoSlice(a, 0, a.length);
  return a;
};
ChunkViews.prototype.pushInto = function (a) {
  for (var vi = 0; vi < this.views.length; vi += 1)
    this.views[vi].pushInto(a);
  return a;
};

  ChunkViews.toScript = function () { return "(" + script.toString() + "())"; };
  return ChunkViews;

}());
