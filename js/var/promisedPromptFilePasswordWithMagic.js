this.promisedPromptFilePasswordWithMagic = (function script() {
  "use strict";

  /*! promisedPromptFilePasswordWithMagic.js Version 1.0.2

      Copyright (c) 2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function promisedPromptFilePasswordWithMagic(message, value) {
    // /!\ Use with care !
    // This prompt captures the focus, if you have two prompts you may trigger infinite loop !
    var oncancel = null, promise = new Promise(function (resolve) {
      var layout = null, beam = null, windoww = null,
          p = null, div = null, table = null, tbody = null, tr = null, td = null,
          input = null, inputp = null, magic = null, cancel = null, ok = null,
          magictimer = null;

      function onEscape(e) {
        if (e.key === "Esc" || e.key === "Escape" || e.keyIdentifier === "U+001B")
          onCancel();
      }
      function onEnter(e, prevent) {
        if (e.key === "Enter" || e.keyIdentifier === "Enter") {
          e.preventDefault();
          onOk();
        }
      }
      function onEnterPreventDefault(e) {
        onEnter(e, true);
      }
      function onInput(e) {
        clearTimeout(magictimer);
        if (inputp.value) {
          magic.textContent = "...";
          magictimer = setTimeout(function () {
            magic.textContent = sumBytesToSha256Base64(encodeStringToUtf8(inputp.value)).slice(0, 3);
          }, 1000);
        } else
          magic.textContent = "";
      }
      function onBlur(e) {
        if (e.relatedTarget === input ||
            e.relatedTarget === inputp ||
            e.relatedTarget === cancel ||
            e.relatedTarget === ok) return;
        input.focus();
      }
      function onBodyFocus(e) {
        if (e.target === input ||
            e.target === inputp ||
            e.target === cancel ||
            e.target === ok) return;
        input.focus();
      }
      function remove() {
        input.disabled = true;  // prevent showing upload dialog when pressing enter on the password input
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
        resolve([input.files[0], inputp.value]);
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

      table = document.createElement("table");
      tbody = document.createElement("tbody");
      table.appendChild(tbody);
      tr = document.createElement("tr");
      tbody.appendChild(tr);

      input = document.createElement("input");
      input.type = "file";
      td = document.createElement("td");
      td.style.textAlign = "right";
      td.textContent = "File";
      tr.appendChild(td);
      td = document.createElement("td");
      td.appendChild(input);
      tr.appendChild(td);

      tr = document.createElement("tr");
      tbody.appendChild(tr);

      inputp = document.createElement("input");
      inputp.style.width = "100%";
      inputp.type = "password";
      inputp.addEventListener("keydown", onEnterPreventDefault, {passive: false});
      inputp.addEventListener("input", onInput, {passive: true});
      td = document.createElement("td");
      td.style.textAlign = "right";
      td.textContent = "Password";
      tr.appendChild(td);
      td = document.createElement("td");
      td.appendChild(inputp);
      tr.appendChild(td)
      windoww.appendChild(table);

      div = document.createElement("div");
      div.style.textAlign = "right";
      magic = document.createElement("span");
      magic.style.fontFamily = "monospace";
      div.appendChild(magic);
      cancel = document.createElement("button");
      cancel.textContent = "Cancel";
      cancel.addEventListener("click", onCancel, {passive: true});
      div.appendChild(cancel);

      ok = document.createElement("button");
      ok.textContent = "OK";
      ok.addEventListener("click", onOk, {passive: true});
      div.appendChild(ok);
      windoww.appendChild(div);

      if (message !== undefined) {
        message = "" + message;
        p.innerHTML = message.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\n/g, "<br/>");
      }
      if (value !== undefined)
        input.value = value;

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
  promisedPromptFilePasswordWithMagic.toScript = function () { return "(" + script.toString() + "())"; };
  promisedPromptFilePasswordWithMagic._requiredGlobals = [
    "encodeStringToUtf8",
    "sumBytesToSha256Base64",
  ];
  return promisedPromptFilePasswordWithMagic;

}());
