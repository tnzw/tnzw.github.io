this.icycle = (function script() {
  "use strict";

  /*! icycle.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function icycle(iterable) {
    return (function* (it) {
      var l = [], o = next(it);
      while (!o.done) { l.push(o.value); yield o.value; o = next(it) }
      while (true) yield* l;
    })(iter(iterable));
  }
  icycle.toScript = function () { return "(" + script.toString() + "())"; };
  icycle._requiredGlobals = ["iter", "inext"];
  return icycle;

}());
