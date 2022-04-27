this.inext = (function script() {
  "use strict";

  /*! inext.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function inext(iterator, callback) {
    for (let _ of {[Symbol.iterator]: _ => iterator}) callback(_);
  }
  inext.toScript = function () { return "(" + script.toString() + "())"; };
  return inext;

}());
