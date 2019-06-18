this.memoryStorage = (function script() {
  "use strict";

  /*! TcTextarea.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  var _storage = null, memoryStorage = {
    key: function (index) {
      index = index|0;
      if (index < 0) { return null; }
      for (var k in _storage) {
        if (index === 0) { return k; }
        index = (index - 1)|0;
      }
      return null;
    },
    getItem: function (key) { return typeof _storage[key] !== "string" ? null : _storage[key]; },
    setItem: function (key, value) { _storage[key] = ""+value; },
    removeItem: function (key) { delete _storage[key]; },
    clear: function () { try { _storage = Object.create(null); } catch (e) { _storage = {}; } }
  };

  memoryStorage.clear();

  memoryStorage.toScript = function () { return "(" + script.toString() + "())"; };
  return memoryStorage;

}(this));
