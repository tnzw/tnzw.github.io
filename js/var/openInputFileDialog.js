this.openInputFileDialog = (function script() {
  "use script";

  /*! openInputFileDialog.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function openInputFileDialog(input) {
    // input element should have type=file
    // XXX Find a way to resolve with empty file list when user closes the dialog.
    //     This uses `cancel` method internaly to avoid calling it twice on the same element.
    var oncancel = function () {},
        promise = new Promise(function (resolve, reject) {
      oncancel = function () { reject(new Error("cancelled")); }
      if (input.type !== "file") return reject(new Error("not a file input element"));

      function listener(e) {
        resolve(e.target.files);
        e.target.removeEventListener("change", listener, {passive: true, once: true});
      }
      input.addEventListener("change", listener, {passive: true, once: true});
      input.value = null;
      input.click();
    });
    promise.cancel = oncancel;

    if (input.type === "file") {
      if (input._openInputFileDialog_promise)
        try { input._openInputFileDialog_promise.cancel(); } catch (_) {}
      input._openInputFileDialog_promise = promise;
    }
    return promise;
  }

  openInputFileDialog.toScript = function () { return "(" + script.toString() + "())"; };
  return openInputFileDialog;

}());
