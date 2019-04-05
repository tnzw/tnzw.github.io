this.importScriptsAsync = (function lib() {
  "use strict";

  /*! importScriptsAsync.js Version 0.2.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function importScriptsAsync() {
    var i = 0, j = 0, srcs = [], src = "",
        count = 0, callback = null,
        baseUrl = (document.currentScript ? document.currentScript.src : (location.origin + location.pathname)),
        script = null;

    for (; i < arguments.length; i += 1) {
      if (typeof arguments[i] === "function") callback = arguments[i];
      else srcs.push("" + arguments[i]);
    }

    function trycallend() {
      if (callback === null) return;
      if (count === 0) {
        try { callback(); } catch (e) { console.error(e); }
      }
    }

    for (i = 0; i < srcs.length; i += 1) {
      script = document.createElement("script");
      script.async = false;
      src = srcs[i];
      if (/^[^\/]+:/.test(src) || /^\//.test(src)) script.src = src;
      else script.src = baseUrl.replace(/[^\/]+$/, "") + src;
      src = script.src;

      // do not import libs twice
      // normaly, the browser loads the resource once, but may include/exec n times
      for (j = 0; j < document.scripts.length; j += 1)
        if (document.scripts[j].src === src) { src = ""; break; }
      if (src === "") continue;

      count += 1;
      script.addEventListener("load", function () {
        count -= 1;
        trycallend();
      });
      script.addEventListener("error", function () {
        count -= 1;
        trycallend();
      });
      document.head.appendChild(script);
    }
    if (count === 0)
      if (typeof Promise === "function")
        new Promise(function (r) { r(); }).then(trycallend);
      else
        setTimeout(trycallend);
  }
  importScriptsAsync.toScript = function () { return "(" + lib.toString() + "())"; };
  return importScriptsAsync;

}());
