this.readBlob = (function script() {
  "use strict";

  /*! readBlob.js Version 1.2.0

      Copyright (c) 2015-2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function readBlob(blob, as) {
    //     readBlob(blob, "Text")
    // blob = new Blob([..])
    //   the blob to read
    // as = "Text"
    //   in which type to read the blob
    //   Choices : "Text", "ArrayBuffer", "DataURL"
    var d = {},
        fr = new FileReader();
    d.promise = new Promise(function (res, rej) { d.resolve = res; d.reject = rej; });
    fr.onload = function (e) { return d.resolve(e.target.result); };
    fr.onerror = fr.onabort = function (e) { return d.reject(e.target.error); };
    d.promise.cancel = function () { fr.abort(); };
    switch (as.toLowerCase()) {
      case "arraybuffer": fr.readAsArrayBuffer(blob); break;
      case "text":
      case "string":
      case undefined: fr.readAsText(blob); break;
      case "dataurl": fr.readAsDataURL(blob); break;
      case "binarystring": if (fr.readAsBinaryString) { fr.readAsBinaryString(blob); break; }
      default: throw new Error("unhandled `as = " + as + "`");
    }
    return d.promise;
  }
  readBlob.toScript = function () { return "(" + script.toString() + "())"; };
  return readBlob;

}());
