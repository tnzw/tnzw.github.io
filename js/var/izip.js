this.izip = (function script() {
  "use strict";

  /*! izip.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function izip(...iterables) {
    return (function* (zz) {
      var v, t, i;
      while (true) {
        t = [];
        for (i = 0; i < zz.length; i += 1) {
          v = next(zz[i]);
          if (v.done) return;
          t.push(v.value);
        }
        yield t;
      }
    })(iterables.map(_ => iter(_)));
  }
  izip.toScript = function () { return "(" + script.toString() + "())"; };
  izip._requiredGlobals = ["iter", "next"];
  return izip;

}());
