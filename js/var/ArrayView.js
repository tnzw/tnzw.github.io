this.ArrayView = (function script() {
  "use strict";

  /*! ArrayView.js Version 1.1.0

      Copyright (c) 2017-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ArrayView(array, offset, length) {
    // ArrayView(array[, offset[, length]])
    // Inspired by TypedArray and DataView
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray
    this.array = array;
    this.viewOffset = offset|0;
    this.viewLength = length === undefined ? array.length|0 : length|0;
  }
  ArrayView.prototype.array = null;
  ArrayView.prototype.viewOffset = 0;
  ArrayView.prototype.viewLength = 0;

  ArrayView.prototype.copyWithin = function (target, start, end) {
    // arrayview.copyWithin(target, start[, end = this.viewLength])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/copyWithin
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0;

    // force int
    target = target|0;
    start = start|0;
    end = end === undefined ? viewLength|0 : end|0;

    // force positive index
    if (end > viewLength) end = viewLength|0; else if (end <= ~viewLength) return this; else if (end < 0) end = (viewLength + end)|0;
    if (start >= end) return this; else if (start <= ~viewLength) start = 0; else if (start < 0) start = (viewLength + start)|0;
    if (target >= viewLength) return this; else if (target <= ~viewLength) { /*XXXstart = (start - target)|0;*/ target = 0; } else if (target < 0) target = (viewLength + target)|0;

    if (target < start) {
      // use actual array index
      target = (target + viewOffset)|0;
      start = (start + viewOffset)|0;
      end = (end + viewOffset)|0;

      for (; start < end;)
        this.array[target++] = this.array[start++];

    } else if (target > start) {
      // start from last possible index
      target = (target + end - start)|0;
      if (target >= viewLength) { end = (end - target + viewLength)|0; target = viewLength|0; }

      // use actual array index
      target = (target + viewOffset)|0;
      start = (start + viewOffset)|0;
      end = (end + viewOffset)|0;

      for (; start < end;)
        this.array[--target] = this.array[--end];
    }
    return this;
  };
  ArrayView.prototype.entries = function () {
    // arrayview.entries()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/entries
    return new ArrayView.EntriesIterator(this.array, this.viewOffset, this.viewLength);
  };
  ArrayView.prototype.every = function (callback, thisArg) {
    // arrayview.every(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/every
    for (var i = 0; i < (this.viewLength|0); i += 1)
      if (!callback.call(thisArg, this.array[(i + (this.viewOffset|0))|0], i, this))
        return false;
    return true;
  };
  ArrayView.prototype.fill = function (value, start, end) {
    // arrayview.fill(value[, start = 0[, end = this.viewLength])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/fill
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0;

    // force int
    start = start|0;
    end = end === undefined ? viewLength : end|0;

    // force positive index
    if (end > viewLength) end = viewLength|0; else if (end <= ~viewLength) return this; else if (end < 0) end = (viewLength + end)|0;
    if (start >= viewLength) return this; else if (start <= ~viewLength) start = 0; else if (start < 0) start = (viewLength + start)|0;

    // use actual array index
    start = (start + viewOffset)|0;
    end = (end + viewOffset)|0;

    for (; start < end; start += 1)
      this.array[start] = value;
    return this;
  };
  ArrayView.prototype.filter = function (callback, thisArg) {
    // arrayview.filter(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/filter
    var a = [], i = 0, v;
    for (; i < (this.viewLength|0); i += 1) {
      v = this.array[(i + (this.viewOffset|0))|0];
      if (callback.call(thisArg, v, i, this))
        a.push(v)
    }
    return new ArrayView(a, 0, a.length);
  };
  ArrayView.prototype.find = function (callback, thisArg) {
    // arrayview.find(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/find
    var i = 0, v;
    for (; i < (this.viewLength|0); i += 1) {
      v = this.array[(i + (this.viewOffset|0))|0];
      if (callback.call(thisArg, v, i, this))
        return v;
    }
    return undefined;
  };
  ArrayView.prototype.findIndex = function (callback, thisArg) {
    // arrayview.findIndex(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/findIndex
    for (var i = 0; i < (this.viewLength|0); i += 1)
      if (callback.call(thisArg, this.array[(i + (this.viewOffset|0))|0], i, this))
        return i|0;
    return -1;
  };
  ArrayView.prototype.forEach = function (callback, thisArg) {
    // arrayview.forEach(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/forEach
    for (var i = 0; i < (this.viewLength|0); i += 1)
      callback.call(thisArg, this.array[(i + (this.viewOffset|0))|0], i, this);
    return undefined;
  };
  ArrayView.prototype.includes = function (searchElement, fromIndex) {
    // arrayview.includes(searchElement[, fromIndex])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/includes
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0,
        end = (viewLength + viewOffset)|0;
    fromIndex = fromIndex|0;
    if (fromIndex >= viewLength) return false; else if (fromIndex <= ~viewLength) fromIndex = 0; else if (fromIndex < 0) fromIndex = (viewLength + fromIndex)|0;
    fromIndex = (fromIndex + viewOffset)|0;
    for (; fromIndex < end; fromIndex += 1)
      if (this.array[fromIndex] === searchElement)
        return true;
    return false;
  };
  ArrayView.prototype.indexOf = function (searchElement, fromIndex) {
    // arrayview.includes(searchElement[, fromIndex = 0])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/indexOf
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0,
        end = (viewLength + viewOffset)|0;
    fromIndex = fromIndex|0;
    if (fromIndex >= viewLength) return -1; else if (fromIndex <= ~viewLength) fromIndex = 0; else if (fromIndex < 0) fromIndex = (viewLength + fromIndex)|0;
    fromIndex = (fromIndex + viewOffset)|0;
    for (; fromIndex < end; fromIndex += 1)
      if (this.array[fromIndex] === searchElement)
        return (fromIndex - viewOffset)|0;
    return -1;
  };
  ArrayView.prototype.join = function (separator) {
    // arrayview.join([separator = ','])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/join
    var s = "",
        vi = this.viewOffset|0,
        vend = (vi + (this.viewLength|0))|0;
    function tostr(v) { if (v === null || v === undefined) return ""; return ""+v; }
    separator = separator === undefined ? "," : ""+separator;
    if (vi < vend) {
      s += tostr(this.array[vi]);
      for (vi += 1; vi < vend; vi += 1)
        s += separator + tostr(this.array[vi]);
    }
    return s;
  };
  ArrayView.prototype.lastIndexOf = function (searchElement, fromIndex) {
    // arrayview.includes(searchElement[, fromIndex = this.viewLength])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/lastIndexOf
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0,
        start = viewOffset|0;
    fromIndex = fromIndex === undefined ? (viewLength - 1)|0 : fromIndex|0;
    if (fromIndex >= viewLength) fromIndex = (viewLength - 1)|0; else if (fromIndex <= ~viewLength) return -1; else if (fromIndex < 0) fromIndex = (viewLength + fromIndex)|0;
    fromIndex = (fromIndex + viewOffset)|0;

    for (; fromIndex >= start; fromIndex -= 1)
      if (this.array[fromIndex] === searchElement)
        return (fromIndex - viewOffset)|0;
    return -1;
  };
  ArrayView.prototype.map = function (callback, thisArg) {
    // arrayview.map(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/map
    return this.slice().remap(callback, thisArg);
  };
  ArrayView.prototype.reduce = function (callback, initialValue) {
    // arrayview.reduce(callback[, initialValue])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/reduce
    var i = 0;
    if (arguments.length < 2) {
      if ((this.viewLength|0) <= 0) throw new TypeError("reduce of empty array with no initial value");
      initialValue = this.array[this.viewOffset|0];
      i = 1;
    }
    for (; i < (this.viewLength|0); i += 1)
      initialValue = callback(initialValue, this.array[(i + (this.viewOffset|0))|0], i, this);
    return initialValue;
  };
  ArrayView.prototype.reduceRight = function (callback, initialValue) {
    // arrayview.reduceRight(callback[, initialValue])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/reduceRight
    var i = ((this.viewLength|0) - 1)|0;
    if (arguments.length < 2) {
      if ((this.viewLength|0) <= 0) throw new TypeError("reduce of empty array with no initial value");
      initialValue = this.array[((this.viewOffset|0) + i)|0];
      i = (i - 1)|0;
    }
    for (; i >= 0; i -= 1)
      initialValue = callback(initialValue, this.array[(i + (this.viewOffset|0))|0], i, this);
    return initialValue;
  };
  ArrayView.prototype.reverse = function () {
    // arrayview.reverse()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/reverse
    var vs = this.viewOffset|0, ve = (vs + (this.viewLength|0) - 1)|0, v;
    while (vs < ve) {
      v = this.array[ve];
      this.array[ve] = this.array[vs];
      this.array[vs] = v;
      vs = (vs + 1)|0;
      ve = (ve - 1)|0;
    }
    return this;
  };
  ArrayView.prototype.set = function (array, offset) {
    // arrayview.set(array[, offset])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/set
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0,
        ve = (viewOffset + viewLength)|0, i = 0, a = this.array;
    offset = offset|0;
    if (offset < 0 || offset > viewLength) throw new RangeError("invalid or out-of-range index");
    if (array.length > ((viewLength - offset)|0)) throw new RangeError("invalid array length");
    offset = (offset + viewOffset)|0;
    // do not use array.values,
    // if it's a sparse array it does not work.
    for (; offset < ve && i < array.length; offset += 1, i += 1)
      a[offset] = array[i];
    return undefined;
  };
  ArrayView.prototype.slice = function (begin, end) {
    // arrayview.slice([begin[, end]])
    // Copy the content of the view into another view.
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/slice
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0;
    begin = begin|0;
    end = end === undefined ? viewLength : end|0;

    if (end >= viewLength) end = viewLength|0; else if (end <= ~viewLength) return new ArrayView([], 0, 0); else if (end < 0) end = (viewLength + end)|0;
    if (begin >= viewLength) return new ArrayView([], 0, 0); else if (begin <= ~viewLength) begin = 0; else if (begin < 0) begin = (viewLength + begin)|0;

    if (begin > end) return new ArrayView([], 0, 0);
    begin = (begin + viewOffset)|0;
    end = (end + viewOffset)|0;
    return new ArrayView(this.array.slice(begin, end), 0, end - begin);
  };
  ArrayView.prototype.some = function (callback, thisArg) {
    // arrayview.some(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/some
    for (var i = 0; i < (this.viewLength|0); i += 1)
      if (callback.call(thisArg, this.array[(i + (this.viewOffset|0))|0], i, this))
        return true;
    return false;
  };
  ArrayView.prototype.sort = function (compareFunction) {
    // arrayview.sort([compareFunction])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/sort
    // XXX copy code of `set` only for this purpose, check for RangeError is not necessary for instance..
    var viewOffset = this.viewOffset|0;
    // should we use `this.readAsArray` instead of `Array.slice` ?
    this.set(this.array.slice(viewOffset, (viewOffset + (this.viewLength|0))|0).sort(compareFunction));
    return this;
  };
  ArrayView.prototype.subarray = function (begin, end) {
    // arrayview.subarray([begin[, end]])
    // Create a new view based on the same array.
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/subarray
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0;
    begin = begin|0;
    end = end === undefined ? viewLength : end|0;

    if (end >= viewLength) end = viewLength|0; else if (end <= ~viewLength) return new ArrayView(this.array, 0, 0); else if (end < 0) end = (viewLength + end)|0;
    if (begin >= viewLength) return new ArrayView(this.array, 0, 0); else if (begin <= ~viewLength) begin = 0; else if (begin < 0) begin = (viewLength + begin)|0;

    if (begin > end) return new ArrayView(this.array, 0, 0);
    return new ArrayView(this.array, (begin + viewOffset)|0, (end - begin + viewOffset)|0);
  };
  // XXX ArrayView.prototype.toLocaleString = function (callback, thisArg) {
  ArrayView.prototype.toString = function () {
    // arrayview.toString()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/toString
    return this.join(",");
  };
  ArrayView.prototype.values = function () {
    // arrayview.values()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/values
    return new ArrayView.ValuesIterator(this.array, this.viewOffset, this.viewLength);
  };

  ArrayView.prototype.remap = function (callback, thisArg) {
    // arrayview.remap(callback[, thisArg])
    var i = 0, pos = 0;
    for (; i < (this.viewLength|0); i += 1) {
      pos = ((this.viewOffset|0) + i)|0;
      this.array[pos] = callback.call(thisArg, this.array[pos], i, this);
    }
    return this;
  };

  ArrayView.prototype.valueAt = function (index) {
    // arrayview.valuesAt(index)
    index = index|0;
    if (index < 0 || index >= (this.viewLength|0)) return undefined;
    return this.array[(index + (this.viewOffset|0))|0];
  };
  ArrayView.prototype.readAsArray = function () {
    // arrayview.readAsArray()
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0,
        a = new Array(viewLength),  // throws RangeError if length < 0
        j = 0, i = viewOffset|0, max = (i + viewLength)|0;
    while (i < max) a[j++] = this.array[i++];
    return a;
  };
  ArrayView.prototype.readInto = function (array) {
    // arrayview.readInto()
    var viewLength = this.viewLength|0,
        viewOffset = this.viewOffset|0,
        j = 0, i = viewOffset|0, max = (i + viewLength)|0;
    while (i < max && j < array.length) a[j++] = this.array[i++];
    return j;
  };
  ArrayView.prototype.pushInto = function (pushable) {
    // arrayview.pushInto(pushable)
    var i = (this.viewOffset|0), max = (i + (this.viewLength|0))|0;
    while (i < max) pushable.push(this.array[i++]);
    return pushable;
  };

  function EntriesIterator(array, offset, length) {
    this.index = 0;
    this.array = array;
    this.viewOffset = offset|0;
    this.viewLength = length|0;
  }
  EntriesIterator.prototype.array = null;
  EntriesIterator.prototype.viewOffset = 0;
  EntriesIterator.prototype.viewLength = 0;
  EntriesIterator.prototype.index = 0;
  EntriesIterator.prototype.next = function () {
    var i = this.index|0;
    if (i < this.viewLength)
      return {done: false, value: [this.index++, this.array[i + this.viewOffset]]};
    return {done: true, value: undefined};
  };

  function ValuesIterator(array, offset, length) {
    this.index = 0;
    this.array = array;
    this.viewOffset = offset|0;
    this.viewLength = length|0;
  }
  ValuesIterator.prototype.array = null;
  ValuesIterator.prototype.viewOffset = 0;
  ValuesIterator.prototype.viewLength = 0;
  ValuesIterator.prototype.index = 0;
  ValuesIterator.prototype.next = function () {
    if (this.index < this.viewLength)
      return {done: false, value: this.array[(this.index++) + this.viewOffset]};
    return {done: true, value: undefined};
  };

  ArrayView.EntriesIterator = EntriesIterator;
  ArrayView.ValuesIterator = ValuesIterator;
  ArrayView.toScript = function () { return "(" + script.toString() + "())"; };
  return ArrayView;

}());
