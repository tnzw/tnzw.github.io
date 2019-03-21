this.TcTextareaApp = (function script() {
  "use strict";

  /*! TcTextareaApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function TcTextareaApp(params) {
    //     var app = new TcTextareaApp();
    //     document.body.appendChild(app.element);
    // requires
    // /js/lib/tc-textarea-keymap.js
    var style = [
      "box-sizing: border-box;",
    ].join("\n"), placeholder = [
      "Empty content",
      "                                  TC Textarea",
      "",
      "                                 version 1.0.0",
      "                              by Tristan Cavelier",
      "",
      "                       press Alt-; to prompt for commands",
      "                       press Alt-R to repeat command action",
      "",
      "                             No other help so far."
    ].join("\n");

    this.element = document.createElement("textarea");
    this.element.style = style;
    this.element.placeholder = placeholder;
    try { assignTcKeyboardShortcutsToTextarea(this.element); } catch (e) { console.warn(e); }
    this.update(params);
  }
  TcTextareaApp.prototype.element = null;
  TcTextareaApp.prototype.update = function (params) {
    if (params) {
      if (params.dataAsText !== undefined) this.setDataAsText(params.dataAsText);
    }
  };
  TcTextareaApp.prototype.setDataAsText = function (data) { this.element.value = data; };
  TcTextareaApp.prototype.getDataAsText = function () { return this.element.value; };
  TcTextareaApp.toScript = function () { return "(" + script.toString() + "())"; };
  //TcTextareaApp._requiredGlobals = ["assignTcKeyboardShortcutsToTextarea"];  // XXX

  return TcTextareaApp;
}());
