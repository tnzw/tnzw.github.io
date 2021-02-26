#!/bin/sh
set -e
cd "$(dirname "$0")"
{
  cat lib/codemirror.js
  cat mode/clike/clike.js
  cat mode/css/css.js
  cat mode/diff/diff.js
  cat mode/go/go.js
  cat mode/htmlmixed/htmlmixed.js
  cat mode/javascript/javascript.js
  cat mode/lua/lua.js
  cat mode/markdown/markdown.js
  cat mode/php/php.js
  cat mode/python/python.js
  cat mode/shell/shell.js
  cat mode/sql/sql.js
  cat mode/xml/xml.js
  cat addon/dialog/*.js
  cat addon/display/fullscreen.js
  cat addon/display/autorefresh.js
  cat addon/edit/*.js
  cat addon/scroll/*.js
  cat addon/search/*.js
  cat keymap/*.js
} > bundle.js
{
  cat lib/codemirror.css
  cat theme/*.css
  cat addon/dialog/*.css
  cat addon/display/*.css
  cat addon/scroll/*.css
  cat addon/search/*.css
} > bundle.css
