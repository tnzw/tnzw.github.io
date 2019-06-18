this.FileOpenerAp = (function script() {
  "use strict";

  /*! FileOpenerApp.js Version 0.1.0

      Copyright (c) 2017 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

    function FileOpenerApp(options) {
      //this.baseUrl = (options && options.baseUrl) || location.origin + location.pathname;
      var ths = this;
      this.element = dce("div", null, [
        this.actionDiv = dce("div", null, [
          this.fileInputLabel = dce("label", null, [
            "Open: ",
            this.fileInput = dce("input", {type: "file", on: {change: this.runOpenFile.bind(this)}})
          ]), " ",
          this.downloadA = dce("a", {href: "#", style: "display:none"}, ["Download"])
        ]),
        this.subAppDiv = dce("div", null, ["Please open a file."])
      ]);
      this.downloadA.addEventListener("click", function (event) {
        function getFileName() {
          return (typeof ths.subApp.getFileName === "function" && ths.subApp.getFileName()) ||
            (ths.fileInput.files[0] && ths.fileInput.files[0].name) ||
            "untitled";
        }
        if (ths.subApp) {
        if (typeof ths.subApp.getDataAsBytes === "function") {
          ths.downloadA.href = "data:application/octet-stream;base64," + encodeBytesToBase64(ths.subApp.getDataAsBytes());
          ths.downloadA.download = getFileName();
          setTimeout(function () { ths.downloadA.href = "#"; ths.downloadA.download = ""; });
          return true;
        }
        if (typeof ths.subApp.getDataAsText === "function") {
          ths.downloadA.href = "data:text/plain;base64," + encodeStringToBase64(ths.subApp.getDataAsText());
          ths.downloadA.download = getFileName();
          setTimeout(function () { ths.downloadA.href = "#"; ths.downloadA.download = ""; });
          return true;
        }
        }
        event.preventDefault();
        return false;
      }, false);
    }
    FileOpenerApp.prototype.element = null;
    FileOpenerApp.guessAppFromFileName = function (fileName) {
      switch (fileName.replace(/^.*\./g, "")) {
        //case "ogg": return AudioPlayerApp;
        //case "webm": return VideoPlayerApp;
        case "pdf": return TcHexEditorApp;  // true ?
        case "js":
        case "txt": return TcCodeMirrorApp;
      }
      return null;
    };
    FileOpenerApp.guessAppFromBytes = function (bytes) {
      // https://golang.org/src/net/http/sniff.go
      // https://wiki.xiph.org/MIMETypesCodecs
      if (bytes.length > 512) bytes = bytes.slice(0, 512);
      if (bytes.length === 0) return TcCodeMirrorApp;
      var i = 0, b = 0;
      //var str = decodeUt8ToString(bytes), i = 0, b = 0;
      //function equalsMin(a, b) {
      //  if (a.length < b.length) return false;
      //  var i = 0;
      //  while (i++ < b.length) if (a[i] !== b[i]) return false;
      //  return true;
      //}
      //if (/^\s*<(!doctype html|html|head|script|iframe|h1|div|font|table|a|style|title|b|body|br|p|!--)[ >]/i.test(str)) return "text/html;charset=utf-8";
      //if (/^\s*<\?xml/.test(str)) return "text/xml;charset=utf-8";
      //if (str.startsWith("%PDF-")) return "application/pdf";
      //if (str.startsWith("%!PS-Adobe-")) return "application/postscript";
      //if (equalsMin(bytes. [0xFE, 0xFF]) && bytes.length >= 4) return "text/plain;charset=utf-16be";
      //if (equalsMin(bytes. [0xFF, 0xFE]) && bytes.length >= 4) return "text/plain;charset=utf-16le";
      //if (equalsMin(bytes. [0xEF, 0xBB, 0xBF]) && bytes.length >= 4) return "text/plain;charset=utf-8";
      //if (str.startsWith("GIF87a")) return "image/gif";
      //if (str.startsWith("GIF89a")) return "image/gif";
      //if (equalsMin(bytes, [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])) return "image/png";
      //if (equalsMin(bytes, [0xFF, 0xD8, 0xFF])) return "image/jpeg";
      //if (str.startsWith("BM")) return "image/bmp";
      //if (str.startsWith("RIFF") && decodeExtendedAsciiCodesToString(bytes.slice(8, 14)) === "WEBPVP") return "image/webp";
      //if (equalsMin(bytes, [0x00, 0x00, 0x01, 0x00])) return "image/vnd.microsoft.icon";
      //if (equalsMin(bytes, [0x4F, 0x67, 0x67, 0x53, 0x00])) return "application/ogg";
      //if (str.startsWith("RIFF") && decodeExtendedAsciiCodesToString(bytes.slice(8, 12)) === "WAVE") return "audio/wave";
      //if (equalsMin(bytes, [0x1A, 0x45, 0xDF, 0xA3])) return "video/webm";
      //if (equalsMin(bytes, [0x52, 0x61, 0x72, 0x20, 0x1A, 0x07, 0x00])) return "application/x-rar-compressed";
      //if (equalsMin(bytes, [0x50, 0x4B, 0x03, 0x04])) return "application/zip";
      //if (equalsMin(bytes, [0x1F, 0x8B, 0x08])) return "application/x-gzip";
      //mp4Sig{},
      while (i < bytes.length)
        if ((b = bytes[i++]) <= 0x08 ||
            b === 0x0B ||
            0x0E <= b && b <= 0x1A ||
            0x1C <= b && b <= 0x1F)
          return TcHexEditorApp; //return "application/octet-stream";
      return TcCodeMirrorApp; //return "text/plain;charset=utf-8";
    };

    FileOpenerApp.prototype.runOpenFile = function () {
      if (this.fileInput.files.length === 0) {
        this.subAppDiv.textContent = "Please open a file.";
        this.downloadA.style.display = "none";
        return;
      }
      var App = FileOpenerApp.guessAppFromFileName(this.fileInput.files[0].name),
          ths = this, p = null;
      if (App === null)
        p = readBlob(this.fileInput.files[0], "ArrayBuffer").
        then(function (ab) {
          App = FileOpenerApp.guessAppFromBytes(new Uint8Array(ab));
        });
      else
        p = Promise.resolve();
      p.then(function () {
        if (App === null) App = TcHexEditorApp;
        if (App.prototype.setDataAsBytes)
          return readBlob(ths.fileInput.files[0], "ArrayBuffer");
        if (App.prototype.setDataAsText)
          return readBlob(ths.fileInput.files[0], "Text");
        return readBlob(ths.fileInput.files[0], "ArrayBuffer");
      }).then(function (data) {
        if (data instanceof ArrayBuffer)
          ths.subApp = new App({dataAsBytes: new Uint8Array(data), TextEditorApp: TcCodeMirrorApp});
        else
          ths.subApp = new App({dataAsText: data, TextEditorApp: TcCodeMirrorApp});
        ths.subAppDiv.remove();
        ths.element.appendChild(ths.subAppDiv = ths.subApp.element);
        ths.element.style.width = "100%";
        ths.element.style.height = "90vh";
        if (typeof ths.subApp.getDataAsBytes === "function" ||
            typeof ths.subApp.getDataAsText === "function")
          ths.downloadA.style.display = "inherit";
        else
          ths.downloadA.style.display = "none";
      });
    };

    //mimeTypeByExtensionDict = {
    //  // contains mimetypes that a browser can handle
    //  // fill other mime types ?
    //  ".appcache": "text/cache-manifest;charset=utf-8",
    //  ".avi": "video/avi",
    //  ".bmp": "image/bmp",
    //  ".css": "text/css;charset=utf-8",
    //  ".gif": "image/gif",
    //  ".gz": "application/x-gzip",
    //  ".flac": "audio/x-flac",
    //  ".htm": "text/html;charset=utf-8",
    //  ".html": "text/html;charset=utf-8",
    //  ".ico": "image/vnd.microsoft.icon",
    //  ".jpeg": "image/jpeg",
    //  ".jpg": "image/jpeg",
    //  ".js": "application/javascript",
    //  ".json": "application/json",
    //  ".mp3": "audio/mp3",
    //  ".mp4": "video/mp4",
    //  ".mov": "video/quicktime",
    //  ".ogg": "audio/ogg",
    //  ".opus": "audio/ogg;codecs=opus",
    //  ".pdf": "application/pdf",
    //  ".png": "image/png",
    //  ".svg": "image/svg+xml;charset=utf-8",
    //  ".tif": "image/tiff",
    //  ".txt": "text/plain;charset=utf-8",
    //  ".wav": "audio/wav",
    //  ".webm": "video/webm",
    //  ".xml": "text/xml;charset=utf-8",
    //  ".zip": "application/zip"
    //};

    //FileOpenerApp._createElement = function (tag, attrs, content) {
    //  var e = document.createElement(tag), i = 0, d = {};
    //  Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); });
    //  //Object.keys(listeners || {}).forEach(function (t) { listeners[t].forEach(function (fn) { e.addEventListener(t, fn); }); });
    //  if (typeof content === "string") e.innerHTML = content;
    //  else (content || []).forEach(function (o) { e.appendChild(typeof o === "string" ? document.createTextNode(o) : o); });
    //  return e;
    //};
    FileOpenerApp.toScript = function () { return "(" + script.toString() + "())"; };
    FileOpenerApp._requiredGlobals = [
      "dce",
      "readBlob",
      "decodeUtf8ToString",
      "encodeStringToBase64",
      "TcCodeMirrorApp",
      "TcHexEditorApp"
    ];
    return FileOpenerApp;

}());
