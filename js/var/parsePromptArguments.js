this.parsePromptArguments = (function script() {
  "use strict";

  /*! parsePromptArguments.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function parsePromptArguments(string) {
    // nearly shell like arguments
    var args = [], expectedindex = -1 >>> 1;
    string.replace(/(?:"((?:\\.|[^\\"])*)"|'([^']*)'|([^\\"' \t]+)|(\\.)|([\\"']))/g, function (m, dq, sq, r, bs, q, i) {
      var s = "";
      if (args.length === 0) args.push("");
      if (dq !== undefined) s = dq.replace(/\\"/g, '"');
      else if (sq !== undefined) s = sq;
      else if (r !== undefined) s = r;
      else if (bs !== undefined) s = bs.slice(1, 2);
      else if (q !== undefined) s = q;

      if (i <= expectedindex) args[args.length - 1] += s;
      else args.push(s);
      expectedindex = i + m.length;
    });
    return args;
  }

  parsePromptArguments.toScript = function () { return "(" + script.toString() + "())"; };
  return parsePromptArguments;

}());
