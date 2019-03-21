this.loadVarScripts = (function lib() {
  "use strict";

  /*! loadVarScripts.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function loadVarScripts() {
    // loadVarScripts({baseUrl: "../js/var/"}, "readBlob").then(...)
    function getLocationOrigin() {
      // on Firefox 57, file:///media/... as location.origin === "null"
      var origin = location.origin;
      if (typeof origin === "string" &&
          origin.indexOf("/") !== -1)
        return origin;
      if (location.protocol === "file:")
        return "file://";
      throw new Error("loadVarScripts: cannot get origin");
    }
    var defer = {}, i = 0, stmp = "", names = [],
        baseUrl = (document.currentScript && document.currentScript.src) || (getLocationOrigin() + location.pathname);
    //console.log(baseUrl);

    defer.promise = new Promise(function (a, b) { defer.resolve = a; defer.reject = b; });

    for (; i < arguments.length; i += 1) {
      if (typeof arguments[i] === "object" && arguments[i] !== null) {
        if (arguments[i].baseUrl !== undefined) {
          stmp = arguments[i].baseUrl + "";
          if (/^[^\/]+:/.test(stmp) || /^\//.test(stmp)) baseUrl = stmp;
          else baseUrl = baseUrl.replace(/[^\/]+$/, "") + stmp;
        }
      } else names.push("" + arguments[i]);
    }

    function loadScript(src) {
      var defer = {}, j = 0, script = null;
      defer.promise = new Promise(function (a, b) { defer.resolve = a; defer.reject = b; });
      script = document.createElement("script");
      script.async = false;
      if (/^[^\/]+:/.test(src) || /^\//.test(src)) script.src = src;
      else script.src = baseUrl.replace(/[^\/]+$/, "") + src;
      src = script.src;

      // do not import libs twice
      // normaly, the browser loads the resource once, but may include/exec n times
      // we CANNOT concider a script loaded if present in the dom even if `script.async = false`
      for (j = 0; j < document.scripts.length; j += 1)
        if (document.scripts[j].src === src) { src = ""; break; }
      if (src === "") {
        //console.log(document.scripts[j], document.scripts[j].loadPromise);
        if (document.scripts[j].loadPromise)
          //document.scripts[j].loadPromise.then(defer.resolve, defer.reject);
          return document.scripts[j].loadPromise;
        defer.resolve();
        return defer.promise;
      }  /**/

      script.addEventListener("load", function () { defer.resolve(); });
      script.addEventListener("error", function (e) { var er = new Error(e.message); er.event = e; defer.reject(er); });
      script.loadPromise = defer.promise;
      document.head.appendChild(script);
      return defer.promise;
    }

    function rec() {
      var name = "";
      do {
        if (names.length === 0) { defer.resolve(); return; }
        name = names.shift() + "";
      } while (!(/^[a-z_\$][a-z0-9_\$]*$/i).test(name));
      (eval.call(null, "typeof " + name + ' === "undefined"') ? loadScript(name + ".js") : Promise.resolve()).then(function () {
        var v = eval.call(null, name);
        if (typeof v === "function" &&
            Array.isArray(v._requiredGlobals))
          names.push.apply(names, v._requiredGlobals);
        rec();
      }, defer.reject);
    }
    rec();
    return defer.promise;
  }
  loadVarScripts.toScript = function () { return "(" + lib.toString() + "())"; };
  return loadVarScripts;

}());
