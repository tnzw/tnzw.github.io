this.importStyleSheetsAsync = (function lib() {
  "use strict";

  /*! importStyleSheetsAsync.js Version 0.1.1

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function importStyleSheetsAsync() {
    var i = 0, j = 0, hrefs = [], href = "",
        baseUrl = (document.currentScript ? document.currentScript.src : (location.origin + location.pathname)),
        link = null;

    for (; i < arguments.length; i += 1)
      hrefs.push("" + arguments[i]);

    for (i = 0; i < hrefs.length; i += 1) {
      link = document.createElement("link");
      link.rel = "stylesheet";
      href = hrefs[i];
      if (/^[^\/]+:/.test(href) || /^\//.test(href)) link.href = href;
      else link.href = baseUrl.replace(/[^\/]+$/, "") + href;
      href = link.href;

      // do not import libs twice
      // normaly, the browser loads the resource once, but may include/exec n times
      for (j = 0; j < document.styleSheets.length; j += 1)
        if (document.styleSheets[j].href === href) { href = ""; break; }
      if (href === "") continue;

      document.head.appendChild(link);
    }
  }
  importStyleSheetsAsync.toScript = function () { return "(" + lib.toString() + "())"; };
  return importStyleSheetsAsync;

}());
