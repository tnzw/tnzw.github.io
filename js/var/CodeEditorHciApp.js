this.CodeEditorHciApp = (function script() {
  "use strict";

  /*! CodeEditorHciApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

    function CodeEditorHciApp(params) {  // XXX rename to TcCodeMirrorFileEditorHciApp ?
      // [:] Open: [choose file]____ - CodeEditor  [x]
      var ths = this;
      this.element = document.createElement("div");
      this.element.style.display = "inline-block";
      this.menuDownloadButton = document.createElement("button");
      this.menuDownloadButton.textContent = "Download";
      this.menuDownloadButton.style.width = "100%";
      this.menuCloseButton = document.createElement("button");
      this.menuCloseButton.textContent = "Close";
      this.menuCloseButton.style.width = "100%";
      this.menuApp = new MenuApp({
        text: ":",
        elements: [
          this.menuDownloadButton,
          document.createElement("br"),
          this.menuCloseButton
        ],
        listener: this
      });
      this.menuApp.menuDiv.style.zIndex = 10;  // to bypass code mirror
      this.titleTextNode = document.createTextNode("CodeEditor");
      this.closeButton = document.createElement("button");
      this.closeButton.style.minWidth = "1em";
      this.closeButton.textContent = "x";
      this.codemirrorApp = new CodeMirrorApp({
        autoRefresh: true,  // default false (autorefresh)
        keyMap: "tc",  // default "default"
        lineNumbers: true,  // default false
        extraKeys: {
          "Alt-Esc": function () { ths.menuApp.focus(); },
          "F3": "findNext",
          "Shift-F3": "findPrev"
        }
      });

      this.codemirrorApp.element.style.border = "1px solid rgba(0,0,0,0.3)";

      this.menuDownloadButton.addEventListener("click", this, {passive: true});
      this.menuCloseButton.addEventListener("click", this, {passive: true});
      this.closeButton.addEventListener("click", this, {passive: true});

      this.element.appendChild(this.closeButton);
      this.element.appendChild(document.createTextNode(" "));
      this.element.appendChild(this.menuApp.element);
      this.element.appendChild(document.createTextNode(" "));
      this.element.appendChild(this.titleTextNode);
      this.element.appendChild(document.createElement("br"));
      this.element.appendChild(this.codemirrorApp.element);

      this.update(params);
    }
    CodeEditorHciApp.prototype.element = null;
    CodeEditorHciApp.prototype.listener = null;
    CodeEditorHciApp.prototype.update = function (params) {
      var i = 0, a = null;
      if (params) {
        if (params.file !== undefined) this.loadFile(params.file);
      }
    };
    CodeEditorHciApp.prototype._notify = function (event) {
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
    CodeEditorHciApp.prototype.focus = function () {
      this.codemirrorApp.focus();
    };
    CodeEditorHciApp.prototype.runPromptOpenFile = function () {
      // XXX
    };
    CodeEditorHciApp.prototype.runMenuOpenFile = function () {
      // XXX
    };
    CodeEditorHciApp.prototype.runClose = function () {
      if (!confirm("Ok to close ?")) return;
      this.codemirrorApp.setDataAsText("");
      this._notify({type: "close", target: this});
    };
    CodeEditorHciApp.prototype.runDownload = function () {
      var a = document.createElement("a");
      a.href = "data:text/plain," + encodeURI(this.codemirrorApp.getDataAsText());
      a.download = "untitled.txt";
      a.style.display = "none";
      setTimeout(function () { document.body.removeChild(a); });
      document.body.appendChild(a);
      a.click();
      this._notify({type: "download", target: this});
    };
    CodeEditorHciApp.prototype.runAwareOfChanges = function () {
      // XXX
    };
    CodeEditorHciApp.prototype.runReduce = function () {
      // XXX
    };
    CodeEditorHciApp.prototype.runMaximize = function () {
      // XXX
    };
    CodeEditorHciApp.prototype.handleEvent = function (event) {
      //console.log(event);
      switch (event.type) {
        case "error":
          this._notify(event);
          break;
        case "click":
          if (event.target === this.menuDownloadButton) { this.runDownload(); event.target.blur(); }
          else if (event.target === this.menuCloseButton) { this.runClose(); event.target.blur(); }
          else if (event.target === this.closeButton) this.runClose();
          break;
      }
    };
    //CodeEditorHciApp._then = function (executor) {
    //  if (typeof executor === "function") try { return Promise.resolve(executor()); } catch (e) { return Promise.reject(e); }
    //  return Promise.resolve();
    //};

    CodeEditorHciApp.toScript = function () { return script.toString(); };
    CodeEditorHciApp._requiredGlobals = [
      "MenuApp",
      "CodeMirrorApp"
    ];
    return CodeEditorHciApp;

}());
