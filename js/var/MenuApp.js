(function (global) {
  "use strict";

  /*! MenuApp.js Version 1.0.1

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  global.MenuApp = (function script() {

    function MenuApp(params) {
      // params.text = ".."
      //   the menu button text
      // params.elements = [..]
      //   the DOM elements to append to the menu
      // params.autoFocusElement = ..
      //   the DOM element that should call focus() after opening the menu
      //   should also be on the params.elements list

      this.element = document.createElement("div");
      this.element.style.display = "inline-block";
      this.menuButton = document.createElement("button");
      this.menuButton.textContent = "Menu";
      this.menuButton.addEventListener("click", this, false);
      this.menuDiv = document.createElement("div");
      this.menuDiv.style.position = "absolute";
      this.menuDiv.style.display = "none";
      this.menuDiv.addEventListener("focus", this, {capture: true, passive: true});
      this.menuDiv.addEventListener("blur", this, {capture: true, passive: true});
      //this.menuDiv.addEventListener("keydown", this, {capture: true, passive: true});
      this.element.appendChild(this.menuButton);
      this.element.appendChild(document.createElement("br"));
      this.element.appendChild(this.menuDiv);
      this.update(params);
    }
    //inherits(MenuApp, EventManager);
    MenuApp.prototype.element = null;
    MenuApp.prototype.listener = null;
    MenuApp.prototype.update = function (params) {
      var i = 0, a = null;
      if (params) {
        if (params.text !== undefined) this.menuButton.textContent = params.text;
        if (a = params.elements) { this.menuDiv.innerHTML = ""; for (; i < a.length; i += 1) this.menuDiv.appendChild(a[i]); }
        if (params.autoFocusElement !== undefined) this.autoFocusElement = params.autoFocusElement;
        if (params.listener !== undefined) this.listener = params.listener;
      }
    };
    MenuApp.prototype._notify = function (event) {
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
    MenuApp.prototype.focus = function () {
      this.menuButton.focus();
    };
    MenuApp.prototype.runMenuToggleAction = function () {
      if (this.menuDiv.style.display !== "none")
        this.runCloseMenuAction();
      else
        this.runOpenMenuAction();
    };
    MenuApp.prototype.runCloseMenuAction = function () {
      if (this.menuDiv.style.display !== "none") {
        this.menuDiv.style.display = "none";
        this._notify({type: "close", target: this});
      }
    };
    MenuApp.prototype.runOpenMenuAction = function () {
      if (this.menuDiv.style.display === "none") {
        this.menuDiv.style.display = "inline-block";
        if (this.autoFocusElement) this.autoFocusElement.focus();  // XXX protect from elements that are not in menuDiv successors ?
        else this.tryFocusMenu();
        this._notify({type: "open", target: this});
      }
    };
    MenuApp.prototype.tryFocusMenu = function () {
      var elements = this.menuDiv.querySelectorAll("*"),
          i = 0;
      for (; i < elements.length; i += 1)
        if (elements[i].tabIndex >= 0) {
          elements[i].focus();
          return true;
        }
      return false;
    };
    MenuApp.prototype.handleEvent = function (event) {
      var name = "", ths = this, fn = null;
      //console.log(event);
      if (event.target === this.menuButton) {
        if (event.type === "click")
          this.runMenuToggleAction();
      } else {
        // keydown, focus & blur listening from menuDiv
        if (event.type === "focus") {
          //this.menuDivFocused = true;
        } else if (event.type === "blur") {
          if (MenuApp._hasNodeAnscestor(event.relatedTarget, this.menuDiv)) {}  // XXX add depth to hasNodeAnscestor
          else {
            //this.menuDivFocused = false;
            if (event.relatedTarget === this.menuButton)
              setTimeout(function (ths) { ths.runCloseMenuAction(); }, 50, this);
            else
              this.runCloseMenuAction();
          }
        }/* else if (event.type === "keydown") {
          if (event.key === "Escape")
            this.menuButton.focus();
        }*/
      }
    };
    MenuApp.makeButtonListMenu = function (descriptions) {
      // descriptions = [{textContent: "Open", listener: onClick}, ...]
      var di = 0, div = document.createElement("div"), button = null;
      for (; di < descriptions.length; di += 1) {
        button = document.createElement("button");
        button.style.width = "100%";
        button.textContent = descriptions[di].textContent || "?";
        button.addEventListener("click", descriptions[di].listener, false);
        div.appendChild(button);
        div.appendChild(document.createElement("br"));
      }
      return div;
    };
    MenuApp._hasNodeAnscestor = function (node, anscestor) {
      if (node) while (node = node.parentNode) if (node === anscestor) return true;
      return false;
    };
    //MenuApp._then = function (executor) {
    //  if (typeof executor === "function") try { return Promise.resolve(executor()); } catch (e) { return Promise.reject(e); }
    //  return Promise.resolve();
    //};

    MenuApp.toScript = function () { return script.toString(); };
    return MenuApp;
  }());

}(this));
