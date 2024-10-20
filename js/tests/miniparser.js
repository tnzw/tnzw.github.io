/*jslint indent: 2 */
(function script() {
  "use strict";

  /*! miniparser.js version 0.1.0

      Copyright (c) 2023 <tnzw@github.triton.ovh>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  if (typeof loadVarScripts === "function" &&
      !script.noImport) {
    script.noImport = true;
    console.log("loading miniparser.js dependencies");
    return loadVarScripts(
      {baseUrl: "../var/"},
      "miniparser",
    ).then(script, function (e) { console.error(e); });
  }
  console.log("running miniparser.js tests");

  /*jslint vars: true */
  var info = function () { console.info.apply(console, arguments); };
  var error = function () { console.error.apply(console, arguments); };
  // function test(name, timeout, expected, testFn) {
    // var res = [], timer;
    // function end() {
      // if (timer === undefined) return error("test `" + name + "`, `end` called twice");
      // timer = clearTimeout(timer);  // timer should be set to undefined
      // if (JSON.stringify(res) !== JSON.stringify(expected)) {
        // error("test `" + name + "`, result `" + JSON.stringify(res) + "` !== `" + JSON.stringify(expected) + "` expected");
      // }
    // }
    // timer = setTimeout(function () {
      // try { if (typeof end.onbeforetimeout === "function") end.onbeforetimeout(); }
      // catch (e) { error("test: " + name + ", error on before timeout ! `" + e + "`"); }
      // if (timer === undefined) return;  // it has ended in before timeout
      // error("test `" + name + "`, timeout ! result `" + JSON.stringify(res) + "` <-> `" + JSON.stringify(expected) + "` expected");
    // }, timeout);
    // setTimeout(function () {
      // try { testFn(res, end); }
      // catch (e) { error("test `" + name + "`, error ! result `" + e + "`"); }
    // });
  // }

  // function nativeSoftDecodeBase64String(text) {
    // return Array.from(atob(text)).map(function (c) { return c.charCodeAt(0); });
  // }
  // function nativeEncodeBase64ToString(bytes) {
    // return btoa(String.fromCharCode.apply(String, bytes));
  // }

  // function bytesToJs(bytes) {
    // return "[" + bytes.map(function (v) { return "0x" + v.toString(16); }).join(",") + "]";
  // }
  // function randBytes(length) {
    // var r = [], i = 0;
    // while (i++ < length) r.push(parseInt(Math.random() * 256, 10));
    // return r;
  // }

  // function testSoftDecodeBase64String(text, exp) {
    // if (!exp)
      // try { exp = nativeSoftDecodeBase64String(text); } catch (e) { exp = [e.message]; }
    // test("base64 " + text, 300, exp, function (res, end) {
      // try { exp = decodeBase64ToBytes(text); } catch (e) { exp = [e.message]; }
      // res.push.apply(res, exp);
      // end();
    // });
  // }
  // function testEncodeBase64ToString(bytes, exp) {
    // if (!exp)
      // try { exp = [nativeEncodeBase64ToString(bytes)]; } catch (e) { exp = [e.message]; }
    // test("base64 " + bytesToJs(bytes), 300, exp, function (res, end) {
      // try { exp = [encodeBytesToBase64(bytes)]; } catch (e) { exp = [e.message]; }
      // res.push.apply(res, exp);
      // end();
    // });
  // }

  var NAME = '';
  function miniparser__test_comp_matches(comp, string, pos, endpos, expected) {
    var result = [...comp(string, pos, endpos)];
    if (JSON.stringify(result) !== JSON.stringify(expected))
      throw new Error(`${NAME}: ${JSON.stringify(result, null, 2)} !== ${JSON.stringify(expected, null, 2)}`);
  }
  function miniparser__test_comp_values(comp, string, pos, endpos, expected) {
    var result = [...comp(string, pos, endpos)].map(m => miniparser.match_getvalue(m));
    if (JSON.stringify(result) !== JSON.stringify(expected))
      throw new Error(`${NAME}: ${JSON.stringify(result)} !== ${JSON.stringify(expected)}`);
  }

// def miniparser__test_comp_values(comp, string, pos, endpos, expected):
  // result = [miniparser.match_getvalue(m) for m in comp(string, pos, endpos)]
  // assert_equal(result, expected)


  //////////////////////////////////////////////
  // miniparser tests
  setTimeout(string => { NAME = 'test_miniparser__string';
    string = miniparser.string;
    miniparser__test_comp_matches(string('abc'), 'abce', 0, 4, [['abce', 0, 4, 0, 3]]);  // /abc/ on 'abce'
    miniparser__test_comp_matches(string('abc'), 'eabce', 1, 5, [['eabce', 1, 5, 1, 4]]);  // /abc/ on 'eabce'
  });

  setTimeout(istring => { NAME = 'test_miniparser__istring';
    istring = miniparser.istring;
    miniparser__test_comp_matches(istring('abC'), 'aBce', 0, 4, [['aBce', 0, 4, 0, 3]]);  // /abC/i on 'aBce'
    miniparser__test_comp_matches(istring('aBc'), 'eAbce', 1, 5, [['eAbce', 1, 5, 1, 4]]);  // /aBc/i on 'eAbce'
  });

  setTimeout((string, some) => { NAME = 'test_miniparser__some';
    string = miniparser.string;
    some = miniparser.some;
    miniparser__test_comp_values(some(string('a')), 'aaa', 0, 3, [[...'aaa'], [...'aa'], ['a'], []]);  // /a*/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 1), 'aaa', 0, 3, [['a']]);  // /a{1}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 2), 'aaa', 0, 3, [[...'aa']]);  // /a{2}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 3), 'aaa', 0, 3, [[...'aaa']]);  // /a{3}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 4), 'aaa', 0, 3, []);  // /a{4}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, null), 'aaa', 0, 3, [[...'aaa'], [...'aa'], ['a'], []]);  // /a{0,}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, undefined), 'aaa', 0, 3, [[...'aaa'], [...'aa'], ['a'], []]);
    miniparser__test_comp_values(some(string('a'), 1, null), 'aaa', 0, 3, [[...'aaa'], [...'aa'], ['a']]);  // /a{1,}/ or /a+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 2, null), 'aaa', 0, 3, [[...'aaa'], [...'aa']]);  // /a{2,}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 3, null), 'aaa', 0, 3, [[...'aaa']]);  // /a{3,}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 4, null), 'aaa', 0, 3, []);  // /a{4,}/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, 3), 'aaaa', 0, 4, [[...'aaa'], [...'aa'], ['a'], []]);  // /a{0,3}/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 1, 3), 'aaaa', 0, 4, [[...'aaa'], [...'aa'], ['a']]);  // /a{1,3}/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 2, 3), 'aaaa', 0, 4, [[...'aaa'], [...'aa']]);  // /a{2,3}/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 3, 3), 'aaaa', 0, 4, [[...'aaa']]);  // /a{3,3}/ on 'aaaa'

    miniparser__test_comp_values(some(string('a'), {lazy: true}), 'aaa', 0, 3, [[], ['a'], [...'aa'], [...'aaa']]);  // /a*?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 1, {lazy: true}), 'aaa', 0, 3, [['a']]);  // /a{1}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 2, {lazy: true}), 'aaa', 0, 3, [[...'aa']]);  // /a{2}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 3, {lazy: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{3}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 4, {lazy: true}), 'aaa', 0, 3, []);  // /a{4}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, null, {lazy: true}), 'aaa', 0, 3, [[], ['a'], [...'aa'], [...'aaa']]);  // /a{0,}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 1, null, {lazy: true}), 'aaa', 0, 3, [['a'], [...'aa'], [...'aaa']]);  // /a{1,}?/ or /a+?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 2, null, {lazy: true}), 'aaa', 0, 3, [[...'aa'], [...'aaa']]);  // /a{2,}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 3, null, {lazy: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{3,}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 4, null, {lazy: true}), 'aaa', 0, 3, []);  // /a{4,}?/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, 3, {lazy: true}), 'aaaa', 0, 4, [[], ['a'], [...'aa'], [...'aaa']]);  // /a{0,3}?/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 1, 3, {lazy: true}), 'aaaa', 0, 4, [['a'], [...'aa'], [...'aaa']]);  // /a{1,3}?/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 2, 3, {lazy: true}), 'aaaa', 0, 4, [[...'aa'], [...'aaa']]);  // /a{2,3}?/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 3, 3, {lazy: true}), 'aaaa', 0, 4, [[...'aaa']]);  // /a{3,3}?/ on 'aaaa'

    miniparser__test_comp_values(some(string('a'), {possessive: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a*+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 1, {possessive: true}), 'aaa', 0, 3, [['a']]);  // /a{1}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 2, {possessive: true}), 'aaa', 0, 3, [[...'aa']]);  // /a{2}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 3, {possessive: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{3}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 4, {possessive: true}), 'aaa', 0, 3, []);  // /a{4}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, null, {possessive: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{0,}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 1, null, {possessive: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{1,}+/ or /a++/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 2, null, {possessive: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{2,}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 3, null, {possessive: true}), 'aaa', 0, 3, [[...'aaa']]);  // /a{3,}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 4, null, {possessive: true}), 'aaa', 0, 3, []);  // /a{4,}+/ on 'aaa'
    miniparser__test_comp_values(some(string('a'), 0, 3, {possessive: true}), 'aaaa', 0, 4, [[...'aaa']]);  // /a{0,3}+/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 1, 3, {possessive: true}), 'aaaa', 0, 4, [[...'aaa']]);  // /a{1,3}+/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 2, 3, {possessive: true}), 'aaaa', 0, 4, [[...'aaa']]);  // /a{2,3}+/ on 'aaaa'
    miniparser__test_comp_values(some(string('a'), 3, 3, {possessive: true}), 'aaaa', 0, 4, [[...'aaa']]);  // /a{3,3}+/ on 'aaaa'

    miniparser__test_comp_values(some(string('')), 'a', 0, 1, [[''], []]);  // /(?:)*/ on 'a'
    miniparser__test_comp_values(some(string(''), 0, 3), 'a', 0, 1, [[''], []]);  // /(?:){0,3}/ on 'a'
    miniparser__test_comp_values(some(string(''), 2, 3), 'a', 0, 1, [['', '']]);  // /(?:){2,3}/ on 'a'
    miniparser__test_comp_values(some(string(''), {possessive: true}), 'a', 0, 1, [['']]);  // /(?:)*+/ on 'a'
  });


  setTimeout((string, some, chain) => { NAME = 'test_miniparser__chain';
    string = miniparser.string;
    some = miniparser.some;
    chain = miniparser.chain;
    miniparser__test_comp_values(chain([string('a'), string('b')]), 'ab', 0, 2, [[...'ab']]);  // /ab/ on 'ab'
    miniparser__test_comp_values(chain([string('a'), string('c')]), 'ab', 0, 2, []);  // /ac/ on 'ab'

    miniparser__test_comp_values(chain([some(string('a')), string('a')]), 'aaa', 0, 3, [[[...'aa'], 'a'], [['a'], 'a'], [[], 'a']]);  // /a*a/ on 'aaa'
    miniparser__test_comp_values(chain([some(string('a')), string('b')]), 'aab', 0, 3, [[[...'aa'], 'b']]);  // /a*b/ on 'aab'

    miniparser__test_comp_matches(chain([some(string('a')), some(string('a'))]), 'aaa', 0, 3, [  // /a*a/ on 'aaa'
      ['aaa', 0, 3, 0, 3, [[...'aaa'], []]],
      ['aaa', 0, 3, 0, 3, [[...'aa'], ['a']]],
      ['aaa', 0, 3, 0, 2, [[...'aa'], []]],
      ['aaa', 0, 3, 0, 3, [['a'], [...'aa']]],
      ['aaa', 0, 3, 0, 2, [['a'], ['a']]],
      ['aaa', 0, 3, 0, 1, [['a'], []]],
      ['aaa', 0, 3, 0, 3, [[], [...'aaa']]],
      ['aaa', 0, 3, 0, 2, [[], [...'aa']]],
      ['aaa', 0, 3, 0, 1, [[], ['a']]],
      ['aaa', 0, 3, 0, 0, [[], []]]]);

    miniparser__test_comp_matches(chain([some(string('a')), some(string('a'))], {possessive: true}), 'aaa', 0, 3, [  // /(?>a*a)/ on 'aaa'
      ['aaa', 0, 3, 0, 3, [[...'aaa'], []]]]);

    miniparser__test_comp_matches(chain([]), 'abc', 0, 3, [['abc', 0, 3, 0, 0, []]]);
  });

  setTimeout((string, select, chain) => { NAME = 'test_miniparser__chain_partial';
    string = miniparser.string;
    select = miniparser.select;
    chain = miniparser.chain;
    miniparser__test_comp_matches(chain([select([string('a'), string('a')]), string('b'), string('c')], {partial: true}), 'abc', 0, 3, [
      ['abc', 0, 3, 0, 3, ['a', 'b', 'c']],
      ['abc', 0, 3, 0, 2, ['a', 'b']],
      ['abc', 0, 3, 0, 1, ['a']],
      ['abc', 0, 3, 0, 3, ['a', 'b', 'c']],
      ['abc', 0, 3, 0, 2, ['a', 'b']],
      ['abc', 0, 3, 0, 1, ['a']],
      ['abc', 0, 3, 0, 0, []]]);
    miniparser__test_comp_matches(chain([select([string('a'), string('a')]), string('b'), string('c')], {partial: true}), 'ab', 0, 2, [
      ['ab', 0, 2, 0, 2, ['a', 'b']],
      ['ab', 0, 2, 0, 1, ['a']],
      ['ab', 0, 2, 0, 2, ['a', 'b']],
      ['ab', 0, 2, 0, 1, ['a']],
      ['ab', 0, 2, 0, 0, []]]);
    miniparser__test_comp_matches(chain([select([string('a'), string('a')]), string('b'), string('c')], {partial: true, lazy: true}), 'ab', 0, 2, [
      ['ab', 0, 2, 0, 0, []],
      ['ab', 0, 2, 0, 1, ['a']],
      ['ab', 0, 2, 0, 2, ['a', 'b']],
      ['ab', 0, 2, 0, 1, ['a']],
      ['ab', 0, 2, 0, 2, ['a', 'b']]]);
    miniparser__test_comp_matches(chain([select([string('a'), string('a')]), string('b'), string('c')], {partial: true, lazy: true}), 'abc', 0, 3, [
      ['abc', 0, 3, 0, 0, []],
      ['abc', 0, 3, 0, 1, ['a']],
      ['abc', 0, 3, 0, 2, ['a', 'b']],
      ['abc', 0, 3, 0, 3, ['a', 'b', 'c']],
      ['abc', 0, 3, 0, 1, ['a']],
      ['abc', 0, 3, 0, 2, ['a', 'b']],
      ['abc', 0, 3, 0, 3, ['a', 'b', 'c']]]);
  });

  setTimeout((string, select, some) => { NAME = 'test_miniparser__select';
    string = miniparser.string;
    select = miniparser.select;
    some = miniparser.some;
    miniparser__test_comp_values(select([string('a'), string('b')]), 'a', 0, 1, ['a']);  // `a|b` on 'a'
    miniparser__test_comp_values(select([string('a'), string('b')]), 'b', 0, 1, ['b']);  // `a|b` on 'b'
    miniparser__test_comp_values(select([some(string('a')), string('b')]), 'b', 0, 1, [[], 'b']);  // `a*|b` on 'b'
    miniparser__test_comp_values(select([some(string('a')), some(string('b'))]), 'b', 0, 1, [[], ['b'], []]);  // `a*|b*` on 'b'
    miniparser__test_comp_matches(select([some(string('a')), some(string('b'))], {getindexvalue: true}), 'b', 0, 1, [  // `a*|b*` on 'b'
      ['b', 0, 1, 0, 0, [0, []]],
      ['b', 0, 1, 0, 1, [1, ['b']]],
      ['b', 0, 1, 0, 0, [1, []]]]);
    miniparser__test_comp_matches(select([some(string('a')), some(string('b'))], {getindex: true}), 'b', 0, 1, [  // `a*|b*` on 'b'
      ['b', 0, 1, 0, 0, 0],
      ['b', 0, 1, 0, 1, 1],
      ['b', 0, 1, 0, 0, 1]]);
    miniparser__test_comp_matches(select([]), 'b', 0, 1, []);
  });

  setTimeout((string, some, chain, atomic) => { NAME = 'test_miniparser__atomic';
    string = miniparser.string;
    some = miniparser.some;
    chain = miniparser.chain;
    atomic = miniparser.atomic;
    miniparser__test_comp_values(atomic(some(string('a'))), 'aaa', 0, 3, [[...'aaa']]);  // /(?>a*)/ on 'aaa'
    miniparser__test_comp_values(chain([atomic(some(string('a'))), string('a')]), 'aaa', 0, 3, []);  // /(?>a*)a/ on 'aaa'
  });

  setTimeout(read => { NAME = 'test_miniparser__read';
    read = miniparser.read;
    miniparser__test_comp_values(read(0), 'aaa', 0, 3, ['']);     // `.{0}`
    miniparser__test_comp_values(read(1), 'aaa', 0, 3, ['a']);    // `.{1}`
    miniparser__test_comp_values(read(2), 'aaa', 0, 3, ['aa']);   // `.{2}`
    miniparser__test_comp_values(read(3), 'aaa', 0, 3, ['aaa']);  // `.{3}`
    miniparser__test_comp_values(read(4), 'aaa', 0, 3, []);       // `.{4}`
  });

  setTimeout((string, search) => { NAME = 'test_miniparser__search';
    string = miniparser.string;
    search = miniparser.search;
    miniparser__test_comp_matches(search(string('b')), 'fedcbabcdef', 0, 11, [['fedcbabcdef', 0, 11, 4, 5]]);
    miniparser__test_comp_matches(search(string('b'), {getscanned: true}), 'fedcbabcdef', 0, 11, [['fedcbabcdef', 0, 11, 0, 5, ['fedc', 'b']]]);
    miniparser__test_comp_values(search(string('b'), {getscanned: true, possessive: false}), 'fedcbabcdef', 0, 11, [['fedc', 'b'], ['fedcba', 'b']]);
    miniparser__test_comp_values(search(string('b'), {getscanned: true, lazy: false, possessive: false}), 'fedcbabcdef', 0, 11, [['fedcba', 'b'], ['fedc', 'b']]);
  });

  setTimeout((string, block) => { NAME = 'test_miniparser__block';
    string = miniparser.string;
    block = miniparser.block;
    miniparser__test_comp_matches(block(string('{'), string('.'), string('}')), '{...}', 0, 5, [['{...}', 0, 5, 0, 5, ['{', ['.', '.', '.'], '}']]]);
  });

  setTimeout((string, someSep) => { NAME = 'test_miniparser__someSep';
    string = miniparser.string;
    someSep = miniparser.someSep;
    miniparser__test_comp_matches(someSep(string('abc'), string(';')), '', 0, 0, [
      ['', 0, 0, 0, 0, []],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';')), 'abc', 0, 3, [
      ['abc', 0, 3, 0, 3, ['abc']],
      ['abc', 0, 3, 0, 0, []],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';')), 'abc;abc', 0, 7, [
      ['abc;abc', 0, 7, 0, 7, ['abc', ';', 'abc']],
      ['abc;abc', 0, 7, 0, 3, ['abc']],
      ['abc;abc', 0, 7, 0, 0, []],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';')), 'abc;abc;abc', 0, 11, [
      ['abc;abc;abc', 0, 11, 0, 11, ['abc', ';', 'abc', ';', 'abc']],
      ['abc;abc;abc', 0, 11, 0, 7, ['abc', ';', 'abc']],
      ['abc;abc;abc', 0, 11, 0, 3, ['abc']],
      ['abc;abc;abc', 0, 11, 0, 0, []],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';'), 0), 'abc;abc;abc', 0, 11, [
      ['abc;abc;abc', 0, 11, 0, 0, []],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';'), 0, 1), 'abc;abc;abc', 0, 11, [
      ['abc;abc;abc', 0, 11, 0, 3, ['abc']],
      ['abc;abc;abc', 0, 11, 0, 0, []],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';'), 1, 2), 'abc;abc;abc', 0, 11, [
      ['abc;abc;abc', 0, 11, 0, 7, ['abc', ';', 'abc']],
      ['abc;abc;abc', 0, 11, 0, 3, ['abc']],
    ]);
    miniparser__test_comp_matches(someSep(string('abc'), string(';')), 'abc;abc;def;abc', 0, 15, [
      ['abc;abc;def;abc', 0, 15, 0, 7, ['abc', ';', 'abc']],
      ['abc;abc;def;abc', 0, 15, 0, 3, ['abc']],
      ['abc;abc;def;abc', 0, 15, 0, 0, []],
    ]);
  });


}());
