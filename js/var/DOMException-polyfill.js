(function (global) {
  "use strict";
  if (typeof global.DOMException === "undefined")

global.DOMException = (function script() {
  "use strict";

  /*! DOMException-polyfill.js Version 1.0.0

      Copyright (c) 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function DOMException(message) { this.message = "" + message; }
  DOMException.prototype = new Error();
  DOMException.prototype.name = "DOMException";
  DOMException.prototype.constructor = DOMException;
  DOMException.prototype.ABORT_ERR                   = DOMException.ABORT_ERR                   = 20;
  DOMException.prototype.DATA_CLONE_ERR              = DOMException.DATA_CLONE_ERR              = 25;
  DOMException.prototype.DOMSTRING_SIZE_ERR          = DOMException.DOMSTRING_SIZE_ERR          =  2;
  DOMException.prototype.HIERARCHY_REQUEST_ERR       = DOMException.HIERARCHY_REQUEST_ERR       =  3;
  DOMException.prototype.INDEX_SIZE_ERR              = DOMException.INDEX_SIZE_ERR              =  1;
  DOMException.prototype.INUSE_ATTRIBUTE_ERR         = DOMException.INUSE_ATTRIBUTE_ERR         = 10;
  DOMException.prototype.INVALID_ACCESS_ERR          = DOMException.INVALID_ACCESS_ERR          = 15;
  DOMException.prototype.INVALID_CHARACTER_ERR       = DOMException.INVALID_CHARACTER_ERR       =  5;
  DOMException.prototype.INVALID_MODIFICATION_ERR    = DOMException.INVALID_MODIFICATION_ERR    = 13;
  DOMException.prototype.INVALID_NODE_TYPE_ERR       = DOMException.INVALID_NODE_TYPE_ERR       = 24;
  DOMException.prototype.INVALID_STATE_ERR           = DOMException.INVALID_STATE_ERR           = 11;
  DOMException.prototype.NAMESPACE_ERR               = DOMException.NAMESPACE_ERR               = 14;
  DOMException.prototype.NETWORK_ERR                 = DOMException.NETWORK_ERR                 = 19;
  DOMException.prototype.NOT_FOUND_ERR               = DOMException.NOT_FOUND_ERR               =  8;
  DOMException.prototype.NOT_SUPPORTED_ERR           = DOMException.NOT_SUPPORTED_ERR           =  9;
  DOMException.prototype.NO_DATA_ALLOWED_ERR         = DOMException.NO_DATA_ALLOWED_ERR         =  6;
  DOMException.prototype.NO_MODIFICATION_ALLOWED_ERR = DOMException.NO_MODIFICATION_ALLOWED_ERR =  7;
  DOMException.prototype.QUOTA_EXCEEDED_ERR          = DOMException.QUOTA_EXCEEDED_ERR          = 22;
  DOMException.prototype.SECURITY_ERR                = DOMException.SECURITY_ERR                = 18;
  DOMException.prototype.SYNTAX_ERR                  = DOMException.SYNTAX_ERR                  = 12;
  DOMException.prototype.TIMEOUT_ERR                 = DOMException.TIMEOUT_ERR                 = 23;
  DOMException.prototype.TYPE_MISMATCH_ERR           = DOMException.TYPE_MISMATCH_ERR           = 17;
  DOMException.prototype.URL_MISMATCH_ERR            = DOMException.URL_MISMATCH_ERR            = 21;
  DOMException.prototype.VALIDATION_ERR              = DOMException.VALIDATION_ERR              = 16;
  DOMException.prototype.WRONG_DOCUMENT_ERR          = DOMException.WRONG_DOCUMENT_ERR          =  4;

  DOMException.toScript = function () { return '(' + script.toString() + '())'; };
  return DOMException;
})();

})(this);