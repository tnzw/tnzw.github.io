this.TcHexEditorApp = (function script() {
  "use strict";

  /*! TcHexEditorApp.js Version 1.0.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function TcHexEditorApp(params) {
    //     var app = new TcHexEditorApp();
    //     document.body.appendChild(app.element);

    // TextEditorApp parameter is not updatable !
    if (params && params.TextEditorApp !== undefined)
      this.textapp = new params.TextEditorApp();
    else
      this.textapp = new TcTextareaApp();  // XXX fallback ?
    this.element = this.textapp.element;
    this.update(params);
  }
  TcHexEditorApp.prototype.element = null;
  TcHexEditorApp.prototype.update = function (params) {
    if (params) {
      if (params.dataAsBytes !== undefined) this.setDataAsBytes(params.dataAsBytes);
      else if (params.dataAsHexadecimal !== undefined) this.setDataAsHexadecimal(params.dataAsHexadecimal);
    }
  };
  TcHexEditorApp.prototype.setDataAsBytes = function (bytes) {
    this.textapp.setDataAsText(TcHexEditorApp.dumpBytesToHexadecimal(bytes));
  };
  TcHexEditorApp.prototype.getDataAsBytes = function () {
    return TcHexEditorApp.decodeHexadecimalWithCommentsToBytes(this.textapp.getDataAsText());
  };
  TcHexEditorApp.prototype.setDataAsHexadecimal = function (text) {
    this.textapp.setDataAsText(TcHexEditorApp.dumpBytesToHexadecimal(TcHexEditorApp.decodeHexadecimalToBytes(text)));
  };
  TcHexEditorApp.prototype.getDataAsHexadecimal = function () {
    return TcHexEditorApp.sanitizeHexadecimalWithComments(this.textapp.getDataAsText());
  };


  TcHexEditorApp.sanitizeHexadecimalWithComments = function (text) {
    text = text.replace(/\|.*/gm, "").replace(/\s/g, "")  // ignore comments and whitespaces
    if (/[^a-fA-F0-9]/.test(text)) throw new Error("invalid character");
    if (text.length % 2) throw new Error("text.length % 2 !== 0");
    return text;
  };
  TcHexEditorApp.decodeHexadecimalToBytes = function (text) {
    text = text.replace(/\s/g, "")  // ignore whitespaces
    if (/[^a-fA-F0-9]/.test(text)) throw new Error("invalid character");
    if (text.length % 2) throw new Error("text.length % 2 !== 0");
    var i = 0, j = 0,
        bytes = new Array(text.length / 2);
    for (; i < text.length; i += 2)
      bytes[j++] = parseInt(text.slice(i, i + 2), 16);
    return bytes;
  };
  TcHexEditorApp.decodeHexadecimalWithCommentsToBytes = function (text) {
    text = text.replace(/\|.*/gm, "").replace(/\s/g, "")  // ignore comments and whitespaces
    if (/[^a-fA-F0-9]/.test(text)) throw new Error("invalid character");
    if (text.length % 2) throw new Error("text.length % 2 !== 0");
    var i = 0, j = 0,
        bytes = new Array(text.length / 2);
    for (; i < text.length; i += 2)
      bytes[j++] = parseInt(text.slice(i, i + 2), 16);
    return bytes;
  };
  TcHexEditorApp.dumpBytesToHexadecimal = function (bytes) {
    // 63 6f 75 63 6f 75 63 6f  75 63 6f 75 63 6f 75 63  |coucoucoucoucouc| 00000000
    // 6f 75                                             |ou|               00000010
    var res = "", memi = 0, bi = 0, ai = 0, l = bytes.length;
    for (memi = 0; memi < l; memi += 0x10) {
      res += ("0" + bytes[bi++].toString(16)).slice(-2) + " ";
      while (bi < l && bi % 0x08) res += ("0" + bytes[bi++].toString(16)).slice(-2) + " ";
      res += " ";
      while (bi < l && bi % 0x10) res += ("0" + bytes[bi++].toString(16)).slice(-2) + " ";
      if (bi % 0x10) res += "   ".repeat(0x10 - (bi % 0x10)) + " |";
      else res += " |";
      do {
        if (bytes[ai] >= 32 && bytes[ai] <= 126) res += String.fromCharCode(bytes[ai]);
        else res += ".";
        ai += 1;
      } while (ai < l && ai % 0x10);
      res += "|";
      if (ai % 0x10) { do { res += " " } while (ai++ % 0x10); }
      else res += " ";
      res += ("0000000" + memi.toString(16)).slice(-8) + "\n";
    }
    //res += ("0000000" + bytes.length.toString(16)).slice(-8);
    return res;
  };
  TcHexEditorApp.toScript = function () { return "(" + script.toString() + "())"; };
  TcHexEditorApp._requiredGlobals = ["TcTextareaApp"];

  return TcHexEditorApp;
}());
