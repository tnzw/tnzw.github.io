this.promisedPromptFile = (function script() {
  "use strict";

  /*! promisedPromptFile.js Version 1.0.0

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function promisedPromptFile(message) {
    // /!\ Use with care !
    // This prompt captures the focus, if you have two prompts you may trigger infinite loop !
    var oncancel = null, promise = new Promise(function (resolve) {
      var layout = null, beam = null, windoww = null,
          p = null, div = null, input = null, cancel = null;//, ok = null;

      function onEscape(e) {
        if (e.key === "Esc" || e.key === "Escape" || e.keyIdentifier === "U+001B")
          onCancel();
      }
      function onChange() {
        //ok.disabled = input.value ? false : true;
        if (input.value) onOk();
      }
      function onBlur(e) {
        if (e.relatedTarget === input ||
            e.relatedTarget === cancel) return;
            //e.relatedTarget === ok) return;
        input.focus();
      }
      function onBodyFocus(e) {
        if (e.target === input ||
            e.target === cancel) return;
            //e.target === ok) return;
        input.focus();
      }
      function remove() {
        layout.remove();
        document.body.removeEventListener("keydown", onEscape, {capture: true, passive: true});
        document.body.removeEventListener("focus", onBodyFocus, {capture: true, passive: true});
      }
      function onCancel() {
        remove();
        resolve(null);
      }
      function onOk() {
        remove();
        resolve(input.files[0] || null);
      }

      layout = document.createElement("div");
      layout.style.position = "fixed";
      layout.style.width = "100%";
      layout.style.height = "100%";
      layout.style.left = "0em";
      layout.style.top = "0em";
      layout.style.backgroundColor = "rgba(0,0,0,0.5)";
      layout.style.margin = "0em";
      layout.style.padding = "0em";
      layout.style.zIndex = "9999";  // XXX
      layout.addEventListener("blur", onBlur, {capture: true, passive: true});

      beam = document.createElement("div");
      beam.style.position = "fixed";
      beam.style.width = "100%";
      beam.style.maxHeight = "100%";
      beam.style.left = "0em";
      beam.style.top = "0em";
      beam.style.textAlign = "center";
      beam.style.overflow = "auto";
      layout.appendChild(beam);

      windoww = document.createElement("div");
      windoww.style.backgroundColor = "white";
      windoww.style.color = "black";
      windoww.style.padding = "1em";
      windoww.style.margin = "auto";
      windoww.style.textAlign = "left";
      windoww.style.display = "inline-block";
      beam.appendChild(windoww);

      p = document.createElement("p");
      windoww.appendChild(p);

      input = document.createElement("input");
      input.type = "file";
      input.addEventListener("change", onChange, {passive: true});
      div = document.createElement("div");
      div.appendChild(input);
      windoww.appendChild(div);

      div = document.createElement("div");
      div.style.textAlign = "right";
      cancel = document.createElement("button");
      cancel.textContent = "Cancel";
      cancel.addEventListener("click", onCancel, {passive: true});
      div.appendChild(cancel);

      //ok = document.createElement("button");
      //ok.textContent = "OK";
      //ok.disabled = true;
      //ok.addEventListener("click", onOk, {passive: true});
      //div.appendChild(ok);
      windoww.appendChild(div);

      if (message !== undefined) {
        message = "" + message;
        p.innerHTML = message.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br/>");
      }

      document.body.addEventListener("keydown", onEscape, {capture: true, passive: true});
      document.body.addEventListener("focus", onBodyFocus, {capture: true, passive: true});
      if (document.body.firstChild !== null)
        document.body.insertBefore(layout, document.body.firstChild);
      else
        document.body.appendChild(layout);
      oncancel = onCancel;  // XXX should we throw something ?
      input.focus();
    });
    promise.cancel = oncancel;
    return promise;
  }
  promisedPromptFile.toScript = function () { return "(" + script.toString() + "())"; };
  return promisedPromptFile;

}());
