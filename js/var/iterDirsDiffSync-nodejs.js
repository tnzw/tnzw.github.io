this.iterDirsDiffSync = (function script() {
  "use strict";

  /*! iterDirsDiffSync-nodejs.js Version 1.0.0

      Copyright (c) 2020 Tristan Cavelier <t.cavelier@free.fr>
      This program is free software. It comes without any warranty, to
      the extent permitted by applicable law. You can redistribute it
      and/or modify it under the terms of the Do What The Fuck You Want
      To Public License, Version 2, as published by Sam Hocevar. See
      http://www.wtfpl.net/ for more details. */

  var _iterDirsDiffSync = function (action, paths) {
    // iterDirsDiffSync(action, paths) -> Error
    //   function rec(err, name, roots) {
    //     if (err) throw err;
    //     [a, b, c] = roots;
    //     // Do some stuff here...
    //     console.log(`name='${name}' exists in folder ${roots.join(" ")}`);
    //     // A var is defined if a node exists in its associated folder.
    //     // e.g. *a* is defined if the node exists in folder "a".
    //     //      If *b* is also defined then the node with the same name exists in folder "b" as well.
    //     //      If *c* is not defined then a node with the same name does not exist in folder "c".
    //     iterDirsDiffSync(rec, roots.map(p=>p&&p+"/"+name))  // recursive
    //   }
    //   iterDirsDiffSync(rec, ["a", "b", "c"]);
    var fs = require("fs"), os = require("os");
    _iterDirsDiffSync = function (action, paths) {
      var i = 0, err, dirs, indices, firstpaths, winner, params,
          dirpaths = [],
          subpaths = [];
      for (i=0;i<paths.length;++i) {
        dirs = undefined;
        if (paths[i] !== null && paths[i] !== undefined)
          try { dirs = fs.readdirSync(paths[i]); }
          catch (e) {
            if (e.errno !== -os.constants.errno.ENOENT &&
                e.errno !== -os.constants.errno.ENOTDIR)
              action(e, null, null)
          }
        dirpaths.push(dirs === undefined ? undefined : paths[i]);
        subpaths.push(dirs === undefined ? undefined : dirs.sort());
      }

      indices = []; i=paths.length; while (i--) indices.push(0);
      while (1) {
        firstpaths = [];
        for (i=0;i<paths.length;++i) {
          dirs = subpaths[i];
          if (dirs !== undefined)
            firstpaths[i] = dirs[indices[i]];
        }
        firstpaths.sort();
        winner = undefined;
        for (i=0;i<firstpaths.length;++i)
          if (firstpaths[i] !== undefined) {
            winner = firstpaths[i]
            break;
          }
        if (winner === undefined) return;

        params = []; for(i=paths.length;i--;) params.push(null);
        for (i=0;i<paths.length;++i) {
          if (subpaths[i] === undefined) continue;
          if (subpaths[i][indices[i]] === winner) {
            params[i] = paths[i];
            indices[i] = indices[i] + 1;
          }
        }
        action(null, winner, params);
      }
    };
    return _iterDirsDiffSync(action, paths);
  };
  function iterDirsDiffSync(action, paths) { return _iterDirsDiffSync(action, paths); }
  iterDirsDiffSync.toScript = function () { return "(" + script.toString() + "())"; };
  return iterDirsDiffSync;

}());
