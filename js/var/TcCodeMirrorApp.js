this.TcCodeMirrorApp = (function script() {
  "use strict";

  /*! TcCodeMirrorApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

    function TcCodeMirrorApp(params) {
      // Requires
      // "/third/codemirror-5.29.0/lib/codemirror.js",
      // "/js/lib/tc-codemirror-keymap.js",

      if (params) params = Object.create(params);
      else params = {};
      if (params.lineNumbers === undefined) params.lineNumbers = true;
      if (params.keyMap === undefined) params.keyMap = "tc";

      //CodeMirrorApp.call(this, params);
      this.sub = new CodeMirrorApp(params);
      this.element = this.sub.element;
    }
    //TcCodeMirrorApp.prototype = Object.create(CodeMirrorApp.prototype);
    //TcCodeMirrorApp.prototype.constructor = TcCodeMirrorApp;
    TcCodeMirrorApp.prototype.getDataAsText = function () { return this.sub.getDataAsText.apply(this.sub, arguments); };
    TcCodeMirrorApp.prototype.setDataAsText = function () { return this.sub.setDataAsText.apply(this.sub, arguments); };

    TcCodeMirrorApp.toScript = function () { return "(" + script.toString() + "())"; };
    TcCodeMirrorApp._requiredGlobals = ["CodeMirrorApp"];
    return TcCodeMirrorApp;

}());
