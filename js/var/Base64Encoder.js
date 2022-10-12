this.Base64Encoder = (function script() {
  "use strict";

  /*! Base64Encoder.js Version 1.0.0

      Copyright (c) 2022 <tnzw@github.triton.ovh>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // see original code in ../../py3/def/Base64Encoder.py

  // follows javascript Encoder() methods
  // see https://developer.mozilla.org/en-US/docs/Web/API/TextEncoder
  class Base64Encoder {
    // Base64Encoder(opt)
    //
    // opt:
    //   scheme : The scheme to use bytes(64 or more)
    //          => (default) "standard" (or STANDARD_SCHEME)
    //          => "url" (or URL_SCHEME)
    //          => <CUSTOM_SCHEME> (`computeScheme(codes, padding)`)
    //   cast => "bytes"            : (default) cast the returned transcoded values to Uint8Array.
    //        => null               : do not cast, returns transcoded byte iterator instead.
    //   state : internal use only.
    //
    // Interfaces:
    // - copyable (ie. `copy()`)
    // - transcoder (ie. `transcode(iterable = null, {stream: false})`)
    static STANDARD_CODES = Object.freeze([].map.call('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', _ => _.charCodeAt(0)));
    static URL_CODES = Object.freeze([].map.call('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_', _ => _.charCodeAt(0)));
    static computeScheme(codes, padding) {
      // opt:
      //   codes   => Uint8Array(64): the list of code to use for decoding
      //   padding => bytes("=")    : each one of these bytes may be concidered as padding
      if (padding === undefined) padding = [61];  // b"="
      const a = Array.from(codes);
      a.push(...padding);
      return a;
    }
    static STANDARD_SCHEME = Object.freeze([].map.call('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=', _ => _.charCodeAt(0)));
    static URL_SCHEME = Object.freeze([].map.call('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_=', _ => _.charCodeAt(0)));
    copy() {
      return new Base64Encoder({scheme: this.scheme, cast: this.cast, state: this.state});
    }
    constructor(opt) {
      opt = opt ?? {}; function get(o, k, v) { if (o[k] === undefined) return v; return o[k]; }
      let scheme = get(opt, 'scheme', 'standard'), cast = get(opt, 'cast', 'Uint8Array'), state = get(opt, 'state', 0);
      // scheme
      this.scheme = get({
        standard: Base64Encoder.STANDARD_SCHEME,
        url: Base64Encoder.URL_SCHEME,
      }, scheme, scheme);
      // cast
      function castArray(generator) { return Array.from(generator); }
      function castString(generator) { return String.fromCodePoint(...generator); }
      function castUint8Array(generator) { return Uint8Array.from(generator); }
      this.cast = get({
        Uint8Array: castUint8Array, uint8Array: castUint8Array, uint8array: castUint8Array,
        string: castString, binaryString: castString,
        bytes: castUint8Array,
        array: castArray,
        generator: null,
      }, cast, cast);
      // state
      this.state = state;
    }
    transcode(iterable, opt) {
      // transcode(iterable, opt)
      //
      // iterable: a byte iterable value (defaults to null)
      // opt:
      //   stream => false: tells the transcoder that it is the last transcode operation
      //          => true
      const self = this, stream = opt?.stream ? true : false;
      let iterator;
      function isNullish(v) { return v === undefined || v === null; }
      if (isNullish(iterable)) iterator = "";
      else iterator = iterable[Symbol.iterator]();
      // states are:
      // 0 => [?..]
      // 1 => [A?.]
      // 2 => [AB?]

      function* it() {
        let scheme = self.scheme, state = self.state;
        let cache = state >>> 8; state = state & 0xFF;

        for (let b of iterator) {
          if        (state === 0) {  // [?..]
            yield scheme[b >>> 2];
            cache = b; state = 1;
          } else if (state === 1) {  // [A?.]
            yield scheme[((cache & 0x3) << 4) | (b >>> 4)];
            cache = b; state = 2;
          } else {                   // [AB?]
            yield scheme[((cache & 0xF) << 2) | (b >>> 6)];
            yield scheme[b & 0x3F];
            cache = state = 0;
          }
        }

        if (stream) {
          self.state = ((cache & 0xFF) << 8) | state;
          return;
        }

        if      (state === 0) {}
        else if (state === 1) {
          yield scheme[(cache & 0x3) << 4];
          if (scheme.length > 64) { yield scheme[64]; yield scheme[64]; }
        } else {
          yield scheme[(cache & 0xF) << 2];
          if (scheme.length > 64) { yield scheme[64]; }
        }
        cache = state = 0;
        self.state = ((cache & 0xFF) << 8) | state;
      }
      return self.cast === null ? it() : self.cast(it());
    }
    encode(iterable, opt) { return this.transcode(iterable, opt); }
  }
  Base64Encoder.toScript = function () { return "(" + script.toString() + "())"; };
  return Base64Encoder;

}());
