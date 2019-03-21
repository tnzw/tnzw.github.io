this.parseUrl = (function script() {
  "use strict";

  /*! parseUrl.js Version 1.0.0a

      Copyright (c) 2018 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  /*
  */

  function parseUrl(url) {
    // [scheme:[//][[user[:password]@]host[:port]]/][path][?query][#fragment]
    // scheme = [a-z][a-z0-9\+\.\-]* (insensitive case)

    /*
    var tmp = (/^(data:|mailto:|file:)/i).exec(url);
    if (tmp === null) { return parseHttpUrl(url); }
    if (tmp[0] === "data") { return parseDataUrl(url); }
    if (tmp[0] === "mailto") { return parseMailtoUrl(url); }
    if (tmp[0] === "file") { return parseFileUrl(url); }
    return parseHttpUrl(url);  // ftp: irc[s6]?:
    */

    var tmp = parseUrl._parser.exec(url);
    if (tmp === null) { return null; }  // should not happen
    return {
      input: url,
      match: tmp[0],
      scheme: tmp[1],
      doubleSlash: tmp[2],
      user: tmp[3],
      password: tmp[4],
      host: tmp[5] || tmp[6],
      port: tmp[7],
      path: tmp[8],
      query: tmp[9],
      fragment: tmp[10]
    };
    //return parseUrl._parser.exec(url);  // should never return null
  }
  parseUrl._parser = new RegExp([
    "^",
    "(?:",                                 //   scheme://user:password@host:port
      "([a-zA-Z][a-zA-Z0-9\\+\\.\\-]*)",   // 1 scheme
      ":",
      "(//)?",                             // 2 [//]
      "(?:",                               //   [user:password@host:port]
        "(?:",                             //   [user:password@]
          "([^:@/\\?#]*)",                 // 3 user
          "(?::",                          //   [:password]
            "([^@/\\?#]*)",                // 4 password
          ")?",
        "@)?",
        "(?:",                             //   host
          "(\\[[^\\]/\\?#]*\\])",          // 5 host (ipv6)
        "|",
          "([^:/\\?#]*)",                  // 6 host (ipv4, or other)
        ")",
        "(?::",                            //   [:port]
          "([^/\\?#]*)",                   // 7 port
        ")?",
      ")?",
    ")?",
    "([^\\?#]*)",                          // 8 path
    "(\\?[^#])?",                          // 9 [?query]
    "(\\#.*)?",                            //10 [#fragment]
    "$"
  ].join(""));

  parseUrl.toScript = function () { return "(" + script.toString() + "())"; };
  /*parseUrl._requiredGlobals = [
    "parseHttpUrl",
    "parseDataUrl",
    "parseMailtoUrl",
    "parseFileUrl"
  ];*/
  return parseUrl;

}());
