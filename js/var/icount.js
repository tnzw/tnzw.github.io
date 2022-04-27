this.icount = (function script() {
  "use strict";

  /*! icount.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function* icount(start, step) {
    var i = 0;
    if (start === undefined) start = 0;
    if (step === undefined) step = 1;
    while (true) yield start + (i++) * step;
  }
  icount.toScript = function () { return "(" + script.toString() + "())"; };
  return icount;

}());
