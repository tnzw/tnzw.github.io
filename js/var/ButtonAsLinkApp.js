this.ButtonAsLinkApp = (function script() {
  "use strict";

  /*! ButtonAsLinkApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function ButtonAsLinkApp(params) {
    // params.textContent = ".."
    // params.href = ".."
    // params.target = ".."
    // XXX params.reflectHrefInTitle = true
    this._href = "";
    this._target = "";
    this._a = document.createElement("a");
    this.element = document.createElement("button");
    this.element.addEventListener("click", this, {passive: true});
    this.update(params);
  }
  ButtonAsLinkApp.prototype.element = null;
  ButtonAsLinkApp.prototype.listener = null;
  ButtonAsLinkApp.prototype._notify = function (event) {
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
  ButtonAsLinkApp.prototype.update = function (params) {
    if (params) {
      if (params.textContent !== undefined) this.element.textContent = params.textContent;
      if (params.href !== undefined) this.setHref(params.href);
      if (params.target !== undefined) this.setTarget(params.target);
    }
  };
  ButtonAsLinkApp.prototype.focus = function () {
    this.element.focus();
  };
  ButtonAsLinkApp.prototype.setTextContent = function (text) {
    this.element.textContent = text;
  };
  ButtonAsLinkApp.prototype.getHref = function () {
    return this._href;
  };
  ButtonAsLinkApp.prototype.setHref = function (href) {
    href += "";
    this._href = href;
    this._a.href = href;
    this.element.title = this._a.href;  // sometimes location can change ? use onmouseover to update title ?

    //if ((/^[a-z]:/i).test(href))
    //  this.element.title = href;
    //else if ((/^\/\//).test(href))
    //  this.element.title = location.protocol + href;
    //else if (href[0] === "/")
    //  this.element.title = location.origin + href;
    //else
    //  this.element.title = location.href.split("?")[0].split("#")[0].split("/").slice(0, -1).concat(href).join("/");
  };
  ButtonAsLinkApp.prototype.getTarget = function () {
    return this._target;
  };
  ButtonAsLinkApp.prototype.setTarget = function (target) {
    this._target = target + "";
  };
  ButtonAsLinkApp.prototype.runOpen = function () {
    this._a.target = this._target;
    this._a.click();
  };
  ButtonAsLinkApp.prototype.runOpenTargetBlank = function () {
    this._a.target = "_blank";
    this._a.click();
  };
  ButtonAsLinkApp.prototype.handleEvent = function (event) {
    // event.type = "click"
    // event.target = this.element
    if (event.ctrlKey) this.runOpenTargetBlank();
    else this.runOpen();
  };

  ButtonAsLinkApp.toScript = function () { return "(" + script.toString() + "())"; };
  return ButtonAsLinkApp;

}());
