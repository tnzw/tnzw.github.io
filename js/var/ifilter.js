this.ifilter = (function script() {
  "use strict";

  /*! ifilter.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ifilter(condition, iterable) { return imap(_ => _, iterable, condition) }
  ifilter.toScript = function () { return "(" + script.toString() + "())"; };
  ifilter._requiredGlobals = ["imap"];
  return ifilter;

}());
