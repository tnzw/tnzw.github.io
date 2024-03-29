this.TcTextarea = (function script() {
  "use strict";

  /*! TcTextarea.js Version 1.2.1

      Copyright (c) 2016-2019, 2021 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  function TcTextarea(textarea, options) {
    this._textarea = textarea;
    this.options = options || {};
    this.handledEvent = null;
  }

  // CodeMirror similar properties/methods //

  TcTextarea.fromTextArea = function (textarea, options) {
    if (textarea._tcTextareaCtl === undefined) {
      textarea._tcTextareaCtl = new TcTextarea(textarea, options);
      textarea._tcTextareaCtl.startEventHandling();
    }
    return textarea._tcTextareaCtl;
  };
  TcTextarea.commands = {};
  TcTextarea.defaults = {};
  TcTextarea.keyMap = {};
  TcTextarea.keyMap.basic = {};
  TcTextarea.keyMap.default = {fallthrough: "basic"};
  TcTextarea.optionHandlers = {};
  TcTextarea.modes = {};
  TcTextarea.version = "20211125";
  TcTextarea.prototype.getWrapperElement = function () { return this._textarea; };
  TcTextarea.prototype.getTextArea = function () { return this._textarea; };
  TcTextarea.prototype.toTextArea = function () { return; };
  TcTextarea.prototype.getOption = function (key) { return this.options ? this.options[key] : undefined; };
  TcTextarea.prototype.setOption = function (key, value) { if (TcTextarea.optionHandlers[key]) TcTextarea.optionHandlers[key](this, value); if (!this.options) this.options = {}; this.options[key] = value; };
  TcTextarea.prototype.getValue = function () { return this._textarea.value; };
  TcTextarea.prototype.setValue = function (value) { this._textarea.value = value; };
  TcTextarea.prototype.save = function () { return; };
  TcTextarea.prototype.focus = function () { this._textarea.focus(); };
  TcTextarea.prototype.hasFocus = function () { return this._textarea === document.activeElement; };
  TcTextarea.prototype.isReadOnly = function () { return this._textarea.disabled || this._textarea.readOnly || (this.options && this.options.readOnly) ? true : false; };
  TcTextarea.optionHandlers.readOnly = function (tt, value) { tt._textarea.readOnly = !!value; tt._textarea.disabled = value === "nocursor"; };
  TcTextarea.prototype.getSelection = function () {
    var textarea = this._textarea;
    return textarea.value.slice(textarea.selectionStart, textarea.selectionEnd);
  };
  TcTextarea.prototype.getSelections = function () { return [this.getSelection()]; };
  TcTextarea.prototype.replaceSelection = function (replacement) {
    var textarea = this._textarea;
    this.setRangeText(replacement, textarea.selectionStart, textarea.selectionEnd, "end");
  };
  TcTextarea.prototype.execCommand = function (command) {
    TcTextarea.commands[command](this);
  };

  // Other specific methods //

  TcTextarea.prototype.handleEvent = function (event) {
    this.handledEvent = event;
    try {
      return this.handleEvent[event.type].call(this, event);
    } finally {
      this.handledEvent = null;
    }
  };
  TcTextarea.prototype.handleEvent.keydown = function (event) {
    //var s = event.key || (event.charCode ? String.fromCharCode(event.charCode) : keyCodeStr[event.keyCode]);
    //console.log("keydown", s, event.key, event.code, event.charCode, event.keyCode, event.which);
    var s = "", p = "", k = event.key, shortcuts = null, loopProtection = 999;
    if (/^[a-z]$/.test(k)) { k = k.toUpperCase(); }
    //if (event.metaKey || event.keyCode === 91) { s = "Meta-" + s; }
    if (event.metaKey) { p = "Meta-" + p; }
    if (event.shiftKey) { p = "Shift-" + p; }
    if (event.ctrlKey) { p = "Ctrl-" + p; }
    if (event.keyCode === 225) { p = "AltGraph-" + p; }  // XXX
    if (event.altKey) { p = "Alt-" + p; }

    shortcuts = TcTextarea.keyMap[this.getOption("keyMap") || "default"];
    function exec() {
      if (typeof shortcuts[s] === "string")
        TcTextarea.commands[shortcuts[s]](this);
      else
        shortcuts[s](this);
      if (s !== "Ctrl-C" && s !== "Ctrl-X" && s !== "Ctrl-V")  // XXX HARDCODED
        event.preventDefault();
      // XXX event.stopPropagation(); ???
    }
    switch (1) {
      default:
        s = p + k;          if (shortcuts[s]) { exec.call(this); break; }
        s = p + event.code; if (shortcuts[s]) { exec.call(this); break; }
        while (loopProtection-- && (shortcuts = TcTextarea.keyMap[shortcuts.fallthrough])) {
          s = p + k;          if (shortcuts[s]) { exec.call(this); break; }
          s = p + event.code; if (shortcuts[s]) { exec.call(this); break; }
        }
    }
  };
  TcTextarea.prototype.handleEvent.input = function (event) {
    // for now, this listener "input" is only used to delete autocomplete cache
    this._textarea.removeEventListener("input", this);
    delete this._autocompleteWordVars;
  };
  TcTextarea.prototype.startEventHandling = function () {
    this._textarea.addEventListener("keydown", this, false);  // use capture ?
  };
  TcTextarea.prototype.stopEventHandling = function () {
    this._textarea.removeEventListener("keydown", this, false);  // use capture ?
    this._textarea.removeEventListener("input", this);
  };

  // Textarea utils //

  TcTextarea.prototype.workaroundScroll = function () {
    // XXX Disabled because it triggers 'change' event on setSelection+blur+focus
    //if (this.hasFocus()) {
    //  this._textarea.blur(); this.focus();  // XXX does not work on firefox
    //}
    // XXX idea editor._textarea.scrollTo(null, editor._textarea.scrollTop + 16) ?
  };
  TcTextarea.prototype.fitStyleHeightToText = function (minimumHeight) {
    // oninput = _ => editor.fitStyleHeightToText();
    minimumHeight = minimumHeight|0;
    var textarea = this._textarea, marginBottom = textarea.style.marginBottom, textHeight = textarea.scrollHeight;
    textarea.style.marginBottom = textHeight+"px";
    textarea.style.height = "16px";  // XXX hardcoded
    textHeight = textarea.scrollHeight;
    textarea.style.height = (minimumHeight < textHeight ? textHeight : minimumHeight) + "px";
    textarea.style.marginBottom = marginBottom;
  };

  TcTextarea.prototype._setRangeTextNative = function (replacement, start, end, selectionMode) {
    return this._textarea.setRangeText(replacement, start, end, selectionMode);
  };
  TcTextarea.prototype._setRangeTextPolyfill = function (replacement, start, end, selectionMode) {
    // setRangeText(textarea, replacement[, start, end[, selectionMode]])
    //
    // This function is a polyfill to the textarea.setRangeText experimental method.
    //
    // selectionMode:
    // - "select": Selects the newly inserted text.
    // - "start": Moves the selection to just before the inserted text.
    // - "end": Moves the selection to just after the selected text.
    // - "preserve": Attempts to preserve the selection. This is the default.
    var textarea = this._textarea, cstart = 0, cend = 0, dir = "";
    if (start === undefined) {
      start = textarea.selectionStart;
      end = textarea.selectionEnd;
    }
    switch (selectionMode) {
      case "select":
        cstart = start;
        cend = start + replacement.length;
        break;
      case "start":
        cstart = start;
        cend = start;
        break;
      case "end":
        cstart = start + replacement.length;
        cend = cstart;
        break;
      default:
        if (selectionMode !== undefined && selectionMode !== "preserve") { throw Error("invalid selectionMode " + selectionMode); }
        cend = textarea.selectionEnd;
        if (cend < end) { cend = start + replacement.length; }
        else { cend += replacement.length + start - end; }
        cstart = textarea.selectionStart;
        if (cstart > start) { cstart = cend; }
        dir = textarea.selectionDirection;
    }
    textarea.value = textarea.value.slice(0, start) +
      replacement +
      textarea.value.slice(end);
    textarea.setSelectionRange(cstart, cend, dir);
  };
  TcTextarea.prototype._setRangeTextWithExecCommand = function (replacement, start, end, selectionMode) {
    // setRangeText(textarea, replacement[, start, end[, selectionMode]])
    //
    // This function uses execCommand("insertText", false, ...)
    //
    // selectionMode:
    // - "select": Selects the newly inserted text.
    // - "start": Moves the selection to just before the inserted text.
    // - "end": Moves the selection to just after the selected text.
    // - "preserve": Attempts to preserve the selection. This is the default.
    var textarea = this._textarea, cstart = 0, cend = 0, dir = "";
    if (start === undefined) {
      start = textarea.selectionStart;
      end = textarea.selectionEnd;
    }
    switch (selectionMode) {
      case "select":
        cstart = start;
        cend = start + replacement.length;
        break;
      case "start":
        cstart = start;
        cend = start;
        break;
      case "end":
        cstart = start + replacement.length;
        cend = cstart;
        break;
      default:
        if (selectionMode !== undefined && selectionMode !== "preserve") { throw Error("invalid selectionMode " + selectionMode); }
        cend = textarea.selectionEnd;
        if (cend < end) { cend = start + replacement.length; }
        else { cend += replacement.length + start - end; }
        cstart = textarea.selectionStart;
        if (cstart > start) { cstart = cend; }
        dir = textarea.selectionDirection;
    }
    textarea.setSelectionRange(start, end);
    document.execCommand("insertText", false, replacement);
    textarea.setSelectionRange(cstart, cend, dir);
  };
  TcTextarea.prototype.setRangeText = //(typeof navigator !== "undefined" && /Firefox\//.test(navigator.userAgent)) ?
    //TcTextarea.prototype._setRangeTextNative :
    TcTextarea.prototype._setRangeTextWithExecCommand;
  TcTextarea.prototype.setSelectionRange = function (start, end, direction) {
    this._textarea.setSelectionRange(start, end, direction);
  };
  TcTextarea.prototype.getSelectionRange = function () {
    var textarea = this._textarea;
    return {start: textarea.selectionStart|0, end: textarea.selectionEnd|0, direction: textarea.selectionDirection+""};
  };
  TcTextarea.prototype.moveRange = function moveRange(start, end, offset, selectionMode) {
    var textarea = this._textarea;
    // assuming start <= end
    if (offset < 0) {
      //if (start + offset < 0) { offset = -start; }
      this.setRangeText(
        textarea.value.slice(start, end) +
        textarea.value.slice(start + offset, start),
        start + offset,
        end,
        selectionMode
      );
    } else if (offset > 0) {
      //if (end + offset > textarea.value.length) { offset = textarea.value.length - end; }
      this.setRangeText(
        textarea.value.slice(end, end + offset) +
        textarea.value.slice(start, end),
        start,
        end + offset,
        selectionMode
      );
    }
  };

  TcTextarea.prototype.getCursorPosition = function () {
    var textarea = this._textarea;
    return textarea.selectionDirection[0] === "f" ? textarea.selectionEnd : textarea.selectionStart;
  };
  TcTextarea.prototype.getColumnPosition = function (pos) {
    pos = pos|0;
    return pos - this._textarea.value.lastIndexOf("\n", pos - 1) - 1;
  };
  TcTextarea.prototype.getPreviousGroupPosition = function (pos) {
    pos = pos|0;
    function st(c) { return c === " " || c === "\t"; }
    function s(c) { return " \f\n\r\t\v".indexOf(c) !== -1; }
    function w(c) {
      return (c >= "a" && c <= "z") ||
        (c >= "A" && c <= "Z") ||
        (c >= "0" && c <= "9") ||
        c === "_";
    }
    var value = this._textarea.value;
    if (pos <= 1) { return 0; }
    pos -= 1;
    if (value[pos] === "\n") { return pos; }
    if (st(value[pos])) { pos -= 1; if (pos <= 1) { return 0; } }
    if (w(value[pos])) {
      for (; pos < value.length && w(value[pos]); pos -= 1) {}
      return pos + 1;
    }
    if (st(value[pos])) {
      for (; pos < value.length && st(value[pos]); pos -= 1) {}
      return pos + 1;
    }
    if (!w(value[pos]) && !s(value[pos])) {
      for (; pos < value.length && !w(value[pos]) && !s(value[pos]); pos -= 1) {}
      return pos + 1;
    }
    return 0;
  };
  TcTextarea.prototype.getNextGroupPosition = function (pos) {
    pos = pos|0;
    function st(c) { return c === " " || c === "\t"; }
    function s(c) { return " \f\n\r\t\v".indexOf(c) !== -1; }
    function w(c) {
      return (c >= "a" && c <= "z") ||
        (c >= "A" && c <= "Z") ||
        (c >= "0" && c <= "9") ||
        c === "_";
    }
    var value = this._textarea.value;
    if (value.length < pos) { return value.length; }
    if (value[pos] === "\n") { return pos + 1; }
    if (st(value[pos])) { pos += 1; if (value.length < pos) { return value.length; } }
    if (w(value[pos])) {
      for (; pos < value.length && w(value[pos]); pos += 1) {}
      return pos;
    }
    if (st(value[pos])) {
      for (; pos < value.length && st(value[pos]); pos += 1) {}
      return pos;
    }
    if (!w(value[pos]) && !s(value[pos])) {
      for (; pos < value.length && !w(value[pos]) && !s(value[pos]); pos += 1) {}
      return pos;
    }
    return value.length;
  };
  TcTextarea.prototype.getPreviousWordPosition = function (pos) { pos = pos|0; return pos - /\w*[^\w]*$/.exec(this._textarea.value.slice(0, pos))[0].length; };  // XXX needs to be optimized
  TcTextarea.prototype.getNextWordPosition = function (pos) { pos = pos|0; return pos + /^[^\w]*\w*/.exec(this._textarea.value.slice(pos))[0].length; };  // XXX needs to be optimized
  TcTextarea.prototype.getPreviousWordNlPosition = function (pos) { pos = pos|0; return pos - /\w*[^\w\n]*\n?$/.exec(this._textarea.value.slice(0, pos))[0].length; };  // XXX needs to be optimized
  TcTextarea.prototype.getNextWordNlPosition = function (pos) { pos = pos|0; return pos + /^\n?[^\w\n]*\w*/.exec(this._textarea.value.slice(pos))[0].length; };  // XXX needs to be optimized
  TcTextarea.prototype.getLineStartPosition = function (pos) {
    pos = pos|0;
    return this._textarea.value.lastIndexOf("\n", pos - 1) + 1;
  };
  TcTextarea.prototype.getLineEndPosition = function (pos) {
    pos = pos|0;
    var end = this._textarea.value.indexOf("\n", pos);
    return end === -1 ? this._textarea.value.length : end;
  };
  TcTextarea.prototype.getLineUpPosition = function (pos, colpos) {
    pos = pos|0;
    colpos = colpos|0;
    var upstart = 0,
        start = this._textarea.value.lastIndexOf("\n", pos - 1),
        distance = pos - start;
    if (start === -1) { return 0; }
    upstart = this._textarea.value.lastIndexOf("\n", start - 1);
    if (colpos >= distance) {
      return Math.min(upstart + colpos + 1, start);
    }
    return Math.min(upstart + distance, start);
  };
  TcTextarea.prototype.getLineDownPosition = function (pos, colpos) {
    pos = pos|0;
    colpos = colpos|0;
    var start = 0,
        downend = 0,
        distance = 0,
        end = this._textarea.value.indexOf("\n", pos);
    if (end === -1) { return this._textarea.value.length; }
    start = this._textarea.value.lastIndexOf("\n", pos - 1);
    distance = pos - start;
    downend = this._textarea.value.indexOf("\n", end + 1);
    if (downend === -1) { downend = this._textarea.value.length; }
    if (colpos >= distance) {
      return Math.min(downend, end + colpos + 1);
    }
    return Math.min(downend, end + distance);
  };
  TcTextarea.prototype.getLineRange = function (pos) {
    pos = pos|0;
    var start = this._textarea.value.lastIndexOf("\n", pos - 1) + 1,
        end = this._textarea.value.indexOf("\n", pos);
    if (end === -1) { return {start: start|0, end: this._textarea.value.length|0}; }
    return {start: start|0, end: end|0};
  };
  TcTextarea.prototype.getCursorColumnPosition = function () { return this.getColumnPosition(this.getCursorPosition()); };
  TcTextarea.prototype.getCursorPreviousGroupPosition = function () { return this.getPreviousGroupPosition(this.getCursorPosition()); };
  TcTextarea.prototype.getCursorNextGroupPosition = function () { return this.getNextGroupPosition(this.getCursorPosition()); };
  TcTextarea.prototype.getCursorLineStartPosition = function () { return this.getLineStartPosition(this.getCursorPosition()); };
  TcTextarea.prototype.getCursorLineEndPosition = function () { return this.getLineEndPosition(this.getCursorPosition()); };
  TcTextarea.prototype.getCursorLineUpPosition = function (colpos) { return this.getLineUpPosition(this.getCursorPosition(), colpos); };
  TcTextarea.prototype.getCursorLineDownPosition = function (colpos) { return this.getLineDownPosition(this.getCursorPosition(), colpos); };
  TcTextarea.prototype.getCursorLineRange = function () { return this.getLineRange(this.getCursorPosition()); };
  TcTextarea.prototype.getCursorLine = function () { var range = this.getCursorLineRange(); return this._textarea.value.slice(range.start, range.end); };

  TcTextarea.prototype.setCursorPosition = function (position, select) {
    var textarea = this._textarea;
    if (textarea.selectionDirection[0] === "f") {
      if (select) {
        if (textarea.selectionStart < position) textarea.setSelectionRange(textarea.selectionStart, position, "forward");
        else textarea.setSelectionRange(position, textarea.selectionStart, "backward");
      } else textarea.setSelectionRange(position, position);
    } else {
      if (select) {
        if (textarea.selectionEnd < position) textarea.setSelectionRange(textarea.selectionEnd, position, "forward");
        else textarea.setSelectionRange(position, textarea.selectionEnd, "backward");
      } else textarea.setSelectionRange(position, position);
    }
  };
  TcTextarea.prototype.moveCursor = function (offset, select) {
    var textarea = this._textarea, tmp = 0;
    if (textarea.selectionDirection[0] === "f") {
      if (select) {
        if (textarea.selectionEnd + offset > textarea.selectionStart) textarea.setSelectionRange(textarea.selectionStart, textarea.selectionEnd + offset, "forward");
        else textarea.setSelectionRange(textarea.selectionEnd + offset, textarea.selectionStart, "backward");
      } else textarea.setSelectionRange(tmp = Math.max(textarea.selectionEnd + offset, 0), tmp);
    } else {
      if (select) {
        if (textarea.selectionStart + offset > textarea.selectionEnd) textarea.setSelectionRange(textarea.selectionEnd, textarea.selectionStart + offset, "forward");
        else textarea.setSelectionRange(textarea.selectionStart + offset, textarea.selectionEnd, "backward");
      } else textarea.setSelectionRange(tmp = Math.max(textarea.selectionStart + offset, 0), tmp);
    }
  };

  TcTextarea.prototype.replaceTextInRange = function (regexp, replacement, start, end, selectionMode) {
    var textarea = this._textarea, match = null;
    start = start|0;
    end = end|0;
    if (typeof regexp === "string") {
      regexp = new RegExp(regexp.replace(/([\$\(\)\*\+\.\?\[\\\]\^])/g, "\\$1"));
    }
    if (start === end) end = textarea.value.length;
    if (regexp.global) {
      this.setRangeText(
        textarea.value.slice(start, end).replace(regexp, replacement),
        start,
        end,
        selectionMode
      );
    } else {
      match = regexp.exec(textarea.value.slice(start, end));
      if (match) {
        this.setRangeText(
          TcTextarea.util.formatMatchReplacement(match, replacement),
          start + match.index,
          start + match.index + match[0].length,
          selectionMode
        );
        //textarea.setSelectionRange(start + match.index, start + match.index + match[0].length);
      }
    }
  };

  TcTextarea.prototype.autocompleteWordAtCursor = function (reverse) {
    // XXX when selecting ??
    var that = this, textarea = this._textarea, vars = this._autocompleteWordVars, cursor = this.getCursorPosition(),
        wordsDict = {}, words, index, firstText, lastText, wordPart, lastWordPart, re;
    function add(word) {
      delete wordsDict[word];
      wordsDict[word] = null;
      return word;
    }

    if (vars && vars.lastPosition === cursor && vars.lastWord === textarea.value.slice(cursor - vars.lastWord.length, cursor) && vars.words) {
      // go to next index
      index = vars.index;
      if (reverse) {
        if (index < vars.words.length - 1) { index += 1; } else { index = 0; }
      } else {
        if (index > 0) { index -= 1; } else { index = vars.words.length - 1; }
      }
      if (vars.lastWord === vars.words[index]) { return false; }
      textarea.removeEventListener("input", this);
      this.setRangeText(vars.words[index], cursor - vars.lastWord.length, cursor, "end");
      vars.lastPosition = cursor - vars.lastWord.length + vars.words[index].length;
      setTimeout(function () { textarea.addEventListener("input", that, {passive: true}); });
      vars.lastWord = vars.words[index];
      vars.index = index;
    } else {
      // store words and go to first index
      firstText = textarea.value.slice(0, cursor).replace(/\w+$/, function (match) { wordPart = match; return ""; });
      if (!wordPart) { return false; }
      lastText = textarea.value.slice(firstText.length).replace(/^\w+/, "");
      re = new RegExp("\\b" + wordPart + "\\w+", "g");
      lastText.replace(re, add);
      firstText.replace(re, add);
      words = Object.keys(wordsDict);
      if (!words.length) { return false; }
      index = reverse ? 0 : words.length - 1;
      lastWordPart = words[index].slice(wordPart.length);
      textarea.removeEventListener("input", this);
      this.setRangeText(lastWordPart, cursor, textarea.value.length - lastText.length, "end")
      cursor = cursor + lastWordPart.length;
      this._autocompleteWordVars = {
        lastPosition: cursor,
        lastWord: wordPart + lastWordPart,
        words: words,
        index: index
      };
      setTimeout(function () { textarea.addEventListener("input", that, {passive: true}); });
    }
    return true;
  }

  // other utils //

  TcTextarea.util = {};

  TcTextarea.util.reverseStringCase = function (text) {
    var s = "", l = text.length, i = 0, b = "";
    for (; i < l; i += 1) {
      b = text[i].toUpperCase();
      if (b !== text[i]) { s += b; }
      else { s += b.toLowerCase(); }
    }
    return s;
  };
  TcTextarea.util.toggleStringCase = function (text) {
    var s = "", l = text.length, i = 0, b = "";
    for (; i < l; i += 1) {
      b = text[i].toUpperCase();
      if (b !== text[i]) {
        s += b;
        for (i += 1; i < l; i += 1) { s += text[i].toUpperCase(); }
        break;
      } else if (b.toLowerCase() !== b) {
        s += b.toLowerCase();
        for (i += 1; i < l; i += 1) { s += text[i].toLowerCase(); }
        break;
      } else {
        s += b;
      }
    }
    return s;
  };
  TcTextarea.util.parsePromptArguments = function (string) {
    // nearly shell like arguments
    var args = [], expectedindex = -1 >>> 1;
    string.replace(/(?:"((?:\\.|[^\\"])*)"|'([^']*)'|([^\\"' \t]+)|(\\.)|([\\"']))/g, function (m, dq, sq, r, bs, q, i) {
      var s = "";
      if (args.length === 0) args.push("");
      if (dq !== undefined) s = dq.replace(/\\"/g, '"');
      else if (sq !== undefined) s = sq;
      else if (r !== undefined) s = r;
      else if (bs !== undefined) s = bs.slice(1, 2);
      else if (q !== undefined) s = q;

      if (i <= expectedindex) args[args.length - 1] += s;
      else args.push(s);
      expectedindex = i + m.length;
    });
    return args;
  };
  TcTextarea.util.parseDialogSearch = function (string, global) {
    var res = /^\/((?:\\.|[^\\\/])*)(?:\/([gimyu]{0,5}))?$/.exec(string);  // this regexp does not handle flag errors!
    if (res !== null) {
      if (global && res[2].indexOf("g") === -1) res[2] += "g";
      try { return new RegExp(res[1], res[2]); } catch (ignore) {}  // only this part checks for flag errors.
    }
    // not a regexp / invalid regexp
    if (string.toLowerCase() !== string) res = "";
    else res = "i";
    if (global) res += "g";
    return new RegExp(string.replace(/([\$\(\)\*\+\.\?\[\\\]\^])/g, "\\$1"), res);
  };
  TcTextarea.util.formatMatchReplacement = function (match, replacement) {
    return replacement.replace(/\$(\$|([1-9])|`|_|&|\+)/g, function (_, s, d) {
      if (d) return match[d];
      switch (s) {
        case "&": return match[0];
        case "$": return "$";
        case "+": return match[match.length - 1];
        case "_": return match.input;
        case "`": return match.input.slice(0, match.index);
      }
    });
  };

  // read only commands //

  TcTextarea.commands.selectForCopyEvent = function (tt) {
    var t = tt._textarea, s = t.selectionStart;
    if (s !== t.selectionEnd) { return; }
    t.setSelectionRange(tt.getCursorLineStartPosition(), tt.getCursorLineEndPosition() + 1);
    setTimeout(function () { t.setSelectionRange(s, s); });
  };

  TcTextarea.commands.goCharLeft = function (tt) {
    var event = tt.handledEvent, t = tt._textarea;
    if (!event.shiftKey && t.selectionStart !== t.selectionEnd) {
      t.setSelectionRange(t.selectionStart, t.selectionStart);
    } else {
      tt.moveCursor(-1, event.shiftKey);
    }
    tt.workaroundScroll();
  };
  TcTextarea.commands.goCharRight = function (tt) {
    var event = tt.handledEvent, t = tt._textarea;
    if (!event.shiftKey && t.selectionStart !== t.selectionEnd) {
      t.setSelectionRange(t.selectionEnd, t.selectionEnd);
    } else {
      tt.moveCursor(1, event.shiftKey);
    }
    tt.workaroundScroll();
  };
  TcTextarea.commands.goGroupRight = function (tt) {
    var event = tt.handledEvent;
    tt.setCursorPosition(tt.getCursorNextGroupPosition(), event.shiftKey);
    tt.workaroundScroll();
  };
  TcTextarea.commands.goGroupLeft = function (tt) {
    var event = tt.handledEvent;
    tt.setCursorPosition(tt.getCursorPreviousGroupPosition(), event.shiftKey);
    tt.workaroundScroll();
  };
  TcTextarea.commands.goLineEnd = function (tt) {
    var event = tt.handledEvent;
    tt.setCursorPosition(tt.getCursorLineEndPosition(), event.shiftKey);
    tt.workaroundScroll();
  };

  TcTextarea.commands.goLineStartSmart = function (tt) {
    var event = tt.handledEvent, start = tt.getCursorLineStartPosition(), tmp = null;
    tmp = /^[ \t]*/.exec(tt.getValue().slice(start));
    tt.setCursorPosition(start + tmp[0].length, event.shiftKey);
    tt.workaroundScroll();
  };
  TcTextarea.commands.goLineStart = function (tt) {
    var event = tt.handledEvent;
    tt.setCursorPosition(tt.getCursorLineStartPosition(), event.shiftKey);
    tt.workaroundScroll();
  };
  TcTextarea.commands.goLineDown = function (tt) {
    var event = tt.handledEvent, t = tt._textarea, colpos = 0, length = 0;
    if (!event.shiftKey && t.selectionStart !== t.selectionEnd) {
      t.setSelectionRange(t.selectionEnd, t.selectionEnd);
    } else {
      colpos = tt.getCursorColumnPosition();
      length = tt.getCursorLine().length;
      if (colpos < length) { tt._commandGoLineState = colpos; }
      else if (tt._commandGoLineState < length) { tt._commandGoLineState = length; }
      tt.setCursorPosition(tt.getCursorLineDownPosition(tt._commandGoLineState), event.shiftKey);
    }
    tt.workaroundScroll();
  };
  TcTextarea.commands.goLineUp = function (tt) {
    var event = tt.handledEvent, t = tt._textarea, colpos = 0, length = 0;
    if (!event.shiftKey && t.selectionStart !== t.selectionEnd) {
      t.setSelectionRange(t.selectionStart, t.selectionStart);
    } else {
      colpos = tt.getCursorColumnPosition();
      length = tt.getCursorLine().length;
      if (colpos < length) { tt._commandGoLineState = colpos; }
      else if (tt._commandGoLineState < length) { tt._commandGoLineState = length; }
      tt.setCursorPosition(tt.getCursorLineUpPosition(tt._commandGoLineState), event.shiftKey);
    }
    tt.workaroundScroll();
  };
  TcTextarea.commands.goDocStart = function (tt) {
    var event = tt.handledEvent;
    tt.setCursorPosition(0, event.shiftKey);
    tt.workaroundScroll();
  };
  TcTextarea.commands.goDocEnd = function (tt) {
    var event = tt.handledEvent;
    tt.setCursorPosition(tt._textarea.value.length, event.shiftKey);
    tt.workaroundScroll();
  };
  TcTextarea.commands.undoSelection = function (tt) {
    var t = tt._textarea;
    if (t.selectionDirection[0] === "f") {
      t.setSelectionRange(t.selectionEnd, t.selectionEnd);
    } else {
      t.setSelectionRange(t.selectionStart, t.selectionStart);
    }
  };
  TcTextarea.commands.reverseSelectionDirection = function (tt) {
    // swap the cursor in the selection
    var t = tt._textarea;
    t.setSelectionRange(t.selectionStart, t.selectionEnd, t.selectionDirection[0] === "f" ? "backward" : "forward");
    tt.workaroundScroll();
  };

  TcTextarea.commands.jumpToLine = function (tt) {
    var t = tt._textarea, event = tt.handledEvent, line = parseInt(prompt("Go to line:"), 10), lines, i, l, chars = 0;
    if (line > 0) {
      lines = t.value.split("\n");
      l = lines.length;
      for (i = 0; i < l; i += 1) {
        if (i !== line - 1) {
          chars += lines[i].length + 1;
        } else {
          tt.setCursorPosition(chars, event.shiftKey);
          tt.workaroundScroll();
          return;
        }
      }
    }
    tt.setCursorPosition(t.value.length, event.shiftKey);
    //t.setSelectionRange(t.value.length, t.value.length);
    tt.workaroundScroll();
  };

  // write commands //

  TcTextarea.commands.selectForCutEvent = function (tt) {
    var t = tt._textarea, s = t.selectionStart;
    if (s !== t.selectionEnd) { return; }
    t.setSelectionRange(tt.getCursorLineStartPosition(), tt.getCursorLineEndPosition() + 1);
    if (tt.isReadOnly()) {
      setTimeout(function () {
        t.setSelectionRange(s, s);
        tt.workaroundScroll();
      });
    }
  };

  TcTextarea.commands.delCharAfter = function (tt) {
    var t = tt.getTextArea(), pos = 0;
    if (tt.isReadOnly()) { return; }
    pos = t.selectionStart;
    if (t.selectionStart !== t.selectionEnd) {
      tt.setRangeText("", t.selectionStart, t.selectionEnd, "start");
    } else {
      tt.setRangeText("", pos, pos + 1, "start");
    }
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.delCharBefore = function (tt) {
    var t = tt.getTextArea(), pos = 0;
    if (tt.isReadOnly()) { return; }
    if (t.selectionStart !== t.selectionEnd) {
      pos = t.selectionStart;
      tt.setRangeText("", t.selectionStart, t.selectionEnd, "start");
    } else {
      pos = t.selectionStart - 1;
      if (pos < 0) { return; }
      tt.setRangeText("", pos, pos + 1, "start");
    }
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.delGroupBefore = function (tt) {
    var t = tt._textarea, pos;
    if (tt.isReadOnly()) { return; }
    if (t.selectionStart !== t.selectionEnd)
      tt.setRangeText("", t.selectionStart, t.selectionEnd, "start");
    else
      tt.setRangeText("", tt.getPreviousWordNlPosition(t.selectionStart), t.selectionStart, "start");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.delGroupAfter = function (tt) {
    var t = tt._textarea, pos = 0, start = 0;
    if (tt.isReadOnly()) { return; }
    if (t.selectionStart !== t.selectionEnd)
      tt.setRangeText("", t.selectionStart, t.selectionEnd, "start");
    else
      tt.setRangeText("", t.selectionStart, tt.getNextWordNlPosition(t.selectionStart), "start");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.deleteLine = function (tt) {
    var t = tt._textarea;
    if (tt.isReadOnly()) { return; }
    tt.setRangeText("", tt.getLineStartPosition(t.selectionStart), tt.getLineEndPosition(t.selectionEnd) + 1, "start");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.insertNewline = function (tt) {
    var t = tt._textarea, pos = 0;
    if (tt.isReadOnly()) { return; }
    pos = t.selectionStart + 1;
    tt.setRangeText("\n", t.selectionStart, t.selectionEnd, "end");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.insertLineBefore = function (tt) {
    var t = tt._textarea, pos = 0;
    if (tt.isReadOnly()) { return; }
    pos = tt.getCursorLineStartPosition();
    tt.setRangeText("\n", pos, pos, "start");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.insertLineAfter = function (tt) {
    var t = tt._textarea, pos = 0;
    if (tt.isReadOnly()) { return; }
    pos = tt.getCursorLineEndPosition();
    tt.setRangeText("\n", pos, pos, "end");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.smartNewline = function (tt) {
    var t = tt._textarea, start = 0, tmp = null;
    if (tt.isReadOnly()) { return; }
    start = t.selectionStart;
    tmp = /([ \t]*)[^\n]*$/.exec(t.value.slice(0, start)) || "";
    if (tmp) { tmp = tmp[1]; }
    tt.setRangeText("\n" + tmp, start, t.selectionEnd, "end");
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.duplicateSelectionOrLine = function (tt) {
    if (tt.isReadOnly()) { return; }
    var t = tt._textarea, s = 0, e = 0, d;
    if (t.selectionStart !== t.selectionEnd) {
      s = t.selectionStart;
      e = t.selectionEnd;
      d = t.selectionDirection;
      tt.setRangeText(t.value.slice(s, e), e, e, "select");
      //t.setSelectionRange(e, e + (e - s), d);
    } else {
      d = t.selectionStart;
      s = tt.getLineStartPosition(d);
      e = tt.getLineEndPosition(d) + 1;
      tt.setRangeText((t.value[e - 1] !== "\n" ? "\n" : "") + t.value.slice(s, e), e, e, "start");
      d = d + (e - s);
      t.setSelectionRange(d, d);
    }
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.moveCharsRight = function (tt) {
    if (tt.isReadOnly()) { return; }
    var t = tt._textarea, s = 0, e = 0, d = "";
    e = t.selectionEnd;
    if (e >= t.value.length) { return; }
    s = t.selectionStart;
    d = t.selectionDirection;
    tt.moveRange(s === e ? s - 1 : s, e, 1);
    t.setSelectionRange(s + 1, e + 1, d);
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.moveCharsLeft = function (tt) {
    if (tt.isReadOnly()) { return; }
    var t = tt._textarea, s = 0, e = 0, d = "";
    s = t.selectionStart;
    if (s < 1) { return; }
    e = t.selectionEnd;
    if (e <= 1) { return; }
    d = t.selectionDirection;
    tt.moveRange(s === e ? s - 1 : s, e, -1);
    t.setSelectionRange(s - 1, e - 1, d);
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.moveLinesUp = function (tt) {
    var t = tt._textarea, d = "", cs = 0, ce = 0, ls = 0, le = 0, cls = 0;
    if (tt.isReadOnly()) { return; }
    cs = t.selectionStart;
    ls = tt.getLineStartPosition(cs);
    cls = tt.getLineStartPosition(ls - 1);
    if (ls === 0) { return; }
    ce = t.selectionEnd;
    le = tt.getLineEndPosition(ce);
    d = t.selectionDirection;
    tt.setRangeText(t.value.slice(ls, le) + t.value.slice(ls - 1, ls) + t.value.slice(cls, ls - 1), cls, le, "start");
    //t.value = t.value.slice(0, cls) + t.value.slice(ls, le) + t.value.slice(ls - 1, ls) + t.value.slice(cls, ls - 1) + t.value.slice(le);
    cls = ls - cls;
    t.setSelectionRange(cs - cls, ce - cls, d);
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.moveLinesDown = function (tt) {
    var t = tt._textarea, d = "", cs = 0, ce = 0, ls = 0, le = 0, cle = 0;
    if (tt.isReadOnly()) { return; }
    ce = t.selectionEnd;
    le = tt.getLineEndPosition(ce);
    cle = tt.getLineEndPosition(le + 1);
    if (le === t.value.length) { return; }
    cs = t.selectionStart;
    ls = tt.getLineStartPosition( cs);
    d = t.selectionDirection;
    tt.setRangeText(t.value.slice(le + 1, cle) + t.value.slice(le, le + 1) + t.value.slice(ls, le), ls, cle, "start");
    //t.value = t.value.slice(0, ls) + t.value.slice(le + 1, cle) + t.value.slice(le, le + 1) + t.value.slice(ls, le) + t.value.slice(cle);
    cle = cle - le;
    t.setSelectionRange(cs + cle, ce + cle, d);
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.reverseCase = function (tt) {
    var t = tt._textarea, s = 0, e = 0;
    if (tt.isReadOnly()) { return; }
    e = t.selectionEnd;
    s = t.selectionStart;
    if (s === e) {
      if (e >= t.value.length) { return; }
      tt.setRangeText(TcTextarea.util.reverseStringCase(t.value.slice(e, e + 1)), e, e + 1, "end");
    } else {
      tt.setRangeText(TcTextarea.util.reverseStringCase(t.value.slice(s, e)), s, e, "select");
    }
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.toggleCase = function (tt) {
    var t = tt._textarea, s = 0, e = 0;
    if (tt.isReadOnly()) { return; }
    e = t.selectionEnd;
    s = t.selectionStart;
    if (s === e) {
      if (e >= t.value.length) { return; }
      tt.setRangeText(TcTextarea.util.toggleStringCase(t.value.slice(e, e + 1)), e, e + 1, "end");
      // XXX capitalize word ?
    } else {
      tt.setRangeText(TcTextarea.util.toggleStringCase(t.value.slice(s, e)), s, e, "select");
    }
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.indentMore = function (tt) {
    // indent lines
    var t = tt._textarea, start = 0, end = 0, linestart = 0, dir = "", replacement = "", offset = 0;
    if (tt.isReadOnly()) { return; }
    if (t.selectionStart !== t.selectionEnd) { offset = 1; }
    start = t.selectionStart;
    linestart = tt.getLineStartPosition(start);
    end = t.selectionEnd;
    dir = t.selectionDirection;
    replacement = t.value.slice(linestart, end - offset).replace(/^/mg, "  ");
    tt.setRangeText(replacement, linestart, end - offset, "start");
    t.setSelectionRange(start + 2, linestart + replacement.length + offset, dir);
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.indentLess = function (tt) {
    // unindent lines
    // bug in "abc\n [ def\n ] ghi" -> "abc\n[def]\nghi" instead of "abc\n[def\n]ghi"
    var t = tt._textarea, start = 0, end = 0, linestart = 0, lineend = 0, dir = "", replaced = "", replacement = "", startoffset = 0, offset = 0;
    if (tt.isReadOnly()) { return; }
    if (t.selectionStart !== t.selectionEnd) { offset = 1; }
    start = t.selectionStart;
    linestart = tt.getLineStartPosition(start);
    end = t.selectionEnd;
    dir = t.selectionDirection;
    lineend = tt.getLineEndPosition(t.selectionEnd - offset);
    replaced = t.value.slice(linestart, lineend);
    replacement = replaced.replace(/^(?:  ?|\t)/mg, "");
    startoffset = replaced.split(/\n/)[0].length - replacement.split(/\n/)[0].length;
    tt.setRangeText(replacement, linestart, lineend, "start");
    t.setSelectionRange(Math.max(start - startoffset, linestart), Math.max(end + replacement.length - replaced.length, linestart), dir);
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
  };
  TcTextarea.commands.removeTrailingSpaces = function (tt) {
    var t = tt._textarea, begin = 0, start = 0, end = 0;
    if (tt.isReadOnly()) { return; }
    if (t.selectionStart !== t.selectionEnd) {  // remove trailing spaces
      // bug when selected is "abc  \ndef  " and selectionEnd is end of line
      start = t.selectionStart;
      end = t.selectionEnd;
      begin = 0;
      tt.setRangeText(t.value.slice(start, end).replace(t.value[end + 1] !== "\n" ? /([ \t]+)(\n)/g : /([ \t]+)(\n|$)/g, function (match, spaces, nl) {
        begin += spaces.length;
        return nl;
      }), start, end, "preserve");
    } else {  // remove spaces at cursor
      begin = t.value.slice(0, t.selectionStart).replace(/[ \t]+$/, "");
      start = begin.length;
      tt.setRangeText("", start, t.value.length - t.value.slice(t.selectionEnd).replace(/^[ \t]+/, "").length, "start")
      //t.value = begin + t.value.slice(t.selectionEnd).replace(/^[ \t]+/, "");
      //t.setSelectionRange(start, start);
    }
    t.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll(t);
  };
  TcTextarea.commands.tcAutocompleteWord = function (tt) {
    if (tt.isReadOnly()) { return; }
    if (tt.autocompleteWordAtCursor()) {
      tt._textarea.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
      tt.workaroundScroll();
    }
  };
  TcTextarea.commands.tcAutocompleteWordReverse = function (tt) {
    if (tt.isReadOnly()) { return; }
    if (tt.autocompleteWordAtCursor(true)) {
      tt._textarea.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
      tt.workaroundScroll();
    }
  };
  TcTextarea.commands.replace = function (tt) {
    if (tt.isReadOnly()) { return; }
    var search = prompt("Replace:", tt.getSelection() || tt.lastSearch || ""), searchre = null, replacement = "", action = null;
    if (search === null) { return; }
    replacement = prompt("With:");
    if (replacement === null) { return; }
    searchre = TcTextarea.util.parseDialogSearch(search);
    action = function (tt) {
      if (tt.isReadOnly()) { return; }
      tt.replaceTextInRange(searchre, replacement, tt._textarea.selectionStart, tt._textarea.value.length, "select");
    };
    action(tt);
    tt._textarea.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
    tt.lastSearch = search;
    tt.lastAction = action;
  };
  TcTextarea.commands.replaceAll = function (tt) {
    if (tt.isReadOnly()) { return; }
    var search = prompt("Replace all:", tt.getSelection() || tt.lastSearch || ""), searchre = null, replacement = "";
    if (search === null) { return; }
    replacement = prompt("With:");
    if (replacement === null) { return; }
    searchre = TcTextarea.util.parseDialogSearch(search, true);
    action = function (tt) {
      if (tt.isReadOnly()) { return; }
      tt.replaceTextInRange(searchre, replacement, tt._textarea.selectionStart, tt._textarea.value.length, "select");
    };
    action(tt);
    tt._textarea.dispatchEvent(new Event("input", {bubbles: true}));  // XXX see possible 'data' property
    tt.workaroundScroll();
    tt.lastSearch = search;
    tt.lastAction = action;
  };

  TcTextarea.commands.repeatAction = function (tt) {
    if (typeof tt.lastAction === "function") {
      tt.lastAction(tt);
    }
  };

  TcTextarea.keyMap.tc = {fallthrough: "default"};

  // read only actions //

  TcTextarea.keyMap.default["Ctrl-S"] = "save";  // commands.save needs to be set
  TcTextarea.keyMap.default["Ctrl-U"] = "undoSelection";
  TcTextarea.keyMap.tc["Ctrl-C"] = "selectForCopyEvent";
  TcTextarea.keyMap.tc["Ctrl-X"] = "selectForCutEvent";
  TcTextarea.keyMap.tc["Alt-H"] = TcTextarea.keyMap.tc["Alt-Shift-H"] = "goCharLeft";
  TcTextarea.keyMap.tc["Alt-L"] = TcTextarea.keyMap.tc["Alt-Shift-L"] = "goCharRight";
  TcTextarea.keyMap.tc["Alt-B"] = TcTextarea.keyMap.tc["Alt-Shift-B"] = "goGroupLeft";
  TcTextarea.keyMap.tc["Alt-E"] = TcTextarea.keyMap.tc["Alt-Shift-E"] = "goGroupRight";
  TcTextarea.keyMap.tc["Alt-K"] = TcTextarea.keyMap.tc["Alt-Shift-K"] = "goLineUp";
  TcTextarea.keyMap.tc["Alt-J"] = TcTextarea.keyMap.tc["Alt-Shift-J"] = "goLineDown";
  TcTextarea.keyMap.tc["Alt-I"] = TcTextarea.keyMap.tc["Alt-Shift-I"] = "goLineStartSmart";
  TcTextarea.keyMap.tc["Alt-0"] = TcTextarea.keyMap.tc["Alt-Shift-0"] = "goLineStart";
  TcTextarea.keyMap.tc["Alt-Z"] = TcTextarea.keyMap.tc["Alt-Shift-Z"] = "goLineStart";
  TcTextarea.keyMap.tc["Alt-A"] = TcTextarea.keyMap.tc["Alt-Shift-A"] = "goLineEnd";
  TcTextarea.keyMap.tc["Alt-Shift-<"] = TcTextarea.keyMap.tc["Alt-Shift-?"] = TcTextarea.keyMap.tc["Alt-,"] = "goDocStart";
  TcTextarea.keyMap.tc["Alt-Shift->"] = TcTextarea.keyMap.tc["Alt-Shift-."] = TcTextarea.keyMap.tc["Alt-."] = TcTextarea.keyMap.tc["Alt-;"] = "goDocEnd";
  TcTextarea.keyMap.tc["Alt-Shift-W"] = "reverseSelectionDirection";
  TcTextarea.keyMap.tc["Alt-Shift-G"] = TcTextarea.keyMap.tc["Alt-G"] = "jumpToLine";

  // write actions //

  TcTextarea.keyMap.default["Ctrl-D"] = "deleteLine";
  TcTextarea.keyMap.default["Ctrl-]"] = "indentMore";
  TcTextarea.keyMap.default["Ctrl-["] = "indentLess";
  TcTextarea.keyMap.default["Ctrl-Shift-F"] = "replace";
  TcTextarea.keyMap.default["Ctrl-Shift-R"] = "replaceAll";
  TcTextarea.keyMap.tc["Ctrl-H"] = "delCharBefore";
  TcTextarea.keyMap.tc["Alt-Shift-X"] = "delCharBefore";
  TcTextarea.keyMap.tc["Ctrl-D"] = "delCharAfter";
  TcTextarea.keyMap.tc["Alt-X"] = "delCharAfter";
  TcTextarea.keyMap.tc["Alt-Backspace"] = "delCharAfter";
  TcTextarea.keyMap.tc["Alt-S"] = "delGroupBefore";
  TcTextarea.keyMap.tc["Alt-D"] = "delGroupAfter";
  TcTextarea.keyMap.tc["Alt-Shift-D"] = "deleteLine";
  TcTextarea.keyMap.tc["Alt-M"] = "insertNewline";
  TcTextarea.keyMap.tc["Alt-Shift-O"] = "insertLineBefore";
  TcTextarea.keyMap.tc["Alt-O"] = "insertLineAfter";
  TcTextarea.keyMap.tc["Alt-Enter"] = "smartNewline";
  TcTextarea.keyMap.tc["Alt-Y"] = "duplicateSelectionOrLine";
  TcTextarea.keyMap.tc["Alt-T"] = "moveCharsRight";
  TcTextarea.keyMap.tc["Alt-Shift-T"] = "moveCharsLeft";
  TcTextarea.keyMap.tc["Ctrl-ArrowUp"] = "moveLinesUp";
  TcTextarea.keyMap.tc["Ctrl-ArrowDown"] = "moveLinesDown";
  TcTextarea.keyMap.tc["Alt-C"] = "reverseCase";
  TcTextarea.keyMap.tc["Alt-Shift-C"] = "toggleCase";
  TcTextarea.keyMap.tc["Alt-Space"] = "tcAutocompleteWord";
  TcTextarea.keyMap.tc["Alt-P"] = "tcAutocompleteWord";
  TcTextarea.keyMap.tc["Alt-Shift-Space"] = "tcAutocompleteWordReverse";
  TcTextarea.keyMap.tc["Alt-Shift-P"] = "tcAutocompleteWordReverse";
  //TcTextarea.keyMap.tc["Alt-#"] = "removeTrailingSpaces";

  TcTextarea.keyMap.tc["Alt-R"] = "repeatAction";

  TcTextarea.toScript = function () { return "(" + script.toString() + "())"; };
  return TcTextarea;

}());
