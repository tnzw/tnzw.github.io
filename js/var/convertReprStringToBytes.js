this.convertReprStringToBytes = (function script() {
  "use strict";

  /*! convertReprStringToBytes.js Version 1.0.0

      Copyright (c) 2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */    

  function convertReprStringToBytes(string) {
    var i = 0, j = 0, k = 0, codepoint = 0, byte = 0,
        bytes = encodeStringToBytes(string);
    while (i < bytes.length) {
      byte = bytes[i]|0;
      if (byte === 0x5C) {
        if (i < bytes.length) {
          byte = bytes[++i]|0;
          switch (byte) {
            case 0x6E: bytes[j++] = 0x0A; ++i; break;  // \n
            case 0x74: bytes[j++] = 0x09; ++i; break;  // \t
            case 0x72: bytes[j++] = 0x0D; ++i; break;  // \r
            case 0x62: bytes[j++] = 0x08; ++i; break;  // \b
            case 0x66: bytes[j++] = 0x0C; ++i; break;  // \f
            case 0x76: bytes[j++] = 0x0B; ++i; break;  // \v
            case 0x22: bytes[j++] = 0x22; ++i; break;  // \"
            case 0x5C: bytes[j++] = 0x5C; ++i; break;  // \\
            case 0x78:  // \x00
              // invalid hexadecimal escape sequence
              bytes[j] = 0;
              for (k = 1; k >= 0; k -= 1) {
                byte = bytes[++i]|0;
                if (0x30 <= byte && byte <= 0x39) bytes[j] |= (byte - 0x30) << (k * 4);
                else if (0x41 <= byte && byte <= 0x46) bytes[j] |= (byte - 0x37) << (k * 4);
                else if (0x61 <= byte && byte <= 0x66) bytes[j] |= (byte - 0x57) << (k * 4);
                else { bytes[j] = 0x78; i -= (1 - k) + 1; break; }
                //else throw new Error("invalid hexadecimal escape sequence");
              }
              ++j; ++i;
              break;
            //case 0x75:  // \u0000
            //  // invalid unicode escape sequence
            //  codepoint = 0;
            //  for (k = 3; k >= 0; k -= 1) {
            //    byte = bytes[++i]|0;
            //    if (0x30 <= byte && byte <= 0x39) codepoint |= (byte - 0x30) << (k * 4);
            //    else if (0x41 <= byte && byte <= 0x46) codepoint |= (byte - 0x37) << (k * 4);
            //    else if (0x61 <= byte && byte <= 0x66) codepoint |= (byte - 0x57) << (k * 4);
            //    else { codepoint = 0x75; i -= (3 - k) + 1; break; }
            //    //else throw new Error("invalid unicode escape sequence");
            //  }
            //  j += encodeCodePointInUtf8Array(codepoint, bytes, j, i).writeLength;
            //  ++i;
            //  break;
            default:
              bytes[j++] = bytes[i++];
          }
        } else {
          bytes[j++] = bytes[i++];  // unexpected end of data | alone backslash
        }
      } else {
        bytes[j++] = bytes[i++];
      }
    }
    return bytes.slice(0, j);
  }
  convertReprStringToBytes.toScript = function () { return "(" + script.toString() + "())"; };
  convertReprStringToBytes._requiredGlobals = ["encodeStringToBytes"];
  return convertReprStringToBytes;

}());
