this.openNewTab = (function script() {
  "use strict";

  /*! openNewTab.js Version 1.0.0

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function openNewTab(href) {
    var a = document.createElement("a");
    a.setAttribute("target", "_blank");
    a.setAttribute("style", "display:none");
    a.href = href === undefined ? "about:blank" : href;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { a.parentNode.removeChild(a); });
  }
  openNewTab.toScript = function () { return "(" + script.toString() + "())"; };
  return openNewTab;

}());
