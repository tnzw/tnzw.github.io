/*jslint indent: 2 */
(function (root) {
  "use strict";

  /*
   A stateless keymap that mix some emacs and vim shortcuts
   mostly thank to the Alt button.
  */

  /*! tc-codemirror-keymap.js Version 20190405

      Copyright (c) 2015-2019 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  /*jslint vars: true */

  var CodeMirror = root.CodeMirror;

  function update(object1, object2) {
    /*jslint forin: true */
    var key;
    for (key in object2) {
      object1[key] = object2[key];
    }
    return object1;
  }

  function defaults(object1, object2) {
    /*jslint forin: true */
    var key;
    for (key in object2) {
      if (object1[key] === undefined) {
        object1[key] = object2[key];
      }
    }
    return object1;
  }

//   function addNTimes(toAdd, n) {
//     var i, res;
//     if (typeof toAdd === "string") {
//       res = "";
//     } else if (typeof toAdd === "number") {
//       res = 0;
//     }
//     for (i = 0; i < n; i += 1) {
//       res += toAdd;
//     }
//     return res;
//   }
//
//   function operateOnLine(cm, op) {
//     var start = defaults({"ch": 0}, cm.getCursor()), end = defaults({}, start);
//     end.line += 1;
//     cm.replaceRange(op(cm.getRange(start, end)), start, end);
//     cm.setCursor(end);
//   }

  // Vocabulary:
  // - Right: from the cursor, match the next on the document, until the end of document
  // - After: from the cursor, match the next on the line, until the end of line. If cursor is on eol, then match also on the next line
  // - Left: from the cursor, match the previous on the document, until the beginning of document
  // - Before: from the cursor, match the previous on the line, until the beginning of line. If cursor is on bol, then match also on the previous line

  function operateUntilWordAfter(cm, op) {
    var start = cm.getCursor(), end = cm.findPosH(start, 1, "word");
    cm.replaceRange(op(cm.getRange(start, end)), start, end);
    cm.setCursor(end);
  }

  function operateOnCharAfter(cm, op) {
    var start = cm.getCursor(), end = cm.findPosH(start, 1, "char");
    cm.replaceRange(op(cm.getRange(start, end)), start, end);
    cm.setCursor(end);
  }

  function capitalize(string) {
    return string.replace(/\w+/g, function (word) {
      return word.slice(0, 1).toUpperCase() + word.slice(1).toLowerCase();
    });
  }

  function reverseCase(string) {
    var i, l, str = "", chr;
    for (i = 0, l = string.length; i < l; i += 1) {
      chr = string[i].toUpperCase();
      if (chr !== string[i]) {
        str += chr;
        continue;
      }
      chr = string[i].toLowerCase();
      str += chr;
    }
    return str;
  }

  function setOrUnsetMark(cm) {
    cm.setCursor(cm.getCursor());
    cm.setExtending(!cm.getExtending());
    function setExtendingToFalse() {
      cm.off("change", setExtendingToFalse);
      cm.setExtending(false);
    }
    cm.on("change", setExtendingToFalse);
  }

  function convertSelectionToSquareSelection(cm) {
    var anchor = cm.getCursor("from"), head = cm.getCursor("to"), leftCh = (anchor.ch < head.ch ? anchor.ch : head.ch), i;
    cm.setSelection(anchor, {line: anchor.line, ch: head.ch});
    if (anchor.line < head.line) {
      for (i = anchor.line + 1; i <= head.line; i += 1) {
        if (cm.getLine(i).length >= leftCh) {
          cm.addSelection({line: i, ch: anchor.ch}, {line: i, ch: head.ch});
        }
      }
    } else {
      for (i = anchor.line - 1; i >= head.line; i -= 1) {
        if (cm.getLine(i).length >= leftCh) {
          cm.addSelection({line: i, ch: anchor.ch}, {line: i, ch: head.ch});
        }
      }
    }
    //cm.setExtending(false);
  }
  CodeMirror.commands.tcConvertSelectionToSquareSelection = convertSelectionToSquareSelection;

  function clearMark(cm) {
    cm.setExtending(false);
    cm.setCursor(cm.getCursor());
  }

  // TODO moveBlockOrLineUp
  function moveLineUp(cm) {
    var cursor = cm.getCursor(), lineUp, lineDown;
    lineUp = cm.getRange({"line": cursor.line - 1, "ch": 0}, {"line": cursor.line, "ch": 0});
    if (lineUp === "") { return; }
    lineDown = cm.getRange({"line": cursor.line, "ch": 0}, {"line": cursor.line + 1, "ch": 0});
    if (lineDown[lineDown.length - 1] !== "\n") {
      lineUp = lineUp.slice(0, -1);
      lineDown += "\n";
    }
    cm.replaceRange(lineDown + lineUp, {"line": cursor.line - 1, "ch": 0}, {"line": cursor.line + 1, "ch": 0});
    cm.setCursor({"line": cursor.line - 1, "ch": cursor.ch});
  }

  // TODO moveBlockOrLineDown
  function moveLineDown(cm) {
    var cursor = cm.getCursor(), lineUp, lineDown;
    lineUp = cm.getRange({"line": cursor.line, "ch": 0}, {"line": cursor.line + 1, "ch": 0});
    if (lineUp[lineUp.length - 1] !== "\n") { return; }
    lineDown = cm.getRange({"line": cursor.line + 1, "ch": 0}, {"line": cursor.line + 2, "ch": 0});
    if (lineDown[lineDown.length - 1] !== "\n") {
      lineUp = lineUp.slice(0, -1);
      lineDown += "\n";
    }
    cm.replaceRange(lineDown + lineUp, {"line": cursor.line, "ch": 0}, {"line": cursor.line + 2, "ch": 0});
    cm.setCursor({"line": cursor.line + 1, "ch": cursor.ch});
  }

  function transposeWords(cm) {
    // TODO does not work with "  function transposeWords(cm) {" with cursor between "transposeWords" and "cm", and also between "cm" and the end of the line
    var wordOneStart, wordOneEnd, wordTwoStart, wordTwoEnd, wordOne, wordTwo, offset;
    wordOneStart = cm.findPosH(cm.getCursor(), -1, "word");
    wordOneEnd = cm.findPosH(wordOneStart, 1, "word");
    wordTwoEnd = cm.findPosH(wordOneEnd, 1, "word");
    wordTwoStart = cm.findPosH(wordTwoEnd, -1, "word");
    wordOne = cm.getRange(wordOneStart, wordOneEnd);
    wordTwo = cm.getRange(wordTwoStart, wordTwoEnd);
    console.log(wordOne);
    console.log(wordTwo);
    offset = wordTwo.length - wordOne.length;
    cm.replaceRange(wordTwo, wordOneStart, wordOneEnd);
    cm.replaceRange(wordOne, cm.findPosH(wordTwoStart, offset, "char"), cm.findPosH(wordTwoEnd, offset, "char"));
    cm.setCursor(wordTwoEnd);
  }

  function removeSpacesAtCursor(cm) {
    if (cm.getOption("readOnly")) { return; }
    var cursor, col;
    while (true) {
      cursor = cm.getCursor();
      col = cm.findPosH(cursor, -1, "column");
      if (/\s/.test(cm.getRange(col, cursor))) {
        cm.replaceRange("", col, cursor);
      } else {
        break;
      }
    }
    while (true) {
      cursor = cm.getCursor();
      col = cm.findPosH(cursor, 1, "column");
      if (/\s/.test(cm.getRange(cursor, col))) {
        cm.replaceRange("", cursor, col);
      } else {
        break;
      }
    }
  }
  CodeMirror.commands.tcRemoveSpacesAtCursor = removeSpacesAtCursor;

  function autocompleteWordOnChangeListener(cm) {
    cm.off("change", autocompleteWordOnChangeListener);
    delete cm.tcAutocompleteWordVars;
  }
  function autocompleteWord(cm, reverse) {
    var vars = cm.tcAutocompleteWordVars, cursor = cm.getCursor(), wordsDict = {}, words, index, firstText, lastText, wordPart, re;
    function add(word) {
      delete wordsDict[word];
      wordsDict[word] = null;
      return word;
    }

    if (vars && vars.location && vars.location.line === cursor.line && vars.location.ch === cursor.ch && vars.words && cm.getLine(cursor.line).slice(0, cursor.ch).endsWith(vars.words[vars.index || 0])) {
      // go to next index
      index = vars.index;
      if (reverse) {
        if (index < vars.words.length - 1) { index += 1; } else { index = 0; }
      } else {
        if (index > 0) { index -= 1; } else { index = vars.words.length - 1; }
      }
      cm.off("change", autocompleteWordOnChangeListener);
      cm.replaceRange(vars.words[index], {line: cursor.line, ch: cursor.ch - vars.words[vars.index].length}, cursor);
      vars.location = {line: cursor.line, ch: cursor.ch - vars.words[vars.index].length + vars.words[index].length};
      vars.index = index;
      cm.on("change", autocompleteWordOnChangeListener);
    } else {
      // store words and go to first index
      firstText = cm.getRange({"line": 0, "ch": 0}, cursor).replace(/\w+$/, function (match) { wordPart = match; return ""; });
      if (!wordPart) { return; }
      lastText = cm.getValue().slice(firstText.length).replace(/^\w+/, "");
      re = new RegExp("\\b" + wordPart + "\\w+", "g");
      lastText.replace(re, add);
      firstText.replace(re, add);
      words = Object.keys(wordsDict);
      if (!words.length) { return; }
      if (reverse) {
        index = 0;
      } else {
        index = words.length - 1;
      }
      wordPart = words[index].slice(wordPart.length);
      cm.off("change", autocompleteWordOnChangeListener);
      cm.replaceRange(wordPart, cursor, cursor);
      cursor.ch += wordPart.length;
      cm.tcAutocompleteWordVars = {
        location: cursor,
        words: words,
        index: index
      };
      cm.on("change", autocompleteWordOnChangeListener);
    }
  }
  CodeMirror.commands.tcAutocompleteWord = autocompleteWord;
  CodeMirror.commands.tcAutocompleteWordReverse = function (cm) { return autocompleteWord(cm, true); };

  function insertNewline(cm) { cm.replaceSelection("\n"); }
  CodeMirror.commands.tcInsertNewline = insertNewline;
  function doNothing() { return; }
  CodeMirror.commands.tcDoNothing = doNothing;

  // keymap samples emacs-Ctrl-X {"auto": "emacs", "nofallthrough": true, "disableInput": true}
  //                emacs-Ctrl-Q {"auto": "emacs", "nofallthrough": true}

  // CodeMirror.keyMap.tc = updateObject({}, CodeMirror.keyMap["default"]);
  CodeMirror.keyMap.tc = {"fallthrough": "default"};
  CodeMirror.keyMap.tc.Enter = insertNewline;
  CodeMirror.keyMap.tc.Tab = "insertSoftTab";
  CodeMirror.keyMap.tc.F3 = "findNext";

  CodeMirror.keyMap.tc["Alt-A"] = "goLineEnd";
  CodeMirror.keyMap.tc["Alt-B"] = "goGroupLeft";
  CodeMirror.keyMap.tc["Alt-C"] = function (cm) {
    operateOnCharAfter(cm, reverseCase);
  };
  CodeMirror.keyMap.tc["Alt-D"] = "delWordAfter"; // "duplicateLine";
  CodeMirror.keyMap.tc["Alt-E"] = "goGroupRight";
  CodeMirror.keyMap.tc["Alt-F"] = doNothing;
  CodeMirror.keyMap.tc["Alt-H"] = "goCharLeft"; // "goColumnLeft";
  CodeMirror.keyMap.tc["Alt-I"] = "indentAuto";
  CodeMirror.keyMap.tc["Alt-J"] = "goLineDown";
  CodeMirror.keyMap.tc["Alt-K"] = "goLineUp";
  CodeMirror.keyMap.tc["Alt-L"] = "goCharRight"; // "goColumnRight";
  CodeMirror.keyMap.tc["Alt-M"] = insertNewline; // "goLineStartSmart";
  CodeMirror.keyMap.tc["Alt-N"] = "findNext";
  CodeMirror.keyMap.tc["Alt-O"] = function (cm) {
    cm.execCommand("goLineEnd");
    cm.replaceSelection("\n");
  };
  CodeMirror.keyMap.tc["Alt-P"] = doNothing; // TODO searchPrevious
  // CodeMirror.keyMap.tc["Alt-Q"] = undefined;
  CodeMirror.keyMap.tc["Alt-R"] = "replace";
  CodeMirror.keyMap.tc["Alt-S"] = "delWordBefore";
  CodeMirror.keyMap.tc["Alt-T"] = "transposeChars";
  CodeMirror.keyMap.tc["Alt-U"] = "undo";
  CodeMirror.keyMap.tc["Alt-V"] = setOrUnsetMark;
  CodeMirror.keyMap.tc["Alt-W"] = "goWordRight";
  CodeMirror.keyMap.tc["Alt-X"] = "delCharAfter";
  CodeMirror.keyMap.tc["Alt-Y"] = "duplicateLine";
  CodeMirror.keyMap.tc["Alt-Z"] = "goLineStart";
  CodeMirror.keyMap.tc["Alt-0"] = "goLineStart";
  CodeMirror.keyMap.tc["Alt-/"] = "find";
  CodeMirror.keyMap.tc["Alt-\\"] = "tcRemoveSpacesAtCursor";
  CodeMirror.keyMap.tc["Alt-#"] = "tcRemoveSpacesAtCursor";
  CodeMirror.keyMap.tc["Alt--"] = "tcAutocompleteWord";
  CodeMirror.keyMap.tc["Alt-,"] = "goDocStart";
  CodeMirror.keyMap.tc["Alt-."] = "goDocEnd";
  CodeMirror.keyMap.tc["Alt-;"] = "goDocEnd";
  CodeMirror.keyMap.tc["Alt-Up"] = "goPageUp"; // (NO OTHER CHOICE on chromebooks)
  CodeMirror.keyMap.tc["Alt-Down"] = "goPageDown"; // (NO OTHER CHOICE on chromebooks)
  CodeMirror.keyMap.tc["Alt-Space"] = "tcAutocompleteWord"; // (unreachable on Windows)
  CodeMirror.keyMap.tc["Alt-Backspace"] = "delCharAfter"; // (NO OTHER CHOICE on chromebooks)
  CodeMirror.keyMap.tc["Alt-Enter"] = function (cm) {
    cm.execCommand("tcRemoveSpacesAtCursor");
    cm.execCommand("newlineAndIndent");
  };

  // CodeMirror.keyMap.tc["Ctrl-A"] = undefined;
  CodeMirror.keyMap.tc["Ctrl-B"] = doNothing;
  // CodeMirror.keyMap.tc["Ctrl-C"] = undefined;
  CodeMirror.keyMap.tc["Ctrl-D"] = "delCharAfter";
  // CodeMirror.keyMap.tc["Ctrl-E"] = undefined;
  // CodeMirror.keyMap.tc["Ctrl-F"] = undefined;
  // CodeMirror.keyMap.tc["Ctrl-G"] = undefined;
  CodeMirror.keyMap.tc["Ctrl-H"] = "delCharBefore";
  CodeMirror.keyMap.tc["Ctrl-I"] = "insertTab";
  CodeMirror.keyMap.tc["Ctrl-J"] = insertNewline;
  // CodeMirror.keyMap.tc["Ctrl-K"] = "goLineUp";
  // CodeMirror.keyMap.tc["Ctrl-L"] = "goCharRight";
  CodeMirror.keyMap.tc["Ctrl-M"] = insertNewline;
  // CodeMirror.keyMap.tc["Ctrl-N"] = undefined; // (browser new window NO OTHER CHOICE)
  // CodeMirror.keyMap.tc["Ctrl-O"] = undefined;
  CodeMirror.keyMap.tc["Ctrl-P"] = doNothing;
  // CodeMirror.keyMap.tc["Ctrl-Q"] = undefined;
  CodeMirror.keyMap.tc["Ctrl-R"] = "redo"; // (browser reload page)
  CodeMirror.keyMap.tc["Ctrl-S"] = "save";
  // CodeMirror.keyMap.tc["Ctrl-T"] = undefined; // (browser new tab)
  // CodeMirror.keyMap.tc["Ctrl-U"] = "undo";
  // CodeMirror.keyMap.tc["Ctrl-V"] = undefined;
  // CodeMirror.keyMap.tc["Ctrl-W"] = undefined; // (browser close window NO OTHER CHOICE)
  // CodeMirror.keyMap.tc["Ctrl-X"] = "delCharAfter";
  // CodeMirror.keyMap.tc["Ctrl-Y"] = undefined;
  // CodeMirror.keyMap.tc["Ctrl-Z"] = undefined;
  CodeMirror.keyMap.tc["Ctrl-Up"] = moveLineUp;
  CodeMirror.keyMap.tc["Ctrl-Down"] = moveLineDown;
  // CodeMirror.keyMap.tc["Ctrl-Backspace"] = undefined; // (browser delWordBefore)

  CodeMirror.keyMap.tc["Shift-Tab"] = "insertSoftTab"; // TODO ?
  CodeMirror.keyMap.tc["Shift-F3"] = "findPrev";

  // CodeMirror.keyMap.tc["Shift-Alt-A"] = "goLineEnd";
  // CodeMirror.keyMap.tc["Shift-Alt-B"] = undefined;
  CodeMirror.keyMap.tc["Shift-Alt-C"] = function (cm) {
    operateUntilWordAfter(cm, capitalize);
  };
  CodeMirror.keyMap.tc["Shift-Alt-D"] = "deleteLine";
  // CodeMirror.keyMap.tc["Shift-Alt-E"] = "transposeChars";
  CodeMirror.keyMap.tc["Shift-Alt-F"] = doNothing; // (firefox [File] shortcut)
  CodeMirror.keyMap.tc["Shift-Alt-G"] = doNothing;
  // CodeMirror.keyMap.tc["Shift-Alt-H"] = "goCharLeft";
  CodeMirror.keyMap.tc["Shift-Alt-I"] = "goLineStartSmart";
  // CodeMirror.keyMap.tc["Shift-Alt-J"] = "goLineDown";
  // CodeMirror.keyMap.tc["Shift-Alt-K"] = "goLineUp";
  // CodeMirror.keyMap.tc["Shift-Alt-L"] = "goCharRight";
  // CodeMirror.keyMap.tc["Shift-Alt-M"] = undefined;
  CodeMirror.keyMap.tc["Shift-Alt-N"] = "findPrev";  // TODO ? (chromeos open message center NO OTHER CHOICE)
  CodeMirror.keyMap.tc["Shift-Alt-O"] = function (cm) {
    cm.execCommand("goLineStart");
    cm.replaceSelection("\n");
    cm.execCommand("goCharLeft");
  };
  // CodeMirror.keyMap.tc["Shift-Alt-P"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Alt-Q"] = undefined;
  CodeMirror.keyMap.tc["Shift-Alt-R"] = "replaceAll";
  CodeMirror.keyMap.tc["Shift-Alt-S"] = "delCharAfter";
  CodeMirror.keyMap.tc["Shift-Alt-T"] = doNothing; // TODO transposeWords (firefox [Tools] shortcut)
  CodeMirror.keyMap.tc["Shift-Alt-U"] = "redo";
  CodeMirror.keyMap.tc["Shift-Alt-V"] = "tcConvertSelectionToSquareSelection"; // (firefox [View] shortcut)
  // CodeMirror.keyMap.tc["Shift-Alt-W"] = undefined;
  CodeMirror.keyMap.tc["Shift-Alt-X"] = "delCharBefore";
  // CodeMirror.keyMap.tc["Shift-Alt-Y"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Alt-Z"] = undefined;
  CodeMirror.keyMap.tc["Shift-Alt-3"] = doNothing; // TODO searchThisWordPrevious
  CodeMirror.keyMap.tc["Shift-Alt-4"] = "goLineEnd";
  CodeMirror.keyMap.tc["Shift-Alt-8"] = doNothing; // TODO searchThisWordNext
  //CodeMirror.keyMap.tc["Shift-Alt-,"] = "goDocStart";
  //CodeMirror.keyMap.tc["Shift-Alt-."] = "goDocEnd";
  //CodeMirror.keyMap.tc["Shift-Alt-<"] = "goDocStart"; // doesn't work
  //CodeMirror.keyMap.tc["Shift-Alt->"] = "goDocEnd"; // doesn't work
  CodeMirror.keyMap.tc["Shift-Alt-["] = "indentLess";
  CodeMirror.keyMap.tc["Shift-Alt-]"] = "indentMore";
  CodeMirror.keyMap.tc["Shift-Alt--"] = "tcAutocompleteWordReverse";
  CodeMirror.keyMap.tc["Shift-Alt-Space"] = "tcAutocompleteWordReverse";
  CodeMirror.keyMap.tc["Shift-Alt-Backspace"] = "delWordAfter";

  // CodeMirror.keyMap.tc["Shift-Ctrl-A"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-B"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-C"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-D"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-E"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-F"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-G"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-H"] = "goCharLeft";
  // CodeMirror.keyMap.tc["Shift-Ctrl-I"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-J"] = "goLineDown";
  // CodeMirror.keyMap.tc["Shift-Ctrl-K"] = "goLineUp";
  // CodeMirror.keyMap.tc["Shift-Ctrl-L"] = "goCharRight";
  // CodeMirror.keyMap.tc["Shift-Ctrl-M"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-O"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-P"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-Q"] = undefined;
  CodeMirror.keyMap.tc["Shift-Ctrl-R"] = doNothing; // (browser reload page without cache)
  // CodeMirror.keyMap.tc["Shift-Ctrl-S"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-T"] = undefined; // (browser open recently closed tab)
  // CodeMirror.keyMap.tc["Shift-Ctrl-U"] = "undo";
  // CodeMirror.keyMap.tc["Shift-Ctrl-V"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-W"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-X"] = "delCharAfter";
  // CodeMirror.keyMap.tc["Shift-Ctrl-Y"] = undefined;
  // CodeMirror.keyMap.tc["Shift-Ctrl-Z"] = undefined;
  CodeMirror.keyMap.tc["Shift-Ctrl--"] = "undo";

}(this));
