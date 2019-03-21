this.Array_prototype_set = (function script() {
  "use strict";

  /*! Array_prototype_set.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function Array_prototype_set(array, offset) {
    // Array_prototype_set.call(thisArg, array, offset)
    // Array.prototype.set = Array_prototype_set;
    // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/TypedArray/set
    var length = this.length|0, i = 0;
    offset = offset|0;
    if (offset < 0 || offset > length) throw new RangeError("invalid or out-of-range index");
    if (array.length > ((length - offset)|0)) throw new RangeError("invalid array length");
    // do not use array.values, if it's a sparse array it does not work.
    for (; offset < length && i < array.length; offset += 1, i += 1)
      this[offset] = array[i];
    return undefined;
  };
  Array_prototype_set.toScript = function () { return "(" + script.toString() + "())"; };
  return Array_prototype_set;

}());
