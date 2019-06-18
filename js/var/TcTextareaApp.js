this.TcTextareaApp = (function script() {
  "use strict";

  /*! TcTextareaApp.js Version 1.1.0

      Copyright (c) 2017-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function TcTextareaApp(params) {
    //     var app = new TcTextareaApp();
    //     document.body.appendChild(app.element);
    this.element = document.createElement("textarea");
    this.element.placeholder = [
      "Empty content",
      "                                TC Textarea App",
      "",
      "                                 version 1.1.0",
      "                              by Tristan Cavelier",
    ].join("\n");
    this.update(params);
  }
  TcTextareaApp.prototype.element = null;
  TcTextareaApp.prototype.update = function (params) {
    if (this.editor) throw new Error("not implemented");
    this.editor = TcTextarea.fromTextArea(this.element, params);
    if (params) {
      if (params.dataAsText !== undefined) this.setDataAsText(params.dataAsText);
      else if (params.value !== undefined) this.setDataAsText(params.value);
    }
  };
  TcTextareaApp.prototype.setDataAsText = function (data) { this.element.value = data; };
  TcTextareaApp.prototype.getDataAsText = function () { return this.element.value; };

  TcTextareaApp.toScript = function () { return "(" + script.toString() + "())"; };
  TcTextareaApp._requiredGlobals = ["TcTextarea"];
  return TcTextareaApp;

}());
