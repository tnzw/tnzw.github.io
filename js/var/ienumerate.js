this.ienumerate = (function script() {
  "use strict";

  /*! ienumerate.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ienumerate(iterable, start) {
    if (start === undefined) start = 0;
    return imap(_ => [start++, _], iterable);
  }
  ienumerate.toScript = function () { return "(" + script.toString() + "())"; };
  ienumerate._requiredGlobals = ["imap"];
  return ienumerate;

}());
