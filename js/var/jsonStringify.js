this.jsonStringify = (function script() {
  "use strict";

  /*! jsonStringify.js Version 1.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function jsonStringify(value, replacer, space) {
    var replacerIsFunction = false,
        replacerDict = null,
        hasSpace = false,
        separator = "",
        newLine = "",
        di = 0;
    if (typeof replacer === "function") replacerIsFunction = true;
    else if (Array.isArray(replacer)) {
      replacerDict = {};
      while (di < replacer.length) { replacerDict[replacer[di++]] = true; }
    }
    function undefinable(value, typeofs) {
      if (value === undefined) return true;
      var i = 0;
      while (i < typeofs.length)
        if (typeof value === typeofs[i++])
          return true;
      return false;
    }
    function nullable(value) {
      return (value === null) ||
             (typeof value === "function") ||
             (typeof value === "symbol") ||
             (typeof value === "number" && isNaN(value));
    }
    function notEntryable(value) {
      return (typeof value === "function") ||
             (typeof value === "symbol");
    }
    function rec(key, value, prefixIndentation, indentation, undefinableTypeofs) {
      var s = null, i = 0, k = "", fullIndentation = prefixIndentation + indentation, tmp;
      if (replacerIsFunction === true) { value = replacer(key, value/*, SymbolIterator XXX*/); }
      if (undefinable(value, undefinableTypeofs)) { return undefined; }
      if (nullable(value)) { return "null"; }
      if (typeof value.toJSON === "function") {
        value = value.toJSON();
        if (undefinable(value, undefinableTypeofs)) { return undefined; }
        if (nullable(value)) { return "null"; }
      }
      if (Array.isArray(value)) {
        s = new Array(value.length);
        // XXX use replacerDict ?
        for (; i < value.length; i += 1)
          if ((tmp = rec("" + i, value[i], fullIndentation, indentation, [])) === undefined) s[i] = "null";
          else s[i] = tmp;
        return "[" + newLine + fullIndentation + s.join("," + newLine + fullIndentation) + newLine + prefixIndentation + "]";
      }
      if (typeof value === "object") {
        if (value.constructor === Number) return JSON.stringify(value/* + 0*/);
        else if (value.constructor === String) return JSON.stringify(value/* + ""*/);
        else if (value.constructor === Boolean) return JSON.stringify(value/* + 0 ? true : false*/);
        s = [];
        if (replacerDict !== null) {
          for (k in value)
            if (replacerDict[k] === true)
              if ((tmp = rec(k, value[k], fullIndentation, indentation, ["function", "symbol"])) !== undefined)
                s.push(JSON.stringify(k) + ":" + separator + tmp);
        } else {
          for (k in value)
            if ((tmp = rec(k, value[k], fullIndentation, indentation, ["function", "symbol"])) !== undefined)
              s.push(JSON.stringify(k) + ":" + separator + tmp);
        }
        return "{" + newLine + fullIndentation + s.join("," + newLine + fullIndentation) + newLine + prefixIndentation + "}";
      }
      // symbol
      // function
      // string
      // number (int, float, NaN, Infinity)
      // boolean
      // ...
      return JSON.stringify(value); 
    }
    if (typeof space === "string") {
      separator = " ";
      newLine = "\n";
    } else if (typeof space === "number" && isFinite(space)) {
      space = " ".repeat(space);
      separator = " ";
      newLine = "\n";
    } else {
      space = "";
    }
    return rec("", value, "", space, []);
  }
  jsonStringify.toScript = function () { return "(" + script.toString() + "())"; };
  return jsonStringify;

}());
