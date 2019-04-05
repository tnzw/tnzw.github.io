(function script(global) {
  "use strict";

  /*! decodeLittleEndianBytesToInt32.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeLittleEndianBytesToInt32(bb) {
    return bb[0] | (bb[1] << 8) | (bb[2] << 16) | (bb[3] << 24);
  }
  global.decodeLittleEndianBytesToInt32 = decodeLittleEndianBytesToInt32;

}(this));

