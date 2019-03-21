this.createNullPrototypedInstance = (function script() {
  "use strict";

  /*! createNullPrototypedInstance.js Version 1.0.0

      Copyright (c) 2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */    

  function createNullPrototypedInstance(dict) {
    var keys = null, i = 0, instance = Object.create(null);
    if (dict) {
      keys = Object.keys(dict);
      for (; i < keys.length; i = (i + 1)|0) instance[keys[i]] = dict[keys[i]];
    }
    return instance;
  }
  createNullPrototypedInstance.toScript = function () { return "(" + script.toString() + "())"; };
  createNullPrototypedInstance._requiredGlobals = ["Object"];
  return createNullPrototypedInstance;

}());
