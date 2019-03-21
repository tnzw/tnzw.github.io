this.decodeBase64ToBytes = (function script() {
  "use strict";

  /*! decodeBase64ToBytes.js Version 0.1.7

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  //importScriptsAsync("decodeBase64CodesToBytesChunkAlgorithm.js");

  function decodeBase64ToBytes(text) {
    var ret = [], ee = [], e = null, cache = [];
    decodeBase64CodesToBytesChunkAlgorithm(text, 0, text.length, ret, {
      A:0,B:1,C:2,D:3,E:4,F:5,G:6,H:7,I:8,J:9,K:10,L:11,M:12,
      N:13,O:14,P:15,Q:16,R:17,S:18,T:19,U:20,V:21,W:22,X:23,Y:24,Z:25,
      a:26,b:27,c:28,d:29,e:30,f:31,g:32,h:33,i:34,j:35,k:36,l:37,m:38,
      n:39,o:40,p:41,q:42,r:43,s:44,t:45,u:46,v:47,w:48,x:49,y:50,z:51,
      0:52,1:53,2:54,3:55,4:56,5:57,6:58,7:59,8:60,9:61,
      "+":62,"/":63,  // standard way
      //"-":62,"_":63,  // url way
      "=":64,  // padding value
      " ":65,"\t":66,"\r":67,"\n":68  // ignored values
      // built by `parseBase64SchemeForStringDecoding("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/= \t\r\n")`
    }, ee, cache, true);
    if ((e = ee[0]) !== undefined) {
      if (e.message === "unexpected end of data")// && e.length > 1)
        return ret;
      ee = new Error(e.message);
      ee.index = e.index;
      throw ee;
    }
    return ret;
  }
  decodeBase64ToBytes.toScript = function () { return "(" + script.toString() + "())"; };
  decodeBase64ToBytes._requiredGlobals = ["decodeBase64CodesToBytesChunkAlgorithm"];
  return decodeBase64ToBytes;

}());
