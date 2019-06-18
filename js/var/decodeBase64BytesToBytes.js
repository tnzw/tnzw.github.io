this.decodeBase64BytesToBytes = (function script() {
  "use strict";

  /*! decodeBase64BytesToBytes.js Version 0.1.7

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  //importScriptsAsync("decodeBase64CodesToBytesChunkAlgorithm.js");

  function decodeBase64BytesToBytes(bytes) {
    var ret = [], ee = [], e = null, cache = [];
    decodeBase64CodesToBytesChunkAlgorithm(bytes, 0, bytes.length, ret, {
      65:0,66:1,67:2,68:3,69:4,70:5,71:6,72:7,73:8,74:9,75:10,76:11,77:12,
      78:13,79:14,80:15,81:16,82:17,83:18,84:19,85:20,86:21,87:22,88:23,89:24,90:25,  // A-Z
      97:26,98:27,99:28,100:29,101:30,102:31,103:32,104:33,105:34,106:35,107:36,108:37,109:38,
      110:39,111:40,112:41,113:42,114:43,115:44,116:45,117:46,118:47,119:48,120:49,121:50,122:51,  // a-z
      48:52,49:53,50:54,51:55,52:56,53:57,54:58,55:59,56:60,57:61,  // 0-9
      43:62,47:63,  // "+/" standard way
      //45:62,95:63,  // "-_" url way
      61:64,  // "=" padding value
      32:65,9:66,13:67,10:68  // " \t\r\n" ignored values
      // built by `parseBase64SchemeForDecoding("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/= \t\r\n")`
    }, ee, cache, true);
    if ((e = ee[0]) !== undefined) {
      if (e.message === "unexpected end of data" && e.length > 1)
        return ret;
      ee = new Error(e.message);
      ee.index = e.index;
      throw ee;
    }
    return ret;
  }
  decodeBase64BytesToBytes.toScript = function () { return "(" + script.toString() + "())"; };
  decodeBase64BytesToBytes._requiredGlobals = ["decodeBase64CodesToBytesChunkAlgorithm"];
  return decodeBase64BytesToBytes;

}());
