# uri_component_encode.py Version 1.0.0
# Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def uri_component_encode():
  def uri_component_encode(bb):
    scheme = uri_component_encode.scheme
    if isinstance(bb, str): bb = bb.encode("UTF-8", "surrogateescape")
    return bytes(_ for b in bb for _ in scheme[b])
  uri_component_encode.scheme = (
    b'%00', b'%01', b'%02', b'%03', b'%04', b'%05', b'%06', b'%07',
    b'%08', b'%09', b'%0A', b'%0B', b'%0C', b'%0D', b'%0E', b'%0F',
    b'%10', b'%11', b'%12', b'%13', b'%14', b'%15', b'%16', b'%17',
    b'%18', b'%19', b'%1A', b'%1B', b'%1C', b'%1D', b'%1E', b'%1F',
    b'%20',   b'!', b'%22', b'%23', b'%24', b'%25', b'%26',   b"'",
      b'(',   b')',   b'*', b'%2B', b'%2C',   b'-',   b'.', b'%2F',
      b'0',   b'1',   b'2',   b'3',   b'4',   b'5',   b'6',   b'7',
      b'8',   b'9', b'%3A', b'%3B', b'%3C', b'%3D', b'%3E', b'%3F',
    b'%40',   b'A',   b'B',   b'C',   b'D',   b'E',   b'F',   b'G',
      b'H',   b'I',   b'J',   b'K',   b'L',   b'M',   b'N',   b'O',
      b'P',   b'Q',   b'R',   b'S',   b'T',   b'U',   b'V',   b'W',
      b'X',   b'Y',   b'Z', b'%5B', b'%5C', b'%5D', b'%5E',   b'_',
    b'%60',   b'a',   b'b',   b'c',   b'd',   b'e',   b'f',   b'g',
      b'h',   b'i',   b'j',   b'k',   b'l',   b'm',   b'n',   b'o',
      b'p',   b'q',   b'r',   b's',   b't',   b'u',   b'v',   b'w',
      b'x',   b'y',   b'z', b'%7B', b'%7C', b'%7D',   b'~', b'%7F',
    b'%80', b'%81', b'%82', b'%83', b'%84', b'%85', b'%86', b'%87',
    b'%88', b'%89', b'%8A', b'%8B', b'%8C', b'%8D', b'%8E', b'%8F',
    b'%90', b'%91', b'%92', b'%93', b'%94', b'%95', b'%96', b'%97',
    b'%98', b'%99', b'%9A', b'%9B', b'%9C', b'%9D', b'%9E', b'%9F',
    b'%A0', b'%A1', b'%A2', b'%A3', b'%A4', b'%A5', b'%A6', b'%A7',
    b'%A8', b'%A9', b'%AA', b'%AB', b'%AC', b'%AD', b'%AE', b'%AF',
    b'%B0', b'%B1', b'%B2', b'%B3', b'%B4', b'%B5', b'%B6', b'%B7',
    b'%B8', b'%B9', b'%BA', b'%BB', b'%BC', b'%BD', b'%BE', b'%BF',
    b'%C0', b'%C1', b'%C2', b'%C3', b'%C4', b'%C5', b'%C6', b'%C7',
    b'%C8', b'%C9', b'%CA', b'%CB', b'%CC', b'%CD', b'%CE', b'%CF',
    b'%D0', b'%D1', b'%D2', b'%D3', b'%D4', b'%D5', b'%D6', b'%D7',
    b'%D8', b'%D9', b'%DA', b'%DB', b'%DC', b'%DD', b'%DE', b'%DF',
    b'%E0', b'%E1', b'%E2', b'%E3', b'%E4', b'%E5', b'%E6', b'%E7',
    b'%E8', b'%E9', b'%EA', b'%EB', b'%EC', b'%ED', b'%EE', b'%EF',
    b'%F0', b'%F1', b'%F2', b'%F3', b'%F4', b'%F5', b'%F6', b'%F7',
    b'%F8', b'%F9', b'%FA', b'%FB', b'%FC', b'%FD', b'%FE', b'%FF',
  )
  return uri_component_encode
uri_component_encode = uri_component_encode()
