this.ButtonAsInputFileApp = (function script() {
  "use strict";

  /*! ButtonAsInputFileApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ButtonAsInputFileApp(params) {
    // params.textContent = ".."
    this._input = document.createElement("input");
    this.element = document.createElement("button");
    this._input.addEventListener("change", this, {passive: true});
    this.element.addEventListener("click", this, {passive: true});
    this.update(params);
  }
  ButtonAsInputFileApp.prototype.element = null;
  ButtonAsInputFileApp.prototype.listener = null;
  ButtonAsInputFileApp.prototype._notify = function (event) {
    try {
      if (typeof this.listener === "function")
        this.listener.call(this, event);
      else if (typeof this.listener === "object" &&
               this.listener !== null &&
               typeof this.listener.handleEvent === "function")
        this.listener.handleEvent(event);
    } catch (e) {
      if (event.type === "error") console.error(e);
      else this._notify({type: "error", message: e.message, error: e});  // XXX on next tick ?
    }
  };
  ButtonAsInputFileApp.prototype.update = function (params) {
    if (params) {
      if (params.textContent !== undefined) this.element.textContent = params.textContent;
    }
  };
  ButtonAsInputFileApp.prototype.focus = function () {
    this.element.focus();
  };
  ButtonAsInputFileApp.prototype.setTextContent = function (text) {
    this.element.textContent = text;
  };
  ButtonAsInputFileApp.prototype.runPrompt = function () {
    this._input.click();
  };
  ButtonAsInputFileApp.prototype.handleEvent = function (event) {
    if (event.target === this.element)
      // event.type = "click"
      this.runPrompt();
    else {  // event.target === this._input
      // event.type = "change"
      this._input.value = null;
      this.notify({type: "file", target: this, file: this._input.files[0]});
    }
  };

  ButtonAsInputFileApp.toScript = function () { return "(" + script.toString() + "())"; };
  return ButtonAsInputFileApp;

}());
