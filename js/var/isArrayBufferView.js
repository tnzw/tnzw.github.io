this.isArrayBufferView = (function script() {
  "use strict";

  /*! isArrayBufferView.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function isArrayBufferView(value) {
    return ArrayBuffer.isView(value);
  }

  isArrayBufferView.toScript = function () { return "(" + script.toString() + "())"; };
  return isArrayBufferView;

}());
