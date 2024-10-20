this.functionHelpers = (function script() {
  "use strict";

  /*! functionHelpers.js Version 1.0.0

      Copyright (c) 2024 <tnzw@github.triton.ovh>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  // https://github.com/tc39/proposal-pipeline-operator
  // https://github.com/tc39/proposal-function-helpers
  const pipe = (init, ...fns) => fns.reduce((init, fn) => fn(init), init);
  const pipeAsync = (init, ...fns) => { init = Promise.resolve(init); for (let fn of fns) init = init.then(fn); return init };
  const flow = (fn, ...fns) => (...args) => pipe(fn(...args), ...fns);
  const flowAsync = (fn, ...fns) => (...args) => pipeAsync(fn(...args), ...fns);
  const constant = x => () => x;
  const identity = x => x;
  const noop = () => {};
  const aside = (fn, value) => { fn(value); return value };
  const unThis = fn => fn.call.bind(fn);
  const once = fn => {
    let called = false;
    return (...args) => {
      if (called) return;
      called = true;
      return fn(...args);
    };
  };
  const debounce = (fn, delay) => {  // runs `fn` after `delay` ms of inactivity
    let timer = null;
    return (...args) => {
      clearTimeout(timer);
      timer = setTimeout(() => fn(...args), delay);
    };
  };
  const throttle = (fn, delay) => {  // runs `fn` only if not previously called within `delay` ms
    let timer = null;
    return (...args) => {
      if (timer != null) return;
      timer = setTimeout(() => timer = null, delay);
      fn(...args);
    };
  };

  const functionHelpers = {
    pipe, pipeAsync,
    flow, flowAsync,
    constant, identity, noop,
    aside, unThis, once, debounce, throttle,
  };
  functionHelpers.toScript = function () { return "(" + script.toString() + "())"; };
  return functionHelpers;

}());
