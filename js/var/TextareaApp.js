this.TextareaApp = (function script() {
  "use strict";

  /*! TextareaApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // This is like an HelloWorldApp

  function TextareaApp(params) {
    //     var app = new TextareaApp();
    //     document.body.appendChild(app.element);

    this.element = document.createElement("textarea");
    this.element.setAttribute("style", [
      // SHOULD be defined by parent app
      "margin: 0;",
      "display: inline-block;",

      // COULD be defined by parent app
      "background-color: rgba(255,255,255,0);",
      //"border: none;",
      "box-sizing: border-box;",
      "height: 100%;", "width: 100%;",
      "resize: none;",

      // MUST NOT be defined by parent app
      "padding: 0.25em;",
    ].join(""));
    this.update(params);
  }
  TextareaApp.prototype.element = null;
  TextareaApp.prototype.update = function (params) {
    if (params) {
      // params should reflect the getters and setters
      if (params.dataAsText !== undefined) this.setDataAsText(params.dataAsText);
    }
  };
  TextareaApp.prototype.setDataAsText = function (data) { this.element.value = data; };
  TextareaApp.prototype.getDataAsText = function () { return this.element.value; };

  TextareaApp.toScript = function () { return "(" + script.toString() + "())"; };
  return TextareaApp;

}());
