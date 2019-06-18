this.isTypedArray = (function script() {
  "use strict";

  /*! isTypedArray.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function isTypedArray(value) {
    if (value === undefined || value === null)
      return false;
    var p = Object.getPrototypeOf(value)
    return
      p === Uint8Array.prototype ||
      p === Int8Array.prototype ||
      p === Uint16Array.prototype ||
      p === Int16Array.prototype ||
      p === Uint32Array.prototype ||
      p === Int32Array.prototype ||
      p === Uint8ClampedArray.prototype ||
      p === Float32Array.prototype ||
      p === Float64Array.prototype;
  }
  /*
    // Node.js way
    // see https://github.com/nodejs/node/blob/afad3b443e5aa90a771031ea9045182d1ecbf11a/deps/v8/test/mjsunit/compiler/typedarray-prototype-tostringtag.js#L18
    return Object.getOwnPropertyDescriptor(
      Object.getPrototypeOf(Uint8Array.prototype),
      Symbol.toStringTag).get.call(value) !== undefined;
  */

  isTypedArray.toScript = function () { return "(" + script.toString() + "())"; };
  return isTypedArray;

}());
