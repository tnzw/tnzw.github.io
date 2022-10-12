this.Base64Decoder = (function script() {
  "use strict";

  /*! Base64Decoder.js Version 1.0.0

      Copyright (c) 2022 <tnzw@github.triton.ovh>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // see original code in ../../py3/def/Base64Decoder.py

  // follows javascript Decoder() methods
  // see https://developer.mozilla.org/en-US/docs/Web/API/TextDecoder
  class Base64Decoder {
    // Base64Decoder(opt)
    //
    // opt:
    //   errors => "strict" : (default) raise on any error
    //          => "pad"    : add base64 padding before EOF if necessary (eg b"RS" → b"RS==")
    //          => "ignore" : ignore unexpected characters
    //                        ex: b"R=K==A=B=L~OZ" → b"RK==ABLO"
    //   fatal : This parameter cannot be set if `errors` is already defined.
    //         => true  : (default) allow TypeError exception to be thrown, equivalent to `errors: 'strict'`.
    //         => false : equivalent to `errors: 'ignore'`.
    //   scheme : The scheme to use bytes(256)
    //          => (default) "standard" or STANDARD_SCHEME
    //          => "url" or URL_SCHEME
    //          => "mixed_url" or MIXED_URL_SCHEME (combines "standard" and "url" schemes)
    //          => <CUSTOM_SCHEME> (`compute_scheme(codes, padding, ignored)`)
    //   cast => "Uint8Array" : (default) cast the returned transcoded values to Uint8Array.
    //        => null         : do not cast, returns transcoded byte iterator instead.
    //   state : internal use only.
    //
    // Decode errors are TypeError.
    // See https://developer.mozilla.org/en-US/docs/Web/API/TextDecoder/TextDecoder
    //
    // Interfaces:
    // - copyable (ie. `copy()`)
    // - transcoder (ie. `transcode(iterable = null, {stream: false})`)
    static STANDARD_CODES = Object.freeze([].map.call('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/', _ => _.charCodeAt(0)));
    static URL_CODES = Object.freeze([].map.call('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_', _ => _.charCodeAt(0)));
    static computeScheme(codes, padding, ignored) {
      // opt:
      //   codes   => Uint8Array(64)  : the list of code to use for decoding
      //   padding => bytes("=")      : each one of these bytes may be concidered as padding
      //   ignored => bytes(" \n\r\t"): ignores each one of these bytes from input
      if (padding === undefined) padding = [61];  // b"="
      if (ignored === undefined) ignored = [32, 10, 13, 9];  // b" \n\r\t"
      let i = 0;
      const struct = new Array(256); for (; i < 256; i += 1) struct[i] = 255;
      for (let _ of ignored) struct[_] = 65;
      for (let _ in padding) struct[_] = 64;
      i = 0; for (let _ of codes) struct[_] = i++;
      return struct;
    }
    static STANDARD_SCHEME = Object.freeze([].map.call('\xff\xff\xff\xff\xff\xff\xff\xff\xffAA\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff>\xff\xff\xff?456789:;<=\xff\xff\xff@\xff\xff\xff\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\xff\xff\xff\xff\xff\xff\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff', _ => _.charCodeAt(0)));
    static URL_SCHEME = Object.freeze([].map.call('\xff\xff\xff\xff\xff\xff\xff\xff\xffAA\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff>\xff\xff456789:;<=\xff\xff\xff@\xff\xff\xff\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\xff\xff\xff\xff?\xff\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff', _ => _.charCodeAt(0)));
    static MIXED_URL_SCHEME = Object.freeze([].map.call('\xff\xff\xff\xff\xff\xff\xff\xff\xffAA\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xffA\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff>\xff>\xff?456789:;<=\xff\xff\xff@\xff\xff\xff\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\xff\xff\xff\xff?\xff\x1a\x1b\x1c\x1d\x1e\x1f !"#$%&\'()*+,-./0123\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff', _ => _.charCodeAt(0)));
    copy() {
      return new Base64Decoder({errors: this.errors, scheme: this.scheme, cast: this.cast, state: this.state});
    }
    constructor(opt) {
      opt = opt ?? {}; function get(o, k, v) { if (o[k] === undefined) return v; return o[k]; }
      let errors = opt.errors, fatal = opt.fatal, scheme = get(opt, 'scheme', 'standard'), cast = get(opt, 'cast', 'Uint8Array'), state = get(opt, 'state', 0);
      //for (let k of Object.keys(opt)) if (!({errors:1,fatal:1,scheme:1,cast:1,state:1})[k]) throw new TypeError(`got an unexpected parameter ${k}`);
      // errors + fatal
      if (errors !== undefined) {
        //if (typeof errors !== 'string') throw new TypeError("parameter 'errors' must be a string");
        if (fatal !== undefined &&
            (!fatal && errors === 'strict' ||
             fatal && errors === 'ignore'))
          throw new TypeError("incompatible 'errors' and 'fatal' values");  // ValueError
        this.errors = errors;
      } else if (fatal !== undefined) this.errors = fatal ? 'strict' : 'ignore';
      else this.errors = 'strict';
      // scheme
      this.scheme = get({
        standard: Base64Decoder.STANDARD_SCHEME,
        url: Base64Decoder.URL_SCHEME,
        mixed_url: Base64Decoder.MIXED_URL_SCHEME,
      }, scheme, scheme);
      // cast
      function castArray(generator) { return Array.from(generator); }
      function castBinaryString(generator) { return String.fromCharCode(...generator); }
      function castUint8Array(generator) { return Uint8Array.from(generator); }
      this.cast = get({
        Uint8Array: castUint8Array, uint8Array: castUint8Array, uint8array: castUint8Array,
        binaryString: castBinaryString,
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
      const self = this, stream = opt?.stream ? true : false, ValueError = TypeError;
      let iterator;
      function isNullish(v) { return v === undefined || v === null; }
      //function isIn(v, i) { for (let _ of i) if (v === _) return true; return false; }
      if (isNullish(iterable)) iterator = '';
      else iterator = iterable[Symbol.iterator]();
      // states are:
      // 0 => [?...]
      // 1 => [A?..]
      // 2 => [AB?.]
      // 3 => [ABC?]
      // 4 => [AB=?]

      function checkErrors(errors) {
        switch (errors) { case "strict": case "pad": case "ignore": return errors; }
        throw new RangeError(`unknown error handler name '${errors}'`);
      }

      function* it() {
        //errors, scheme, ignored, padding = self.errors, self.scheme[:64], self.ignored, self.padding;
        let errors = self.errors, scheme = self.scheme,
            state = self.state,
            cache = state >>> 8; state = state & 0xFF;

        for (let b of iterator) {
          let code = scheme[b];

          if (code !== 65) {

            if (code === 64) {  // is padding
              //      (isIn(state, [3,4]))↓
              if      ([0,0,0,1,1][state]) state = 0;  // [ABC=] [AB==]
              else if (state === 2) state = 4;         // [AB=.]
              else {                                   // [=...] [A=..]
                if (errors !== "ignore") {
                  checkErrors(errors);
                  throw new ValueError("unexpected padding");
                }
              }
            } else {
              if (code < 64) {
                if      (state === 0) {}                                          // [A...]
                else if (state === 1) yield (cache << 2) | (code >>> 4);          // [AB..]
                else if (state === 2) yield ((cache & 0xF) << 4) | (code >>> 2);  // [ABC.]
                else if (state === 3) yield ((cache & 0x3) << 6) | code;          // [ABCD]
                cache = code;
                state = (state + 1) % 4;
              } else if (errors !== "ignore") {
                checkErrors(errors);
                throw new ValueError("invalid code");
              }
            }
          }
        }

        if (stream) {
          self.state = ((cache & 0xFF) << 8) | state;
          return;
        }

        if      (state === 0) {}
        else if (errors === "ignore") state = 0;
        else if (errors === "pad") {
          if (state === 1) throw new ValueError("unexpected end of data");
          state = 0;
        } else {
          checkErrors(errors);
          throw new ValueError("unexpected end of data");
        }

        self.state = ((cache & 0xFF) << 8) | state;
      }
      return self.cast === null ? it() : self.cast(it());
    }
    decode(iterable, opt) { return this.transcode(iterable, opt); }
  }
  Base64Decoder.toScript = function () { return "(" + script.toString() + "())"; };
  return Base64Decoder;

}());
