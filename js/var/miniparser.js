this.miniparser = (function script() {
  "use strict";

  /*! miniparser.js Version 2.4.1
      This is free and unencumbered software released into the public domain.
      SPDX: Unlicense <http://unlicense.org/>
      Contributors: 2023-2024 <tnzw@github.triton.ovh> */

  // This code is taken from my python implementation

  // a `match` is a list|tuple with -> (string, pos, endpos, start, end[, value])
  function match_new(string, pos, endpos, start, end, value) {
    if (value === undefined) return [string, pos, endpos, start, end];
    return [string, pos, endpos, start, end, value];
  }
  function match_frommatch(m, opt) {
    var v;
    if (opt && 'value' in opt) v = [opt.value];
    else if (opt?.getvalue ?? true) v = match_getvalueasslice(m);
    else v = [];
    return [
      opt && 'string' in opt ? opt.string : match_getstring(m),
      opt && 'pos'    in opt ? opt.pos    : match_getpos   (m),
      opt && 'endpos' in opt ? opt.endpos : match_getendpos(m),
      opt && 'start'  in opt ? opt.start  : match_getstart (m),
      opt && 'end'    in opt ? opt.end    : match_getend   (m),
      ...v
    ];
  }
  function match_getstring(m) { return m[0]; }
  function match_getpos   (m) { return m[1]; }
  function match_getendpos(m) { return m[2]; }
  function match_getstart (m) { return m[3]; }
  function match_getend   (m) { return m[4]; }
  function match_getvalueasslice(m) { return m.slice(5, 6); }
  function match_getvalue (m, defaut) {
    var v = match_getvalueasslice(m);
    if (v.length) return v[0];
    if (defaut === undefined) return match_getslice(m);
    return defaut;
  }
  function match_setvalue (m, v) { m[5] = v; return v; }
  function match_hasvalue (m) { return match_getvalueasslice(m).length ? true : false; }
  function match_getslice (m) {
    var s = match_getstart(m),
        e = match_getend(m);
    if (s < 0) return;
    return match_getstring(m).slice(s, e);
  }
  function match_getslicelen(m) {
    var l = match_getend(m) - match_getstart(m);
    if (l < 0) return 0;
    return l;
  }

  // "Pre-compiled" components

  function* NOTHING(string, pos, endpos) {  // `(?:|)`
    yield match_new(string, pos, endpos, pos, pos);
  }
  function* ONE(string, pos, endpos) {  // `.`
    if (pos < endpos) yield match_new(string, pos, endpos, pos, pos + 1);
  }
  function* EOF(string, pos, endpos) {  // `$` or `\Z`
    if (pos === string.length) yield match_new(string, pos, endpos, pos, pos);
  }
  function* BOF(string, pos, endpos) {  // `^` or `\A`
    if (pos === 0) yield match_new(string, pos, endpos, 0, 0);
  }
  function* ENDPOS(string, pos, endpos) {
    if (pos === endpos) yield match_new(string, pos, endpos, endpos, endpos);
  }

  // Leaf components

  function read(size) {  // `.{size}`
    return function* read(string, pos, endpos) {
      var endpos2 = pos + size;
      if (endpos2 <= endpos) yield match_new(string, pos, endpos, pos, endpos2);
    };
  }

  function string(pattern) {  // `abc`
    return function* string(string, pos, endpos) {
      var endpos2 = pos + pattern.length;
      if (endpos < endpos2) endpos2 = endpos;
      if (string.slice(pos, endpos2) === pattern)
        yield match_new(string, pos, endpos, pos, endpos2);
    };
  }

  function istring(pattern) {  // `abc`
    pattern = pattern.toLowerCase();
    return function* string(string, pos, endpos) {
      var endpos2 = pos + pattern.length;
      if (endpos < endpos2) endpos2 = endpos;
      if (string.slice(pos, endpos2).toLowerCase() === pattern)
        yield match_new(string, pos, endpos, pos, endpos2);
    };
  }

  function regexp(pattern) {
    // all regexp flags reminder: 'dgimsuvy'
    if (!pattern.sticky) pattern = new RegExp(pattern.source, pattern.flags + 'y');
    return function* regexp(string, pos, endpos) {
      var _, end;
      pattern.lastIndex = pos;
      if ((_ = pattern.exec(string))) {
        end = pos + _[0].length;
        if (end <= endpos) yield match_new(string, pos, endpos, pos, end);
      }
    };
  }

  function charIn(charset) {
    return function* charIn(string, pos, endpos) {
      if (pos < endpos && charset.indexOf(string[pos]) !== -1)
        yield match_new(string, pos, endpos, pos, pos + 1);
    };
  }

  function charNotIn(charset) {
    return function* charNotIn(string, pos, endpos) {
      if (pos < endpos && charset.indexOf(string[pos]) === -1)
        yield match_new(string, pos, endpos, pos, pos + 1);
    };
  }

  function oneCond(cond) {
    return function* oneCond(string, pos, endpos) {
      if (pos < endpos && cond(string[pos]))
        yield match_new(string, pos, endpos, pos, pos + 1);
    };
  }

  // One-component algorithms

  function optional(comp, opt) {  // `...?`
    var hasDefault = opt && 'default' in opt,
        defaut = hasDefault ? opt.default : null,
        possessive = !!opt?.possessive;
    return function* optional(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a)) {
        yield m;
        if (possessive) return;
      }
      if (hasDefault) yield match_new(string, pos, endpos, pos, pos, defaut);
      else            yield match_new(string, pos, endpos, pos, pos);
    };
  }

  function has(comp) {  // `(?=...)`
    return function* has(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a)) {
        yield match_new(string, pos, endpos, pos, pos, ...match_getvalueasslice(m));
        return;
      }
    };
  }

  function hasNot(comp) {  // `(?!...)`
    return function* hasNot(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a))
        return;
      yield match_new(string, pos, endpos, pos, pos);
    };
  }

  function had(comp, size) {  // `(?<=...)`
    return function* had(string, pos, endpos, ...a) {
      var pos_sub_size = pos - size;
      for (let m of comp(string, pos_sub_size > 0 ? pos_sub_size : 0, pos, ...a))
        if (match_getend(m) === pos) {
          yield match_new(string, pos, endpos, pos, pos, ...match_getvalueasslice(m));
          return;
        }
    };
  }

  function hadNot(comp, size) {  // `(?<!...)`
    return function* hadNot(string, pos, endpos, ...a) {
      var pos_sub_size = pos - size;
      for (let m of comp(string, pos_sub_size > 0 ? pos_sub_size : 0, pos, ...a))
        if (match_getend(m) === pos)
          return;
      yield match_new(string, pos, endpos, pos, pos);
    };
  }

  function atomic(comp) {  // `(?>...)`
    return function* atomic(...a) {
      for (let m of comp(...a)) {
        yield m;
        return;
      }
    };
  }

  // Multi-component algorithms

  function select(comps, opt) {
    const getindexvalue = !!opt?.getindexvalue,
          getindex = !!opt?.getindex,
          possessive = !!opt?.possessive;
    opt = undefined;
    return function* select(...a) {
      let i = -1; for (let comp of comps) { i += 1;
        for (let m of comp(...a)) {
          if (getindexvalue) yield match_frommatch(m, {value: [i, match_getvalue(m)]});
          else if (getindex) yield match_frommatch(m, {value: i});
          else yield m;
          if (possessive) return;
        }
      }
    };
  }

  function chain(comps, opt) {
    // `chain(a, b, c, partial=True)` acts like `some(chain(a, some(chain(b, some(c, 0, 1)), 0, 1)), 0, 1)`.
    const getvalues = !!(opt?.getvalues ?? true),
          partial = !!opt?.partial,
          lazy = !!opt?.lazy,
          possessive = !!opt?.possessive;
    if (!partial && lazy) throw new TypeError('cannot be lazy when partial is not enabled');
    if (lazy && possessive) throw new TypeError('please do not use lazy along with possessive');
    return function* chain(string, pos, endpos, ...a) {
      var stack, cur, i, g, _, m;
      if (comps.length === 0) {
        if (getvalues) yield match_new(string, pos, endpos, pos, pos, []);
        else           yield match_new(string, pos, endpos, pos, pos);
        return;
      }
      if (lazy) {  // here partial is True, possessive is False
        if (getvalues) yield match_new(string, pos, endpos, pos, pos, []);
        else           yield match_new(string, pos, endpos, pos, pos);
      }
      stack = []; stack.length = comps.length;
      cur = pos;
      i = 0
      while (i >= 0) {
        [g, m] = stack[i] || [comps[i](string, cur, endpos, ...a), null];
        _ = g.next();
        if (_.done) {
          if (partial && !lazy) {
            if (i === 0) {
              if (getvalues) yield match_new(string, pos, endpos, pos, pos, []);
              else           yield match_new(string, pos, endpos, pos, pos);
            } else {
              if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i - 1][1]), stack.slice(0, i).map(s => match_getvalue(s[1])));
              else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i - 1][1]));
            }
            if (possessive) return;
          }
          i -= 1;
        } else {
          m = _.value;
          stack[i] = [g, m];
          cur = match_getend(m);
          if (lazy) {  // here partial is True, possessive is False
            if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]), stack.slice(0, i + 1).map(s => match_getvalue(s[1])));
            else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]));
          }
          let elz = true; for (let comp of comps.slice(i + 1)) {
            i += 1;
            g = comp(string, cur, endpos, ...a);
            _ = g.next();
            if (_.done) { elz = false; break; }
            m = _.value;
            stack[i] = [g, m];
            cur = match_getend(m);
            if (lazy) {  // here partial is True, possessive is False
              if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]), stack.slice(0, i + 1).map(s => match_getvalue(s[1])));
              else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[i][1]));
            }
          }
          if (elz) {
            if (!lazy) {
              if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]), stack.map(s => match_getvalue(s[1])));
              //if (getvalues) yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
              else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]));
              if (possessive) return;
            }
          }
        }
      }
    };
  }

  function some(comp, ...repeats_opt) {
    // usage examples:
    //   some(...) or some(..., 0, null) -> `...*`
    //   some(..., 1, null)              -> `...+`
    //   some(..., 3) or some(..., 3, 3) -> `...{3}`
    //   some(..., 0, 1)                 -> `...{0,1}` or `...?`
    //   some(..., {lazy: true})         -> `...*?`
    //   some(..., {possessive: true})   -> `...*+`
    // When `unsafe` is falsish, some() stops if m.end doesn't go further.
    var opt = null, repeats = [], min_repeat, max_repeat;
    for (let r of repeats_opt) {
      if (typeof r === 'object' && r !== null) {
        if (opt !== null) throw new TypeError('too much option objects');
        opt = r;
      } else {
        repeats.push(r);
      }
    }
    if (repeats.length === 0) { min_repeat = 0; max_repeat = null; }
    else if (repeats.length === 1) min_repeat = max_repeat = repeats[0];
    else if (repeats.length === 2) [min_repeat, max_repeat] = repeats;
    else throw new TypeError(`some expected at most 4 arguments, got ${repeats.length + (!!opt) + 1}`);
    const getvalues = !!(opt?.getvalues ?? true),
          lazy = !!opt?.lazy,
          possessive = !!opt?.possessive,
          unsafe = !!opt?.unsafe;
    if (lazy && possessive) throw new TypeError('please do not use lazy along with possessive');
    if (max_repeat === undefined) max_repeat = null;
    return function* some(string, pos, endpos, ...a) {
      var l = 0,
          stack = [],
          cur = pos,
          _, g, m, m_end;
      if (lazy && l >= min_repeat) {
        if (getvalues) yield match_new(string, pos, endpos, pos, pos, []);
        else           yield match_new(string, pos, endpos, pos, pos);
      }
      // try to get more and more sub-match
      while (max_repeat === null || l < max_repeat) {
        g = comp(string, cur, endpos, ...a);
        _ = g.next();
        if (_.done) break;
        m = _.value;
        stack.push([g, m]); l += 1;
        m_end = match_getend(m);
        // handling unsafe
        if (cur < m_end || l < min_repeat || unsafe) cur = m_end;
        else break;
        if (lazy && l >= min_repeat) {
          if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]), stack.map(s => match_getvalue(s[1])));
          //if (getvalues) yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]));
        }
      }
      while (stack.length) {
        if (!lazy && l >= min_repeat) {
          if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]), stack.map(s => match_getvalue(s[1])));
          //if (getvalues) yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]));
          if (possessive) return;
        }
        [g, m] = stack.pop(); l -= 1;
        _ = g.next();
        if (_.done) continue
        m = _.value;
        stack.push([g, m]); l += 1;
        cur = match_getend(m);
        if (lazy && l >= min_repeat) {
          if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]), stack.map(s => match_getvalue(s[1])));
          //if (getvalues) yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
          else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]));
        }
        while (max_repeat === null || l < max_repeat) {
          g = comp(string, cur, endpos, ...a);
          _ = g.next();
          if (_.done) break
          m = _.value;
          stack.push([g, m]); l += 1;
          // handling unsafe
          if (cur < m_end || l < min_repeat || unsafe) cur = m_end;
          else break;
          if (lazy && l >= min_repeat) {
            if (getvalues) yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]), stack.map(s => match_getvalue(s[1])));
            //if (getvalues) yield match_new(string, pos, endpos, min(match_getstart(s[1]) for s in stack), max(match_getend(s[1]) for s in stack), [match_getvalue(s[1]) for s in stack])
            else           yield match_new(string, pos, endpos, match_getstart(stack[0][1]), match_getend(stack[stack.length - 1][1]));
          }
        }
      }
      if (!lazy && l >= min_repeat) {
        if (getvalues) yield match_new(string, pos, endpos, pos, pos, []);
        else           yield match_new(string, pos, endpos, pos, pos);
      }
    };
  }

  function search(comp, opt) {
    var getscanned = !!opt?.getscanned,
        scan_matches = !!(opt?.scanMatches ?? getscanned),
        lazy = !!(opt?.lazy ?? true),
        possessive = !!(opt?.possessive ?? true),
        scan_edit = opt?.scanEdit;
    if (getscanned && (scan_edit === undefined || scan_edit === null)) scan_edit = m => match_getvalue(m);
    return function* search(string, pos, endpos, ...a) {
      if (lazy)
        for (let cur = pos; cur <= endpos; cur += 1)
          for (let m of comp(string, cur, endpos, ...a)) {
            if (getscanned) yield match_new(string, pos, endpos, scan_matches ? pos : match_getstart(m), match_getend(m), [scan_edit(match_new(string, pos, endpos, pos, cur)), match_getvalue(m)]);
            else            yield match_new(string, pos, endpos, scan_matches ? pos : match_getstart(m), match_getend(m),                                                    ...match_getvalueasslice(m));
            if (possessive) return;
          }
      else
        for (let cur = endpos - 1; cur >= pos; cur -= 1)
          for (let m of comp(string, cur, endpos, ...a)) {
            if (getscanned) yield match_new(string, pos, endpos, scan_matches ? pos : match_getstart(m), match_getend(m), [scan_edit(match_new(string, pos, endpos, pos, cur)), match_getvalue(m)]);
            else            yield match_new(string, pos, endpos, scan_matches ? pos : match_getstart(m), match_getend(m),                                                    ...match_getvalueasslice(m))
            if (possessive) return;
          }
    };
  }

  // Match/Value handling

  function editmatch(comp, editor) {
    return function* editmatch(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a)) {
        var m2 = editor(m);  // XXX deep check editor() returned value? like using a match_validate()
        if (m2 !== undefined && m2 !== null) yield m2;
      }
    };
  }

  function editvalue(comp, editor) {
    return function* editvalue(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a))
        yield match_frommatch(m, {value: editor(match_getvalue(m))});
    };
  }

  function edit(comp, editor) {
    // keep sub match object in value: edit(..., lambda m: m)
    // value as matching: edit(..., lambda m: match_getslice(m))
    return function* edit(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a))
        yield match_frommatch(m, {value: editor(m)});
    };
  }

  // Error handling

  function critical(comp, fn) {  // throws if no match
    return function* critical(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a))
        yield m;
      throw fn(string, pos, endpos, ...a);
    };
  }

  function error(comp, fn) {  // raises if match
    return function* error(string, pos, endpos, ...a) {
      for (let m of comp(string, pos, endpos, ...a))
        throw fn(m);
    };
  }

  // Component functions and referencing

  //function genfunc(fn) {  // kinda useless as you can directly put `fn` as a comp.
  //  return function genfunc(string, pos, endpos, ...a) {
  //    return fn(string, pos, endpos, ...a);
  //  };
  //}

  function func(fn) {
    // func((string, pos, endpos) => match_new(string, pos, endpos, pos, endpos))
    return function* func(string, pos, endpos, ...a) {
      var m = fn(string, pos, endpos, ...a);
      if (m !== undefined || m !== null) yield m;
    };
  }

  function ref(fn) {
    // REC = chain(..., ref(_=>REC))
    return function ref(string, pos, endpos, ...a) {
      var comp = fn();
      return comp(string, pos, endpos, ...a);
    };
  }

  // Sugar components

  function stepSearch(stepComp, stopComp, opt) {  // opt{} => minSteps=0, maxSteps=null, getvalues=true, lazy=true, possessive=true, unsafe=false
    const getvalues = opt?.getvalues ?? true,
          lazy = opt?.lazy ?? true,
          possessive = opt?.possessive ?? true,
          unsafe = opt?.unsafe;
    return chain([some(stepComp, opt?.minSteps ?? 0, opt?.maxSteps, {getvalues, lazy, unsafe}), stopComp], {getvalues, possessive});
  }

  function block(startComp, stepComp, stopComp, opt) {  // opt{} => minSteps=0, maxSteps=null, lazy=false, possessive=true, unsafe=false
    return chain([startComp, some(stepComp, opt?.minSteps ?? 0, opt?.maxSteps, {lazy: opt?.lazy, unsafe: opt?.unsafe}), stopComp], {possessive: opt?.possessive ?? true});
  }

  function someSep(comp, sep, ...repeats_opt) {
    // ...repeats_opt => ...repeats, opt
    //   ...repeats   => min_repeat=0, max_repeat=null
    //   opt{}        => lazy=false, ...some.opt
    // someSep(not_hyphens, hyphen)('a-b-c', 0, 5)
    // -> ['a', '-', 'b', '-', 'c']
    // -> ['a', '-', 'b']
    // -> ['a']
    // -> []
    var opt = null, repeats = [], min_repeat, max_repeat, comp1;
    for (let r of repeats_opt) {
      if (typeof r === 'object' && r !== null) {
        if (opt !== null) throw new TypeError('too much option objects');
        opt = r;
      } else {
        repeats.push(r);
      }
    }
    if (repeats.length === 0) { min_repeat = 0; max_repeat = null; }
    else if (repeats.length === 1) min_repeat = max_repeat = repeats[0];
    else if (repeats.length === 2) [min_repeat, max_repeat] = repeats;
    else throw new TypeError(`some expected at most 5 arguments, got ${repeats.length + (!!opt) + 2}`);
    const getvalues = !!(opt?.getvalues ?? true);
    comp1 = chain([comp, some(chain([sep, comp], {getvalues}), min_repeat - 1, max_repeat === null || max_repeat === undefined ? null : max_repeat - 1, opt ?? {})], {getvalues});
    if (getvalues) comp1 = editvalue(comp1, v => v[1].reduce((p, c) => { for (let _ of c) p.push(_); return p }, [v[0]]));
    if (min_repeat === 0) {
      if (max_repeat === 0) comp1 = chain([], {getvalues});
      else if (opt?.lazy) comp1 = select([chain([], {getvalues}), comp1]);
      else comp1 = select([comp1, chain([], {getvalues})]);
    }
    return comp1;
  }

  function v_match(comp) { return edit(comp, m => m) }
  function v_slice(comp) { return edit(comp, m => match_getslice(m)) }
  function v_set  (comp, v) { return edit(comp, m => v) }
  function v_unset(comp) { return editmatch(comp, m => match_new(...m.slice(0, 5))) }

  // Top parser tools

  function mkparser(comp, opt) {
    var return_match = !!opt?.return_match;
    function check_int(v, s, d, l, p) {
      if (v === undefined || v === null) return d;
      if (typeof v === 'number' && v !== (v|0) || typeof v !== 'number') throw new TypeError(`${p} must be an integer`);
      if (v < 0) return 0;  // throw new Error(`${p} must be >= 0`);
      if (v > l) return l;
      return v;
    }
    function parser(string, pos, endpos) {
      var l = string.length, m;
      for (m of comp(string, check_int(pos, string, 0, l, 'pos'), check_int(endpos, string, l, l, 'endpos'))) {
        if (return_match) return m;
        return match_getvalue(m);
      }
      return null;
    }
    return parser;
  }

  var miniparser = {
    match_new, match_frommatch,
    match_getstring, match_getpos, match_getendpos, match_getstart, match_getend,
    match_hasvalue, match_getvalue, match_getvalueasslice, match_setvalue,
    match_getslice, match_getslicelen,
    NOTHING, ONE, EOF, BOF, ENDPOS,
    read, string, istring, regexp,
    charIn, charNotIn, oneCond,
    optional, has, hasNot, had, hadNot, atomic,
    select, chain, some, search,
    editmatch, editvalue, edit,
    critical, error,
    func, ref,
    block, someSep, stepSearch,
    v_match, v_slice, v_set, v_unset,
    mkparser,
  };
  miniparser.toScript = function () { return "(" + script.toString() + "())"; };
  return miniparser;

}());
