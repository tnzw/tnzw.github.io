this.ArrayViews = (function script() {
  "use strict";

  /*! ArrayViews.js Version 1.1.2

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ArrayViews(views) {
    // new ArrayViews([new ArrayView(array, 0, array.length), ...])
    // new ArrayViews([{array: array, viewOffset: 0, viewLength: array.length}, ...])
    // Inspired by TypedArray and DataView
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray
    var i = 0, copy = new Array(views.length);
    this.views = copy;
    this.length = 0;
    for (; i < views.length; i += 1)
      copy[i] = {
        array:       views[i].array         || [],
        viewOffset: (views[i].viewOffset|0) || 0,
        viewLength: (views[i].viewLength|0) || 0
      };
    this.refreshLength();
  }
  ArrayViews.prototype.views = null;
  ArrayViews.prototype.length = 0;

  ArrayViews.prototype.copyWithin = function (target, start, end) {
    // arrayviews.copyWithin(target, start[, end = this.length])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/copyWithin

    var totalLength = this.length|0, l = 0,
        vv = this.views, vvl = 0,
        targetvvi = 0, targetvi = 0, targetvl = 0,
        startvvi = 0, startvi = 0, startvl = 0;

    if (totalLength === 0) return this;

    // force int
    target = target|0;
    start = start|0;
    end = end === undefined ? totalLength|0 : end|0;

    // force positive index
    if (end > totalLength) end = totalLength|0; else if (end <= ~totalLength) return this; else if (end < 0) end = (totalLength + end)|0;
    /*if (start >= end) return this; else*/ if (start <= ~totalLength) start = 0; else if (start < 0) start = (totalLength + start)|0;
    if (start >= end) return this;
    if (target >= totalLength) return this; else if (target <= ~totalLength) target = 0; else if (target < 0) target = (totalLength + target)|0;

    if (target < start) {
      end = (end - start)|0;
      l = vv[0].viewLength|0; while (l < target) { target = (target - l)|0; l = vv[++targetvvi].viewLength|0; }
      l = vv[0].viewLength|0; while (l < start ) { start  = (start  - l)|0; l = vv[++startvvi ].viewLength|0; }
      targetvi = vv[targetvvi].viewOffset|0;
      startvi  = vv[startvvi ].viewOffset|0;
      targetvl = (targetvi + (vv[targetvvi].viewLength|0))|0;
      startvl  = (startvi  + (vv[startvvi ].viewLength|0))|0;
      targetvi = (targetvi + target)|0;
      startvi  = (startvi  + start )|0;
      while (end--) {
        while (targetvi >= targetvl) { targetvi = vv[++targetvvi].viewOffset|0; targetvl = (targetvi + (vv[targetvvi].viewLength|0))|0; }
        while (startvi  >= startvl ) { startvi  = vv[++startvvi ].viewOffset|0; startvl  = (startvi  + (vv[startvvi ].viewLength|0))|0; }
        vv[targetvvi].array[targetvi++] = vv[startvvi].array[startvi++];
      }
    } else if (target > start) {
      end = (end - start)|0;
      if (((target + end)|0) > totalLength) end = (totalLength - target)|0;
      start = (target - start)|0;
      // OR start = (end - target + start)|0;

      startvvi = targetvvi = ((this.views.length|0) - 1)|0;
      // OR targetvvi = ((this.views.length|0) - 1)|0;
      l = vv[startvvi].viewLength|0; while (l < start) { start = (start - l)|0; l = vv[--startvvi].viewLength|0; }
      // OR l = vv[0].viewLength|0; while (l < start ) { start  = (start  - l)|0; l = vv[++startvvi ].viewLength|0; }
      targetvl = vv[targetvvi].viewOffset|0;
      startvl  = vv[startvvi ].viewOffset|0;
      targetvi = (targetvl + (vv[targetvvi].viewLength|0) - 1)|0
      startvi  = (startvl + l - start - 1)|0;
      // OR startvi  = (startvl + start - 1)|0;
      while (end--) {
        while (targetvi < targetvl) { targetvl = vv[--targetvvi].viewOffset|0; targetvi = (targetvl + (vv[targetvvi].viewLength|0) - 1)|0; }
        while (startvi  < startvl ) { startvl  = vv[--startvvi ].viewOffset|0; startvi  = (startvl  + (vv[startvvi ].viewLength|0) - 1)|0; }
        vv[targetvvi].array[targetvi--] = vv[startvvi].array[startvi--];
      }
    }
    return this;
  };
  ArrayViews.prototype.entries = function () {
    // arrayviews.entries()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/entries
    return new ArrayViews.EntriesIterator(this.views);
  };
  ArrayViews.prototype.every = function (callback, thisArg) {
    // arrayviews.every(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/every
    // knowing that `every` can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
        if (!callback.call(thisArg, v.array[(vi + (v.viewOffset|0))|0], i++, this))
          return false;
    return true;
    // // Here, we use a modified version of `valueAt` to also detect end of iteration.
    // var i = 0, cont = true, v;
    // function valueAt(index) {
    //   index = index|0;
    //   var vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
    //   l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) { cont = false; return undefined; } index = (index - l)|0; l = vv[vvi].viewLength|0; }
    //   v = vv[vvi];
    //   return v.array[((v.viewOffset|0) + index)|0];
    // }
    // v = valueAt.call(this, 0);
    // while (cont) { if (!callback.call(thisArg, v, i, this)) return false; v = valueAt.call(this, ++i); }
    // return true;
  };
  ArrayViews.prototype.fill = function (value, start, end) {
    // arrayviews.fill(value[, start = 0[, end = this.length])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/fill
    var views = this.views, newViews = [],
        totalLength = this.length|0,
        length = 0, vvi = 0, vvl = views.length|0,
        v = null, vl = 0, delta = 0,
        wi = 0, wl = 0;
    start = start|0;
    end = end === undefined ? totalLength|0 : end|0;
    value = this._cast(value);

    if (end >= totalLength) end = totalLength|0; else if (end <= ~totalLength) return this; else if (end < 0) end = (totalLength + end)|0;
    if (start >= totalLength) return this; else if (start <= ~totalLength) start = 0; else if (start < 0) start = (totalLength + start)|0;
    if (start >= end) return this;

    // seek for first eligible view, fill view part, if last return
    for (; vvi < vvl; vvi += 1) {
      v = views[vvi];
      vl = v.viewLength|0;
      if (((length + vl)|0) > start) {
        delta = (start - length)|0;
        if (((length + vl)|0) >= end) {
          wi = ((v.viewOffset|0) + delta)|0;
          wl = (wi + (end - length - delta)|0)|0;
          for (; wi < wl; wi = (wi + 1)|0) v.array[wi] = value;
          vvl = 0;  // exit all loops
          break;
        }
        wi = ((v.viewOffset|0) + delta)|0;
        wl = (wi + (((v.viewLength|0) - delta)|0))|0;
        for (; wi < wl; wi = (wi + 1)|0) v.array[wi] = value;
        length = (length + vl)|0;
        vvi += 1;
        break;
      } else {
        length = (length + vl)|0;
      }
    }
    // fill full views and last view part
    for (; vvi < vvl; vvi += 1) {
      v = views[vvi];
      vl = v.viewLength|0;
      if (((length + vl)|0) >= end) {
        wi = v.viewOffset|0;
        wl = (wi + ((end - length)|0))|0;
        for (; wi < wl; wi = (wi + 1)|0) v.array[wi] = value;
        break;
      } else {
        wi = v.viewOffset|0;
        wl = (wi + (v.viewLength|0))|0;
        for (; wi < wl; wi = (wi + 1)|0) v.array[wi] = value;
      }
    }
    return this;
  };
  ArrayViews.prototype.filter = function (callback, thisArg) {
    // arrayviews.filter(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/filter
    // knowing that `filter` can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0, a = [], value;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
        if (callback.call(thisArg, value = v.array[(vi + (v.viewOffset|0))|0], i++, this))
          a.push(value);
    return new this.constructor([{array: a, viewOffset: 0, viewLength: a.length}]);
    // // Here, we use a modified version of `valueAt` to also detect end of iteration.
    // var i = 0, cont = true, a = [], v;
    // function valueAt(index) {
    //   index = index|0;
    //   var vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
    //   l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) { cont = false; return undefined; } index = (index - l)|0; l = vv[vvi].viewLength|0; }
    //   v = vv[vvi];
    //   return v.array[((v.viewOffset|0) + index)|0];
    // }
    // v = valueAt.call(this, 0);
    // while (cont) { if (callback.call(thisArg, v, i, this)) a.push(v); v = valueAt.call(this, ++i); }
    // return new this.constructor([{array: a, viewOffset: 0, viewLength: a.length}]);
  };
  ArrayViews.prototype.find = function (callback, thisArg) {
    // arrayviews.find(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/find
    // knowing that `find` can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0, value;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
        if (callback.call(thisArg, value = v.array[(vi + (v.viewOffset|0))|0], i++, this))
          return value;
    return undefined;
  };
  ArrayViews.prototype.findIndex = function (callback, thisArg) {
    // arrayviews.findIndex(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/findIndex
    // knowing that `findIndex` can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1, i += 1)
        if (callback.call(thisArg, v.array[(vi + (v.viewOffset|0))|0], i, this))
          return i|0;
    return -1;
  };
  ArrayViews.prototype.forEach = function (callback, thisArg) {
    // arrayviews.forEach(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/forEach
    // knowing that forEach can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
        callback.call(thisArg, v.array[(vi + (v.viewOffset|0))|0], i++, this);
    return undefined;
    // // Here, we use a modified version of `valueAt` to also detect end of iteration.
    // var i = 0, cont = true, v;
    // function valueAt(index) {
    //   index = index|0;
    //   var vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
    //   l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) { cont = false; return undefined; } index = (index - l)|0; l = vv[vvi].viewLength|0; }
    //   v = vv[vvi];
    //   return v.array[((v.viewOffset|0) + index)|0];
    // }
    // v = valueAt.call(this, 0);
    // while (cont) { callback.call(thisArg, v, i, this); v = valueAt.call(this, ++i); }
    // return undefined;
  };
  ArrayViews.prototype.includes = function (searchElement, fromIndex) {
    // arrayviews.includes(searchElement[, fromIndex])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/includes
    var totalLength = this.length|0,
        vv = this.views, vvi = 0, vvl = vv.length|0,
        v = null, vi = 0, va = null, vl = 0,
        l = 0;

    fromIndex = fromIndex|0;
    if (fromIndex >= totalLength) return false; else if (fromIndex <= ~totalLength) fromIndex = 0; else if (fromIndex < 0) fromIndex = (totalLength + fromIndex)|0;

    v = vv[vvi];
    l = v.viewLength|0; while (l < fromIndex) { fromIndex = (fromIndex - l)|0; v = vv[++vvi]; l = v.viewLength|0; }

    va = v.array;
    vi = v.viewOffset|0;
    vl = (vi + (v.viewLength|0))|0;
    vi = (vi + fromIndex)|0;

    // Documentation does not tell to use array iterator.
    // Anyway, iterator does not work with sparse array.
    for (; vi < vl; vi += 1)
      if (va[vi] === searchElement)
        return true;

    for (vvi += 1; vvi < vvl; vvi += 1)
      for (v = vv[vvi], vi = v.viewOffset|0, va = v.array, vl = (vi + (v.viewLength|0))|0; vi < vl; vi += 1)
        if (va[vi] === searchElement)
          return true;

    return false;
  };
  ArrayViews.prototype.indexOf = function (searchElement, fromIndex) {
    // arrayviews.indexOf(searchElement[, fromIndex = 0])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/indexOf
    var totalLength = this.length|0,
        vv = this.views, vvi = 0, vvl = vv.length|0,
        v = null, vi = 0, va = null, vl = 0,
        l = 0;

    fromIndex = fromIndex|0;
    if (fromIndex >= totalLength) return -1; else if (fromIndex <= ~totalLength) fromIndex = 0; else if (fromIndex < 0) fromIndex = (totalLength + fromIndex)|0;

    v = vv[vvi];
    l = v.viewLength|0; while (l < fromIndex) { fromIndex = (fromIndex - l)|0; v = vv[++vvi]; l = v.viewLength|0; }

    va = v.array;
    vi = v.viewOffset|0;
    vl = (vi + (v.viewLength|0))|0;
    vi = (vi + fromIndex)|0;

    // Documentation does not tell to use array iterator.
    // Anyway, iterator does not work with sparse array.
    for (; vi < vl; vi += 1, fromIndex += 1)
      if (va[vi] === searchElement)
        return fromIndex|0;

    for (vvi += 1; vvi < vvl; vvi += 1)
      for (v = vv[vvi], vi = v.viewOffset|0, va = v.array, vl = (vi + (v.viewLength|0))|0; vi < vl; vi += 1, fromIndex += 1)
        if (va[vi] === searchElement)
          return fromIndex|0;

    return -1;
  };
  ArrayViews.prototype.join = function (separator) {
    // arrayviews.join([separator = ','])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/join
    var vvi = 0, vvl = this.views.length|0,
        v = null, vi = 0, vl = 0, va = null, s = "";
    separator = separator === undefined ? "," : ""+separator;
    function tostr(v) { if (v === null || v === undefined) return ""; return ""+v; }
    for (; vvi < vvl; vvi += 1) {
      v = this.views[vvi];
      vl = v.viewLength|0;
      if (vl > 0) {
        va = v.array;
        vi = v.viewOffset|0;
        vl = (vl + vi)|0;
        s = tostr(va[v.viewOffset|0]);
        for (vi += 1; vi < vl; vi += 1)
          s += separator + tostr(va[vi]);
        break;
      }
    }
    for (vvi += 1; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], va = v.array, vi = v.viewOffset|0, vl = (vi + (v.viewLength|0))|0; vi < vl; vi += 1)
        s += separator + tostr(va[vi]);
    return s;
  };
  ArrayViews.prototype.lastIndexOf = function (searchElement, fromIndex) {
    // arrayviews.lastIndexOf(searchElement[, fromIndex = this.length])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/lastIndexOf
    var totalLength = this.length|0,
        vv = this.views, vvi = 0, vvl = vv.length|0,
        v = null, vi = 0, va = null, vl = 0,
        l = 0;

    fromIndex = fromIndex === undefined ? totalLength : fromIndex|0;
    if (fromIndex >= totalLength) fromIndex = totalLength|0; else if (fromIndex <= ~totalLength) return -1; else if (fromIndex < 0) fromIndex = (totalLength + fromIndex)|0;

    v = vv[vvi];
    l = v.viewLength|0; while (l < fromIndex) { fromIndex = (fromIndex - l)|0; v = vv[++vvi]; l = v.viewLength|0; }

    va = v.array;
    vi = v.viewOffset|0;
    vl = (vi + fromIndex)|0;

    // Documentation does not tell to use array iterator.
    // Anyway, iterator does not work with sparse array.
    for (; vi < vl; fromIndex -= 1)
      if (va[--vl] === searchElement)
        return (fromIndex - 1)|0;

    for (vvi -= 1; vvi >= 0; vvi -= 1)
      for (v = vv[vvi], vi = v.viewOffset|0, va = v.array, vl = (vi + (v.viewLength|0))|0; vi < vl; fromIndex -= 1)
        if (va[--vl] === searchElement)
          return (fromIndex - 1)|0;

    return -1;
  };
  ArrayViews.prototype.map = function (callback, thisArg) {
    // arrayviews.map(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/map
    return this.slice().remap(callback, thisArg);
  };
  ArrayViews.prototype.reduce = function (callback, initialValue) {
    // arrayviews.reduce(callback[, initialValue])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/reduce
    // knowing that reduce can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0;
    if (arguments.length < 2) {
      if ((this.length|0) <= 0) throw new TypeError("reduce of empty array with no initial value");
      for (; vvi < vvl; vvi += 1)
        for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
          { initialValue = v.array[(vi + (v.viewOffset|0))|0]; i += 1; vvl = 0; vi += 1; break; }
      vvl = this.views.length|0;
      for (; vi < (v.viewLength|0); vi += 1)
        initialValue = callback(initialValue, v.array[(vi + (v.viewOffset|0))|0], i++, this);
    }
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
        initialValue = callback(initialValue, v.array[(vi + (v.viewOffset|0))|0], i++, this);
    return initialValue;
  };
  ArrayViews.prototype.reduceRight = function (callback, initialValue) {
    // arrayviews.reduceRight(callback[, initialValue])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/reduceRight
    // knowing that reduceRight can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = this.length|0;
    if (arguments.length < 2) {
      if ((this.length|0) <= 0) throw new TypeError("reduce of empty array with no initial value");
      for (; vvi < vvl;)
        for (v = this.views[--vvl], vi = (v.viewLength|0); 0 < vi;)
          { initialValue = v.array[(--vi + (v.viewOffset|0))|0]; i += 1; vvi = vvl|0; break; }
      vvi = 0;
      for (; 0 < vi;)
        initialValue = callback(initialValue, v.array[(--vi + (v.viewOffset|0))|0], --i, this);
    }
    for (; vvi < vvl;)
      for (v = this.views[--vvl], vi = (v.viewLength|0); 0 < vi;)
        initialValue = callback(initialValue, v.array[(--vi + (v.viewOffset|0))|0], --i, this);
    return initialValue;
  };
  ArrayViews.prototype.reverse = function () {
    // arrayviews.reverse()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/reverse
    // This algo can be optimized.
    var startvvi = 0, startv = this.views[startvvi], startvi = startv.viewOffset|0,
        endvvi = ((this.views.length|0) - 1)|0, endv = this.views[endvvi], endvi = ((endv.viewLength|0) + (endv.viewOffset|0) - 1)|0,
        value;

    while (startvvi < endvvi || (startvvi === endvvi && startvi < endvi)) {
      if (startvi >= ((startv.viewLength|0) + (startv.viewOffset|0))|0) {
        startvvi = (startvvi + 1)|0;
        startv = this.views[startvvi];
        startvi = startv.viewOffset|0;
      } else if (endvi < (endv.viewOffset|0)) {
        endvvi = (endvvi - 1)|0;
        endv = this.views[endvvi];
        endvi = ((endv.viewLength|0) + (endv.viewOffset|0) - 1)|0;
      } else {
        value = endv.array[endvi];
        endv.array[endvi] = startv.array[startvi];
        startv.array[startvi] = value;
        startvi += 1;
        endvi -= 1;
      }
    }

    return this;
  };
  ArrayViews.prototype.set = function (array, offset) {
    // arrayviews.set(array[, offset])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/set
    var totalLength = this.length|0,
        vv = this.views, vvi = 0, vvl = vv.length|0, v = null, vi = 0, va = null, vl = 0,
        ai = 0, al = array.length|0, l = 0;

    offset = offset|0;

    if (al > ((totalLength - offset)|0)) throw new RangeError("source is too large");
    if (totalLength <= 0) return undefined;

    v = vv[vvi];
    l = v.viewLength|0; while (l < offset) { offset = (offset - l)|0; v = vv[++vvi]; l = v.viewLength|0; }

    va = v.array;
    vi = v.viewOffset|0;
    vl = (vi + (v.viewLength|0))|0;
    vi = (vi + offset)|0;

    // Documentation does not tell to use array iterator.
    // Anyway, iterator does not work with sparse array.
    for (; ai < al && vi < vl; ai += 1, vi += 1)
      va[vi] = this._cast(array[ai]);

    for (vvi += 1; ai < al && vvi < vvl; vvi += 1)
      for (v = vv[vvi], vi = v.viewOffset|0, va = v.array, vl = (vi + (v.viewLength|0))|0; ai < al && vi < vl; ai += 1, vi += 1)
        va[vi] = this._cast(array[ai]);

    return undefined;
  };
  ArrayViews.prototype.slice = function (begin, end) {
    // arrayviews.slice([begin[, end]])
    // Copy the content of the views into other views.
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/slice

    // reuse internal arrays by calling `slice` on them ??? (and may be concat ?)
    // so that we can use native optimization of `slice`. doc would be:
    // // Here, we don't want to flatten arrays by just doing a `this.readAsArray`,
    // // we want to reuse internal javascript optimizations of `Array.slice`.

    var a = this.subarray(begin, end).readAsArray();
    return new this.constructor([{array: a, viewOffset: 0, viewLength: a.length}]);
  };
  ArrayViews.prototype.some = function (callback, thisArg) {
    // arrayviews.some(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/some
    // knowing that `some` can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a double loop version. It is ok if we assume that we don't edit the views object during the iteration.
    var vvi = 0, vvl = this.views.length|0, v = null, vi = 0, i = 0;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], vi = 0; vi < (v.viewLength|0); vi += 1)
        if (callback.call(thisArg, v.array[(vi + (v.viewOffset|0))|0], i++, this))
          return true;
    return false;
  };
  ArrayViews.prototype.sort = function (compareFunction, thisArg) {
    // arrayviews.sort(callback[, thisArg])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/sort
    // XXX Do not use `readAsArray` if this ArrayViews uses only one array...
    //     doc would be: Should we use anyway `this.readAsArray` instead of `slice` ?
    // XXX copy code of `set` only for this purpose, check for RangeError is not necessary for instance..
    this.set(this.readAsArray().sort(compareFunction, thisArg));
    return this;
  };
  ArrayViews.prototype.subarray = function (begin, end) {
    // arrayviews.subarray([begin[, end]])
    // Create a new view based on the same array.
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/subarray
    var views = this.views, newViews = [],
        totalLength = this.length|0,
        length = 0, vvi = 0, vvl = views.length|0,
        v = null, vl = 0, delta = 0;
    begin = begin|0;
    end = end === undefined ? totalLength|0 : end|0;

    if (end >= totalLength) end = totalLength|0; else if (end <= ~totalLength) return new this.constructor([]); else if (end < 0) end = (totalLength + end)|0;
    if (begin >= totalLength) return new this.constructor([]); else if (begin <= ~totalLength) begin = 0; else if (begin < 0) begin = (totalLength + begin)|0;
    if (begin >= end) return new this.constructor([]);

    // seek for first eligible view, append view part, if last return
    for (; vvi < vvl; vvi += 1) {
      v = views[vvi];
      vl = v.viewLength|0;
      if (((length + vl)|0) > begin) {
        delta = (begin - length)|0;
        if (((length + vl)|0) >= end) {
          //newViews.push(new ArrayView(v.array, ((v.viewOffset|0) + delta)|0, (end - length - delta)|0));
          newViews.push({array: v.array, viewOffset: ((v.viewOffset|0) + delta)|0, viewLength: (end - length - delta)|0});
          vvl = 0;  // exit all loops
          break;
        }
        //newViews.push(new ArrayView(v.array, ((v.viewOffset|0) + delta)|0, ((v.viewLength|0) - delta)|0));
        newViews.push({array: v.array, viewOffset: ((v.viewOffset|0) + delta)|0, viewLength: ((v.viewLength|0) - delta)|0});
        length = (length + vl)|0;
        vvi += 1;
        break;
      } else {
        length = (length + vl)|0;
      }
    }
    // append full views and last view part
    for (; vvi < vvl; vvi += 1) {
      v = views[vvi];
      vl = v.viewLength|0;
      if (((length + vl)|0) >= end) {
        //newViews.push(new ArrayView(v.array, v.viewOffset|0, (end - length)|0));
        newViews.push({array: v.array, viewOffset: v.viewOffset|0, viewLength: (end - length)|0});
        break;
      } else {
        //newViews.push(new ArrayView(v.array, v.viewOffset|0, v.viewLength|0));
        newViews.push({array: v.array, viewOffset: v.viewOffset|0, viewLength: v.viewLength|0});
        length = (length + vl)|0;
      }
    }
    return new this.constructor(newViews);
  };
  ArrayViews.prototype.toLocaleString = function (locales, options) {
    // arrayviews.toLocaleString([locales[, options]])
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/toLocaleString
    // Code is completely copied from the join method, except for the tostr function and the separator definition.
    var vvi = 0, vvl = this.views.length|0,
        v = null, vi = 0, vl = 0, va = null, s = "",
        separator = ",";
    function tostr(v) { if (v === null || v === undefined) return ""; if (typeof v.toLocaleString === "function") return v.toLocaleString(locales, options); return ""+v; }
    for (; vvi < vvl; vvi += 1) {
      v = this.views[vvi];
      vl = v.viewLength|0;
      if (vl > 0) {
        va = v.array;
        vi = v.viewOffset|0;
        vl = (vl + vi)|0;
        s = tostr(va[v.viewOffset|0]);
        for (vi += 1; vi < vl; vi += 1)
          s += separator + tostr(va[vi]);
        break;
      }
    }
    for (vvi += 1; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], va = v.array, vi = v.viewOffset|0, vl = (vi + (v.viewLength|0))|0; vi < vl; vi += 1)
        s += separator + tostr(va[vi]);
    return s;
  };
  ArrayViews.prototype.toString = function () {
    // arrayviews.toString()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/toString
    return this.join(",");
  };
  ArrayViews.prototype.values = function () {
    // arrayviews.values()
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/values
    return new ArrayViews.ValuesIterator(this.views);
  };

  ArrayViews.prototype.remap = function (callback, thisArg) {
    // arrayviews.remap(callback[, thisArg])
    // knowing that remap can modify the current Views what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a modified version of `valueAt` to also detect end of iteration.
    var i = 0, cont = true, v;
    function valueAt(index) {
      index = index|0;
      var vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
      l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) { cont = false; return undefined; } index = (index - l)|0; l = vv[vvi].viewLength|0; }
      v = vv[vvi];
      return v.array[((v.viewOffset|0) + index)|0];
    }
    function setValueAt(index, value) {
      index = index|0;
      var vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
      l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) { cont = false; return undefined; } index = (index - l)|0; l = vv[vvi].viewLength|0; }
      v = vv[vvi];
      v.array[((v.viewOffset|0) + index)|0] = value;
      index = (index + 1)|0;
      l = vv[vvi].viewLength|0; while (l <= index) { if (++vvi >= vvl) { cont = false; return undefined; } index = (index - l)|0; l = vv[vvi].viewLength|0; }
      v = vv[vvi];
      return v.array[((v.viewOffset|0) + index)|0];
    }
    v = valueAt.call(this, 0);
    while (cont) { v = setValueAt.call(this, i, this._cast(callback.call(thisArg, v, i, this))); i += 1; }
    return undefined;
  };

  ArrayViews.prototype._cast = function (value) {
    // arrayviews._cast(value)
    // can be overriden by sub classes to create typed views
    // ex:
    //   function Uint8Views(views) { return ArrayViews.call(this, views); }
    //   mixin(Uint8Views.prototype, ArrayViews.prototype)
    //   Uint8Views.prototype._cast = function (value) { return value & 0xFF; };
    return value;
  };
  //ArrayViews.prototype._uncast = function (value) { return value; };  // is it necessary ? it could be if we pass `new Uint8Views([{array: ['a']}])`

  ArrayViews.prototype.refreshLength = function () {
    // arrayviews.refreshLength()
    // No need to have a getLength method, as the views length should not be mutable.
    var vi = 0, vl = this.views.length|0, length = 0;
    for (; vi < vl; vi += 1) length = (length + (this.views[vi].viewLength|0))|0;
    this.length = length|0;
    return length|0;
  };
  ArrayViews.prototype.getLength = ArrayViews.prototype.refreshLength;  // BBB
  ArrayViews.prototype.valueAt = function (index) {
    // arrayviews.valueAt(index)
    index = index|0;
    var vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
    l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) return undefined; index = (index - l)|0; l = vv[vvi].viewLength|0; }
    v = vv[vvi];
    return v.array[((v.viewOffset|0) + index)|0];
  };
  ArrayViews.prototype.readAsArray = function () {
    // arrayviews.readAsArray()
    var a = new Array(this.length|0),
        vvi = 0, vvl = this.views.length|0,
        v = null, vi = 0, vl = 0, va = null, ai = 0;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], va = v.array, vi = v.viewOffset|0, vl = ((v.viewLength|0) + vi)|0; vi < vl; vi += 1)
        a[ai++] = va[vi];
    return a;
  };
  ArrayViews.prototype.readInto = function (array) {
    // arrayviews.readInto(array)
    var vvi = 0, vvl = this.views.length|0,
        v = null, vi = 0, vl = 0, va = null, ai = 0;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], va = v.array, vi = v.viewOffset|0, vl = ((v.viewLength|0) + vi)|0; vi < vl; vi += 1)
        if (ai < array.length) array[ai++] = va[vi];
        else return ai;
    return ai;
  };
  ArrayViews.prototype.pushInto = function (pushable) {
    // arrayviews.pushInto(pushable)
    var vvi = 0, vvl = this.views.length|0,
        v = null, vi = 0, vl = 0, va = null;
    for (; vvi < vvl; vvi += 1)
      for (v = this.views[vvi], va = v.array, vi = v.viewOffset|0, vl = ((v.viewLength|0) + vi)|0; vi < vl; vi += 1)
        pushable.push(va[vi]);
    return pushable;
  };

  function EntriesIterator(views) {
    this.views = views;
    this.index = 0;
  }
  EntriesIterator.prototype.views = null;
  EntriesIterator.prototype.index = 0;
  EntriesIterator.prototype.next = function () {
    // knowing that user can modify the current Views during the iteration what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a modified version of `valueAt`.
    var index = this.index|0;
        vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
    l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) return {done: true, value: undefined}; index = (index - l)|0; l = vv[vvi].viewLength|0; }
    v = vv[vvi];
    return {done: false, value: [this.index++, v.array[((v.viewOffset|0) + index)|0]]};
  };

  function ValuesIterator(views) {
    this.views = views;
    this.index = 0;
  }
  ValuesIterator.prototype.views = null;
  ValuesIterator.prototype.index = 0;
  ValuesIterator.prototype.next = function () {
    // knowing that user can modify the current Views during the iteration what strategy to use ?
    // use double loop ? use iterator ? use `valueAt` ? use something else ?
    // Here, we use a modified version of `valueAt`.
    var index = this.index|0;
        vvi = 0, vv = this.views, vvl = vv.length|0, l = 0, v = null;
    l = vv[0].viewLength|0; while (l <= index) { if (++vvi >= vvl) return {done: true, value: undefined}; index = (index - l)|0; l = vv[vvi].viewLength|0; }
    v = vv[vvi];
    return {done: false, value: v.array[((v.viewOffset|0) + (this.index++))|0]};
  };

  ArrayViews.EntriesIterator = EntriesIterator;
  ArrayViews.ValuesIterator = ValuesIterator;
  ArrayViews.toScript = function () { return "(" + script.toString() + "())"; };
  return ArrayViews;

}());
