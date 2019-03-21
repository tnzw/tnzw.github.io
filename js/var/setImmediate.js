this.setImmediate = (function script() {
  "use strict";

  /*! setImmediate.js Version 1.0.3

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function setImmediate(fn) {
    var l = arguments.length - 1, i = 0, args = new Array(l);
    while (i < l) { args[i] = arguments[++i]; }
    Promise.resolve().then(fn.apply.bind(fn, null, args));
  }
  setImmediate.toScript = function () { return "(" + script.toString() + "())"; };
  return setImmediate;

}());
