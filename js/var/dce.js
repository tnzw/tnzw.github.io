this.dce = (function script() {
  "use strict";

  /*! dce.js Version 1.0.1

      Copyright (c) 2015-2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function dce(tagName, options, nodes) {
    // dce(tagName[, options[, nodes]]);
    // dce(tagName[, options[, innerHTML]]);

    // A `document.createElement` helper.

    // Simple example :
    //     dce("p", null, [
    //       "Please ", dce("a", {href: "#"}, ["Click here"]), " to surf."
    //     ]);

    // Example with listener :
    //     dce("input", {type: "password", placeholder: "Password", on: {input: updateHash}});
    //     dce("input", {type: "password", placeholder: "Password", on: {input: EventListener}});
    //     dce("input", {type: "password", placeholder: "Password", on: {input: {listener: EventListener, options: {capture: false}}}});

    // Examples using custom attributes :
    //     dce("div", {attributes: {"custom-attribute": "custom-value"}});
    //     dce("div", {}, "<span>innerHTML</span>");

    var e = document.createElement(tagName), a = null, i = 0;
    if (options) {
      for (a = Object.keys(options), i = 0; i < a.length; i += 1)
        if (a[i] !== "attributes" && a[i] !== "on")
          e[a[i]] = options[a[i]];
      if (options.on)
        for (a = Object.keys(options.on), i = 0; i < a.length; i += 1)
          if (typeof options.on[a[i]] === "function") e.addEventListener(a[i], options.on[a[i]], false);
          else e.addEventListener(a[i], options.on[a[i]].listener, options.on[a[i]].options || false);
      if (options.attributes)
        for (a = Object.keys(options.attributes), i = 0; i < a.length; i += 1)
          e.setAttributes(a[i], options.attributes[a[i]]);
    }
    if (typeof nodes === "string")
      e.innerHTML = nodes;
    else if (nodes)
      for (i = 0; i < nodes.length; i += 1)
        e.appendChild(typeof nodes[i] === "string" ? document.createTextNode(nodes[i]) : nodes[i]);
    return e;
  }
  dce.toScript = function () { return "(" + script.toString() + "())"; };
  return dce;

}());
