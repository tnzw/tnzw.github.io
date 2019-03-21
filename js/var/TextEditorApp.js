this.TextEditorApp = (function script() {
  "use strict";

  /*! TextEditorApp.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function TextEditorApp(options) {
    this.fileName = options && options.fileName;
    var data = options && options.data, ths = this;
    this.element = dce("div", null, [
      this.textarea = dce("textarea", {placeholder: "empty"})
    ]);
    if (data !== undefined) {
      if (data instanceof Blob) {
        this.textarea.readOnly = true;
        this.textarea.placeholder = "Loading...";
        readBlob(data, "Text").then(function (text) {
          ths.textarea.readOnly = false;
          ths.textarea.placeholder = "empty";
          ths.textarea.value = text;
        });
      } else {
        this.textarea.value = data;
      }
    }
  }
  TextEditorApp.prototype.element = null;
  TextEditorApp.prototype.getFileName = function () { return this.fileName; };
  TextEditorApp.prototype.getContentAsText = function () { return this.textarea.value; };

  TextEditorApp.toScript = function () { return "(" + script.toString() + "())"; };
  TextEditorApp._requiredGlobals = [
    "dce",
    "readBlob"
  ];

  return TextEditorApp;
}());
