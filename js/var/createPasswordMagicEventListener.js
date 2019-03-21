this.createPasswordMagicEventListener = (function script() {
  "use strict";

  /*! createPasswordMagicEventListener.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function createPasswordMagicEventListener(listener, options) {
    // Usage :
    //   var listener = createPasswordMagicEventListener(updateSpan);
    //   createPasswordMagicEventListener.addEventListenerTo(element, listener);
    //   [...]
    //   createPasswordMagicEventListener.removeEventListenerFrom(element, listener);

    // timer should not vary according to element ! Use different listeners for magic update if necessary.
    var timer = null, delay = 1000; //, onComputingListener = null;

    function callListener(listener, event) {
      // Following behavior of :
      //   func.handleEvent = func2;
      //   element.addEventListener("type", func);
      try {
        if (typeof listener === "function") return listener(event);
        else if (typeof listener.handleEvent === "function") return listener.handleEvent(event);
      } catch (e) {
        try { console.error(e); } catch (ignore) {}
      }
    }

    function abortTimerIfNecessary() {
      if (timer !== null) { clearTimeout(timer); timer = null; }
    }

    if (options) {
      if (options.abortPromise) options.abortPromise.then(abortTimerIfNecessary, abortTimerIfNecessary);
      if (options.delay !== undefined) delay = options.delay|0;
      //if (options.onComputingListener) onComputingListener = options.onComputingListener;
    }

    function doMagic(inputElement) {
      timer = null;
      if (inputElement.value === "") return callListener(listener, "");
      callListener(listener, createSha256SummaryBase64StringFromString(inputElement.value).slice(0, 3));
    }

    listener = listener || {};
    function newListener(event) {
      abortTimerIfNecessary();
      if (event.target.value === "") return callListener(listener, "");
      if (delay === 0) return doMagic(event.target);
      callListener(listener, "...");  //if (onComputingListener) callListener(onComputingListener, "...");
      timer = setTimeout(doMagic, delay, event.target);
    }
    return newListener;
  }
  createPasswordMagicEventListener.addEventListenerToInputElement = function (element, listener) {
    element.addEventListener("input", listener, {passive: true});
  };
  createPasswordMagicEventListener.removeEventListenerFromInputElement = function (element, listener) {
    element.removeEventListener("input", listener, {passive: true});
  };

  // Other Usage :
  //   var listener = createPromisedEventListener();
  //   var aborter = createPromiseDeffered();
  //   listener.wrapper = createPasswordMagicEventListener(listener, {abortPromise: aborter.promise, delay: 1000});
  //   createPasswordMagicEventListener.addEventListenerToInput(inputPassword, listener.wrapper);
  //   [...]
  //   while (true) {
  //     try {
  //       var magic = await listener.waitNextEvent();
  //     } finally {
  //       createPasswordMagicEventListener.removeEventListenerFromInput(element, listener.wrapper);
  //       aborter.resolve();
  //     }
  //     span.textContent = magic;  // updateSpan
  //   }

  createPasswordMagicEventListener.toScript = function () { return "(" + script.toString() + "())"; };
  createPasswordMagicEventListener._requiredGlobals = ["createSha256SummaryBase64StringFromString"];
  return createPasswordMagicEventListener;

}());
