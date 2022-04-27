this.imap = (function script() {
  "use strict";

  /*! imap.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function imap(mapper, iterable, condition) {
    // Can do pythonic like list comprehension
    //   [i + 1 for i in iterable if i > 5]
    //   Array.from(imap(i => i + 1, iterable, i => i > 5))

    // imap() is not a generator because it should raise immediatly if iterable is not iterable
    if (condition)
      return (function* (it) {
        for (let _ of {[Symbol.iterator]: _ => it})
          if (condition(_))
            yield mapper(_);
      })(iter(iterable));
    return (function* (it) {
      for (let _ of {[Symbol.iterator]: _ => it})
        yield mapper(_);
    })(iter(iterable));
  }
  imap.toScript = function () { return "(" + script.toString() + "())"; };
  imap._requiredGlobals = ["iter"];
  return imap;

}());
