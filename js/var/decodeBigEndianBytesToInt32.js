(function script(global) {
  "use strict";

  /*! decodeBigEndianBytesToInt32.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function decodeBigEndianBytesToInt32(bb) {
    return (bb[0] << 24) | (bb[1] << 16) | (bb[2] << 8) | bb[3];
  }
  global.decodeBigEndianBytesToInt32 = decodeBigEndianBytesToInt32;

}(this));

