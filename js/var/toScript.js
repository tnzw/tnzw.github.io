this.toScript = (function script() {
  "use strict";

  /*! toScript.js Version 1.3.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function toScript(names, options) {
    // Usage:
    //   var script_to_eval = window.toScript(["toScript"], {useVar: true})
    //   var another_script = toScript.call(env, ["toScript"]);

    // Params:
    //   options
    //     allowToString  bool
    //       Allow to try to call `toString` on functions that have no `toScript` method.
    //     useVar  bool
    //       Use `var varname` instead of `this.varname`.

    // Example:
    //   evalOnWorker("(function () { " + script_to_eval + " }.call(environment_var));");
    //   [..]
    //   evalOnWorker("environment_var.toScript(['toScript']);");

    var global = this, handled = {}, destination = "this", allowToString = false, useVar = false;
    if (options) {
      if (options.allowToString) allowToString = true;
      if (options.useVar) useVar = true;
    }
    function asprop(name) {
      if ((/^[_a-z\$][_a-z0-9\$]*$/i).test(name))
        return "." + name;
      return "[" + JSON.stringify(name) + "]";
    }
    function asvar(name) {
      if ((/^[_a-z\$][_a-z0-9\$]*$/i).test(name))
        return name;
      throw new Error("cannot be a var name: " + name);
    }
    function rec(name) {
      var s = "";
      name += "";
      if (handled[name]) return "";
      handled[name] = true;
      if (global[name] === undefined) {
        return "";
      } else if (typeof global[name] === "function") {
        if (Array.isArray(global[name]._requiredGlobals))
          s = global[name]._requiredGlobals.map(rec).join(";\n") + ";\n";
        if (typeof global[name].toScript === "function")
          return s + (useVar ? "var " + name : "this" + asprop(name)) + " = " + global[name].toScript();
        if (allowToString)
          return s + (useVar ? "var " + name : "this" + asprop(name)) + " = " + global[name].toString();
        return "";
      } else {
        throw new Error("unhandled type `" + (typeof global[name]) + "`");
      }
      throw new Error("not implemented");
    }
    return names.map(rec).join(";\n") + ";";
  }
  toScript.toScript = function () { return "(" + script.toString() + "())"; };
  return toScript;

}());
