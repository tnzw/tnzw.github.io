this.ChunkView = (function script() {

  /*! ChunkView.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

function ChunkView(chunk, start, end) {
  this.chunk = chunk;
  if (start !== undefined) {
    if (start < 0) this.offset = chunk.length + start;
    else this.offset = start;
  }
  if (end !== undefined) {
    if (end < 0) this.size = chunk.length + end - this.offset;
    else this.size = end - this.offset;
  } else this.size = chunk.length - this.offset;
}
ChunkView.prototype.offset = 0;
ChunkView.prototype.size = 0;
ChunkView.prototype.getSize = function () { if (this.size > 0) return this.size; return 0; };
ChunkView.prototype.get = function (index) {
  var pos = this.offset + index;
  if (pos >= this.offset + this.size)
    return undefined;
  return this.chunk[pos];
};
ChunkView.prototype.set = function (index, value) {
  var pos = this.offset + index;
  if (pos >= this.offset + this.size)
    return;
  this.chunk[this.offset + index] = value;
};

ChunkView.prototype.slice = function (start, end) {
  if (start === undefined) start = 0;
  else if (start < 0) start = this.size + start;
  if (end === undefined) end = this.size;
  else if (end < 0) end = this.size + end;
  start += this.offset;
  end += this.offset;
  if (end > this.offset + this.size) end = this.offset + this.size;
  return new ChunkView(this.chunk, start, end);
};
ChunkView.prototype.forEach = function (fn, thisArg) {
  var o = this.offset, ci = o, i = 0;
  for (; ci < o + this.size; ci += 1)
    fn.call(thisArg, this.chunk[ci], i++, this);
};

ChunkView.prototype.readIntoSlice = function (a, start, end) {
  var ci = this.offset, cend = this.offset + this.size,
      ai = start;
//      ai = 0;
//  if (start === undefined) start = 0;
//  else if (start < 0) start = a.length + start;
//  if (end === undefined) end = a.length;
//  else if (end < 0) end = a.length + end;
//  ai = start;
  while (ci < cend && ai < end)
    a[ai++] = this.chunk[ci++];
  return ai - start;
};
ChunkView.prototype.readAsArray = function () {
  var a = new Array(this.size);
  this.readIntoSlice(a, 0, a.length);
  return a;
};

ChunkView.prototype.pushInto = function (a) {
  var i = this.offset, end = this.offset + this.size;
  for (; i < end; i += 1)
    a.push(this.chunk[i]);
  return a;
};

  ChunkView.toScript = function () { return "(" + script.toString() + "())"; };
  return ChunkView;

}());
