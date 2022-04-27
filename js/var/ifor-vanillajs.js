this.ifor = (function script() {
  "use strict";

  /*! ifor-vanillajs.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ifor(iterable, callback) {
    return inext(iter(iterable), callback);
  }
  ifor.toScript = function () { return "(" + script.toString() + "())"; };
  ifor._requiredGlobals = ["iter", "inext"];
  return ifor;

}());
