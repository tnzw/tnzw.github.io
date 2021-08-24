this.divmod = (function script() {
  "use strict";

  /*! divmod.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function divmod(a, b) {
    var mod = a % b;
    return [(a - mod) / b, mod];
  }
  divmod.toScript = function () { return "(" + script.toString() + "())"; };
  return divmod;

}());
