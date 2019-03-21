this.EventManager = (function script() {
  "use strict";

  /*! EventManager.js Version 1.1.1

      Copyright (c) 2015-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // - Force to have private listeners like in html5 EventTarget objects.
  // - `dispatchEvent` is synchronous function, but it can be called like this: `setImmediate(em.dispatchEvent.bind(em), 0, event);`  // XXX create event in the next tick call ?

  function EventManager() {
    // can be mixed in with:
    //     mixObjectProperties(Constructor.prototype, EventManager.prototype);
  }
  EventManager._wm = typeof WeakMap === "function" ? new WeakMap() : {get: function (a) { return a; }, set: function () { return; }};
  EventManager._priv = function (o) {
    var tmp = EventManager._wm.get(o);
    if (tmp) return tmp;
    EventManager._wm.set(o, {});
    return EventManager._wm.get(o);
  };
  EventManager.prototype.addEventListener = function (type, listener, options) {
    // Be careful of memory leaks !
    // If you addEventListener, the listener cannot be garbage collected
    // unless you removeEventListener.

    // https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener

    if (typeof listener !== "function" || typeof listener !== "object" || listener === null) { return; }
    var em = EventManager._priv(this),
        key = "[[EventManagerListeners:" + type + "]]",
        d = {listener: listener, capture: false, once: false, passive: false, _firing: false},
        i = 0, a = em[key];
    if (typeof options === "boolean") d.capture = options;
    else if (options) {
      if (options.capture) d.capture = true;
      if (options.once) d.once = true;
      if (options.passive) d.passive = true;
    }
    if (typeof this._onBeforeAddEventListener === "function")
      if (this._onBeforeAddEventListener(type, d) === false)
        return;
    if (a) {
      while (i < a.length)
        if (a[i].listener === listener &&
            a[i].capture === d.capture)
          return;
      a.push(d);
    } else
      em[key] = [d];
    if (typeof this._onAddEventListener === "function")
      this._onAddEventListener(type, d);
  };
  EventManager.prototype.removeEventListener = function (type, listener, options) {
    // https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/removeEventListener

    var em = EventManager._priv(this),
        key = "[[EventManagerListeners:" + type + "]]",
        listeners = em[key] || [],
        d = {listener: listener, capture: false, passive: false},
        i = 0, found = false;
    if (typeof options === "boolean") d.capture = options;
    else if (options) {
      if (options.capture) d.capture = true;
      if (options.passive) d.passive = true;
    }
    if (typeof this._onBeforeRemoveEventListener === "function")
      this._onBeforeRemoveEventListener(type, d);  // XXX allow to control removal ?
    for (i = 0; i < listeners.length; i += 1) {
      if (listeners[i].listener === listener &&
          listeners[i].capture === d.capture) {
        if (listeners.length === 1) {
          delete em[key];
        } else {
          listeners.splice(i, i + 1);
          i -= 1;
        }
        found = true;
      }
    }
    if (found && typeof this._onRemoveEventListener === "function")
      this._onRemoveEventListener(type, d);
  };
  EventManager.prototype.dispatchEvent = function (event) {
    // Should be called in a next tick
    // Usage: setImmediate(_=>em.dispatchEvent(new MyEvent(...)))

    // The actual behavior cannot be immitated.. that's why we use synchronous call of the listeners
    // This should be the behavior :
    // window.a = []; window.p = Promise.resolve(true);
    // window.onmessage = function (e) {
    //   a.push(4);
    //   p.then(function () {
    //     a.push(5);
    //   }).then(function () {
    //     a.push(6);
    //   });
    // };
    // a.push(1);
    // window.postMessage("coucou");  // === equals setEventTimeout(_=>em.dispatchEvent(new MyPostMessageEvent(...)))
    // a.push(2);
    // window.postMessage("hello");
    // a.push(3);
    // -> a outputs [1,2,3,4,5,6,4,5,6];
    // -> with `p.then(onmessage)` instead of `postMessage()` -> a outputs [1,2,3,4,4,5,5,6,6]

    // XXX event.type should be lower cased ?
    var em = EventManager._priv(this),
        key = "[[EventManagerListeners:" + event.type + "]]",
        key2 = "on" + event.type,
        listeners = em[key] || [],
        i = 0, l = null, fired = false;
    // XXX handle event.cancellable property here
    //     return false if cancelled
    if (typeof this._onBeforeDispatchEvent === "function")
      this._onBeforeDispatchEvent(event);  // XXX allow to control dispatching ?
    if (typeof this[key2] === "function") {
      // XXX call _onDispatchingEvent ?
      try { this[key2](event); } catch (e) { if (typeof this._onError === "function") this._onError(e); }  // XXX protect _onError call try/catch ?
    }
    for (i = 0; i < listeners.length; i += 1)
      listeners[i]._firing = true;
    do {
      fired = false;
      for (i = 0; i < listeners.length; i += 1)
        if ((l = listeners[i])._firing) {
          l._firing = false;
          if (typeof this._onDispatchingEvent === "function")
            if (this._onDispatchingEvent(l, event) === false)  // XXX is it a good idea ?
              continue;
          if (l.once) { listeners.splice(i, i + 1); i -= 1; }  // XXX call a _onRemoveEventListener ? I don't think
          // XXX add a recursive dispatching protection ? yes, only for this event reference 'The event is already being dispatched.'
          if (typeof l.listener === "function") {
            try { l.listener.call(this, event);  } catch (e) { if (typeof this._onError === "function") this._onError(e); }  // XXX protect _onError call with try/catch ?
          } else if (typeof l.listener.handleEvent === "function") {
            try { l.listener.handleEvent(event); } catch (e) { if (typeof this._onError === "function") this._onError(e); }  // XXX protect _onError call with try/catch ?
          }
          fired = true;
          break;
        }
    } while (fired);
    if (typeof this._onDispatchEvent === "function")
      this._onDispatchEvent(event);
    return true;
  };
  EventManager.prototype._onBeforeAddEventListener = null;
  EventManager.prototype._onAddEventListener = null;
  EventManager.prototype._onBeforeRemoveEventListener = null;
  EventManager.prototype._onRemoveEventListener = null;
  EventManager.prototype._onBeforeDispatchEvent = null;
  EventManager.prototype._onDispatchingEvent = null;
  EventManager.prototype._onDispatchEvent = null;
  EventManager.prototype._onError = function (e) { console.error(e); };  // XXX is it good idea ?

  EventManager.toScript = function () { return "(" + script.toString() + "())"; };
  return EventManager;
}());
