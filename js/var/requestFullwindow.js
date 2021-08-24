this.requestFullwindow = (function script() {
  "use strict";

  /*! requestFullwindow.js Version 1.0.1

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function requestFullwindow(element, options) {
    // requestFullwindow(element, options)
    //
    // Requests to make the desired element be displayed in full window mode.
    // ie full window width and height. It uses two classes that should be
    // defined in css file or a style element.
    //
    // Just do element.classList.remove("fullwindow") to quit full window mode.
    //
    // element: An HTMLElement
    // options
    //   async: true/null/undefined (default)
    //            => requestFullwindow returns a promise that is fulfilled when
    //               the element is on fullwindow.
    //          false => use requestFullwindow synchronously.
    //          "untilfullwindowchange"
    //            => promise resolves when fullwindow is turned off.
    //   signal: used to abort the fullwindow only if async ===
    //           "untilfullwindowchange".
    //
    // css (see requestFullwindow.css):
    //   body.fullwindow-body { overflow: hidden; }
    //   .fullwindow { z-index: 9999; box-sizing: border-box; margin: 0; position: fixed; top: 0; left: 0; bottom: 0; right: 0; overflow: auto; }

    function mkAbortError(m){var e=new DOMException(m,"AbortError");e.code=DOMException.ABORT_ERR;return e}

    var signal, async;
    if (options) { signal = options.signal; async = options.async }
    var resolve, reject, promise;
    if (async === "untilfullwindowchange") { promise = new Promise(function (r, j) { resolve = r; reject = j }) }
    else if (async === undefined || async === null || async) {
      return new Promise(function (r) {
        requestFullwindow(element, {signal: signal, async: false});
        r();
      });
    }

    function onAbort(e) {
      element.classList.remove("fullwindow");
      signal.removeEventListener("abort", onAbort, {passive: true, once: true});
    }
    function onFocus(e) {
      var el = e.target
      if (el === window) return;
      if (el === document.body) { el.blur(); return; }
      //while (el) {
      while (el && el.classList) {
        //if (el === element) return;
        if (el.classList.contains("fullwindow")) return;  // in case where several element has fullwindow…
        el = el.parentElement;
      }
      element.focus();
      if (element !== document.activeElement) {
        try { el = element.querySelectorAll('*') } catch (_) { el = [] }
        for (e of el) {
          e.focus();
          if (e === document.activeElement) break;
        }
      }
    }
    function onEscape(e) {
      if (e.key === "Esc" || e.key === "Escape" || e.keyIdentifier === "U+001B") {
        element.classList.remove("fullwindow");
        e.preventDefault();
        e.stopPropagation();
      }
    }

    if (signal) {
      if (signal.aborted) throw new mkAbortError("already aborted signal");
      if (async === "untilfullwindowchange") signal.addEventListener("abort", onAbort, {passive: true, once: true});
      else signal = undefined;
    }

    if (document.querySelector(".fullwindow") || !element.parentElement)
      throw new TypeError("Fullwindow request denied");

    var observer = new MutationObserver(function (mutations) {
      function reversed(iterable) { var n = Array.from(iterable); n.reverse(); return n }
      for (let mutation of reversed(mutations)) {
        if (mutation.type === "attributes" && mutation.attributeName !== "class") continue;
        if (mutation.target.classList.contains("fullwindow")) {
          for (let e of document.body.querySelectorAll(".fullwindow"))
            if (e !== mutation.target) e.classList.remove("fullwindow");
          break;
        }
      }
      if (document.body.querySelectorAll(".fullwindow").length === 0 &&
          document.body.classList.contains("fullwindow-body"))
        document.body.classList.remove("fullwindow-body");
      if (!element.classList.contains("fullwindow") || !element.parentElement) {
        window.removeEventListener("focus", onFocus, {capture: true, passive: true});
        window.removeEventListener("keydown", onEscape, {capture: true, passive: false});
        observer.takeRecords();
        observer.disconnect();
        if (signal) signal.removeEventListener("abort", onAbort, {passive: true, once: true});
        // XXX check this behavior
        if (element.parentElement) element.dispatchEvent(new Event("fullwindowchange"));
        else window.dispatchEvent(new Event("fullwindowchange"));
        if (resolve) resolve();
        return;
      }
    });
    observer.observe(document.body, {subtree: true, attributes: true, childList: true});

    element.classList.add("fullwindow");
    document.body.classList.add("fullwindow-body");
    element.dispatchEvent(new Event("fullwindowchange"));
    window.addEventListener("keydown", onEscape, {capture: true, passive: false});
    window.addEventListener("focus", onFocus, {capture: true, passive: true});
    return promise;
  }

  requestFullwindow.toScript = function () { return "(" + script.toString() + "())"; };
  requestFullwindow._requiredGlobals = ["MutationObserver", "Promise"];  // document, window
  return requestFullwindow;
}());
