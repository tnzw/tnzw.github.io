this.CodeMirrorApp = (function script() {
  "use strict";

  /*! CodeMirrorApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

    function CodeMirrorApp(params) {
      //     var app = new CodeMirrorApp();
      //     document.body.appendChild(app.element);

      this.element = document.createElement("div");
      this.textarea = document.createElement("textarea");
      this.textarea.style = "display: none;";
      this.element.appendChild(this.textarea);
      this.update(params);
    }
    CodeMirrorApp.prototype.element = null;
    CodeMirrorApp.prototype.update = function (params) {
      if (this.editor) throw new Error("not implemented");
      this.editor = CodeMirror.fromTextArea(this.textarea, params);
      if (params) {
        if (params.dataAsText !== undefined) this.setDataAsText(params.dataAsText);
        else if (params.value !== undefined) this.setDataAsText(params.value);
      }
    };
    CodeMirrorApp.prototype.focus = function () {
      this.editor.focus();
    };
    CodeMirrorApp.prototype.setDataAsText = function (text) { this.editor.setValue(text); };
    CodeMirrorApp.prototype.getDataAsText = function () { return this.editor.getValue(); };
    CodeMirrorApp.prototype.getCodeMirrorEditor = function () { return this.editor; };

    CodeMirrorApp.toScript = function () { return script.toString(); };
    return CodeMirrorApp;

}());
