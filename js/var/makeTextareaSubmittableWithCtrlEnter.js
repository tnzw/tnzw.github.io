this.makeTextareaSubmittableWithCtrlEnter = (function script() {
  "use strict";

  /*! makeTextareaSubmittableWithCtrlEnter.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function makeTextareaSubmittableWithCtrlEnter(textarea) {
    textarea.addEventListener("keydown", makeTextareaSubmittableWithCtrlEnter.listener, {passive: true});
  }
  makeTextareaSubmittableWithCtrlEnter.listener = {
    handleEvent: function (event) {
      if (event.ctrlKey &&
          event.key === "Enter" &&
          event.target.form !== null)
        event.target.form.submit();
    }
  };
  makeTextareaSubmittableWithCtrlEnter.toScript = function () { return "(" + script.toString() + "())"; };
  return makeTextareaSubmittableWithCtrlEnter;

}());
