this.decodeBase64CodesToBytesChunkAlgorithm = (function script() {
  "use strict";

  /*! decodeBase64CodesToBytesChunkAlgorithm.js Version 0.1.7

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeBase64CodesToBytesChunkAlgorithm(codes, i, l, bytes, schemeCodeMap, events, cache, close) {
    // codes = [...]
    //   bytes to decode
    // XXX
    // bytes = []
    //   where decoded bytes will be written
    // cache = [0, 0, 0, 0, 0]
    //   used by the algorithm
    // schemeCodeMap = {  // the algorithm assumes it perfect
    //     // X: 0-63 char to 6bit values
    //     // X: 64 padding char
    //     // X: >=65 chars to ignore
    //     A:0,B:1,C:2,D:3,E:4,F:5,G:6,H:7,I:8,J:9,K:10,L:11,M:12,
    //     N:13,O:14,P:15,Q:16,R:17,S:18,T:19,U:20,V:21,W:22,X:23,Y:24,Z:25,
    //     a:26,b:27,c:28,d:29,e:30,f:31,g:32,h:33,i:34,j:35,k:36,l:37,m:38,
    //     n:39,o:40,p:41,q:42,r:43,s:44,t:45,u:46,v:47,w:48,x:49,y:50,z:51,
    //     0:52,1:53,2:54,3:55,4:56,5:57,6:58,7:59,8:60,9:61,
    //     "+":62,"/":63,  // standard way
    //     //"-":62,"_":63,  // url way
    //     "=":64,
    //     " ":65,"\t":66,"\r":67,"\n":68
    //   }
    // XXX
    // o.invalidByteError({codes, bytes, cache, index}) - called on invalid byte
    // o.expectedPaddingError({codes, bytes, cache, index}) - called on expected padding
    // o.unexpectedPaddingError({codes, bytes, cache, index}) - called on unexpected padding
    // o.unexpectedEndOfDataError({codes, bytes, cache, schemeCodeMap, index, requiredCodeAmount, requiredCodeIndex, lastCodes}) - called on unexpected end of data
    // close = false (optional)
    // returns bytes of decoded base64

    var code, byte, a, b, c;
    for (; i < l; i += 1) {
      code = schemeCodeMap[byte = codes[i]];
      switch (cache[0]) {
        case 1:  // after first byte state  [A?..]
          if (!(code >= 0)) events.push({type: "error", message: "invalid code", length: 2, index: i, requiredCodeAmount: 4, requiredCodeIndex: 1});
          else if (code === 64) events.push({type: "error", message: "unexpected padding", length: 2, index: i, requiredCodeAmount: 4, requiredCodeIndex: 1});
          else if (code >= 65) {}
          else { bytes.push(((cache[1] << 2) & 0xFC) | ((code >>> 4) & 0x03)); cache[3] = byte; cache[1] = code; cache[0] = 2; }
          break;
        case 2:  // after second byte state  [AB?.]
          if (!(code >= 0)) events.push({type: "error", message: "invalid code", length: 3, index: i, requiredCodeAmount: 4, requiredCodeIndex: 2});
          else if (code === 64) { cache[4] = byte; cache[0] = 4; }
          else if (code >= 65) {}
          else { bytes.push(((cache[1] << 4) & 0xF0) | ((code >>> 2) & 0x0F)); cache[4] = byte; cache[1] = code; cache[0] = 3; }
          break;
        case 3:  // after third byte state  [ABC?]
          if (!(code >= 0)) events.push({type: "error", message: "invalid code", length: 4, index: i, requiredCodeAmount: 4, requiredCodeIndex: 3});
          else if (code === 64) { cache[4] = byte; cache[0] = 0; }
          else if (code >= 65) {}
          else { bytes.push(((cache[1] << 6) & 0xC0) | (code & 0x3F)); cache[0] = 0; }
          break;
        case 4:  // expect padding state  [AB=?]
          if (!(code >= 0)) events.push({type: "error", message: "invalid code", length: 4, index: i, requiredCodeAmount: 4, requiredCodeIndex: 3});
          else if (code === 64) cache[0] = 0;
          else if (code >= 65) {}
          else events.push({type: "error", message: "expected padding", length: 4, index: i, requiredCodeAmount: 4, requiredCodeIndex: 3});
          break;
        default:  // [?...]
          if (!(code >= 0)) events.push({type: "error", message: "invalid code", length: 1, index: i, requiredCodeAmount: 4, requiredCodeIndex: 0});
          else if (code === 64) events.push({type: "error", message: "unexpected padding", length: 1, index: i, requiredCodeAmount: 4, requiredCodeIndex: 0});
          else if (code >= 65) {}
          else { cache[2] = byte; cache[1] = code; cache[0] = 1; }
      }
    }
    if (close) {
      switch (cache[0]) {
        case 1: events.push({type: "error", message: "unexpected end of data", length: 2, index: i, requiredCodeAmount: 4, requiredCodeIndex: 1}); break;
        case 2: events.push({type: "error", message: "unexpected end of data", length: 3, index: i, requiredCodeAmount: 4, requiredCodeIndex: 2}); break;
        case 3:
        case 4: events.push({type: "error", message: "unexpected end of data", length: 4, index: i, requiredCodeAmount: 4, requiredCodeIndex: 3}); break;
      }
    }
    return bytes;
  }
  decodeBase64CodesToBytesChunkAlgorithm.toScript = function () { return "(" + script.toString() + "())"; };
  return decodeBase64CodesToBytesChunkAlgorithm;

}());
