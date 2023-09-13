# zipfile_archive_pipealgo.py Version 1.0.0
# Copyright (c) 2023 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def zipfile_archive_pipealgo(state, value):
  """\
zipfile_archive_pipealgo()

Allows to create a new zip archive stream by giving components.

Usage:
    state = None
    with open('archive.zip', 'wb') as f:
      state, zipchunk, done = zipfile_archive_pipealgo(state, ('entry', {'path': 'my_file.txt'}))
      f.write(zipchunk)
      state, zipchunk, done = zipfile_archive_pipealgo(state, ('data', b'my_data'))
      f.write(zipchunk)
      state, zipchunk, done = zipfile_archive_pipealgo(state, ('close',))
      f.write(zipchunk)
"""
  force_zip64 = False
  #VM_FAT = 0x14  # a one used by jszip
  VM_FAT = 0x3F  # the one used by 7zip on windows
  VM_UNIX = 0x31E  # a one used by jszip
  CM_STORE = 0
  BF_STREAM = 8
  if state is None:
    cen_data = fn = fe = nte = b''
    state = loc_size = entry_count = vm = ddt = ea = offset = crc32 = compressed_size = uncompressed_size = 0
    if value is None:
      return (state, loc_size, entry_count, cen_data, fn, fe, nte, vm, ddt, ea, offset, crc32, compressed_size, uncompressed_size), b'', False
  elif state[0] == -1:
    return (-1,), None, True
    #raise StopIteration()
  else:
    state, loc_size, entry_count, cen_data, fn, fe, nte, vm, ddt, ea, offset, crc32, compressed_size, uncompressed_size = state
  res = []
  if state == 1 and value[0] != 'data':  # end of loc data sending
    uncompressed_size_32 = 0xFFFFFFFF if uncompressed_size >= 0xFFFFFFFF else 0  # 7zip handles both >= and >. 7zip adds a zip64 extra field so it uses >=.
    compressed_size_32   = 0xFFFFFFFF if   compressed_size >= 0xFFFFFFFF else 0  # 7zip handles both >= and >. 7zip adds a zip64 extra field so it uses >=.
    if force_zip64 or uncompressed_size_32 or compressed_size_32: dd = zipfile_struct_mkdd64record(crc32, compressed_size, uncompressed_size)
    else:                                                         dd =   zipfile_struct_mkddrecord(crc32, compressed_size, uncompressed_size)
    res.append(dd)
    loc_size += len(dd)
    offset_32 = offset
    # 7zip handles both >= and >. 7zip adds a zip64 extra field so it uses >=.
    if force_zip64 or offset >= 0xFFFFFFFF: z64e = zipfile_struct_mkzip64extrafield(uncompressed_size, compressed_size, offset); uncompressed_size_32 = compressed_size_32 = offset_32 = 0xFFFFFFFF
    elif compressed_size_32:                z64e = zipfile_struct_mkzip64extrafield(uncompressed_size, compressed_size); uncompressed_size_32 = 0xFFFFFFFF
    elif uncompressed_size_32:              z64e = zipfile_struct_mkzip64extrafield(uncompressed_size)
    else:                                   z64e = b''
    cen_data += zipfile_struct_mkcenrecord(vm, 0x2D if z64e else 0xA, BF_STREAM, CM_STORE, ddt, crc32, compressed_size_32 or compressed_size, uncompressed_size_32 or uncompressed_size, 0, 0, ea, offset_32, fn, nte + fe + z64e)  # XXX use version 0x2D if z64e else 0xA? works with 0xA in all tested cases
    entry_count += 1
    state = 0
  if state == 0:
    if value[0] == 'close':  # closing archive
      cen_size = len(cen_data)
      res.append(cen_data)
      if force_zip64 or loc_size >= 0xFFFFFFFF or cen_size >= 0xFFFFFFFF or entry_count >= 0xFFFFFFFF:  # XXX use >= or > ?
        res.append(zipfile_struct_mkeocd64record(0x2D, 0x2D, 0, 0, entry_count, entry_count, cen_size, loc_size))
        res.append(zipfile_struct_mkeocd64locatorrecord(0, loc_size + cen_size, 1))
      res.append(zipfile_struct_mkeocdrecord(0, 0, 0xFFFFFFFF if entry_count > 0xFFFFFFFF else entry_count, 0xFFFFFFFF if entry_count > 0xFFFFFFFF else entry_count, 0xFFFFFFFF if cen_size > 0xFFFFFFFF else cen_size, 0xFFFFFFFF if loc_size > 0xFFFFFFFF else loc_size))
      state = -1
      # "FREEING" VARS
      cen_data = fn = fe = nte = b''
      loc_size = entry_count = ddt = ea = offset = crc32 = compressed_size = uncompressed_size = 0
    else:  # sending new entry
      t, entry = value
      if t != 'entry': raise ValueError('expected entry')
      # an entry is a dict with {'path': str|utf8_bytes, 'st_mode'?: int|None, 'is_dir'?: bool|None, 'st_mtime'?: int|float|None, 'st_mtime_offset'?: 'utc'|int|float|None}
      # 'path' separator MUST be slash '/'
      # 'path' MUST end with a slash for dirs else 'path' MUST NOT end with a slash for non-dirs
      path = entry['path']
      st_mode = entry.get('st_mode', None)
      is_dir = entry.get('is_dir', None)
      if st_mode is None:
        vm = VM_FAT
        st_mode = 0
      else:
        vm = VM_UNIX
        if is_dir is None: is_dir = st_mode & 0o40000  # 0o40000 is stat.S_IFDIR
      st_mtime = entry.get('st_mtime', None)
      if st_mtime is None: st_mtime = time.time()
      st_mtime_offset = entry.get('st_mtime_offset', None)
      try:
        if st_mtime_offset == 'utc':      ddt = dosdatetime_fromutctimestamp(st_mtime, True)
        elif st_mtime_offset is not None: ddt = dosdatetime_fromutctimestamp(st_mtime + st_mtime_offset, True)
        else:                             ddt = dosdatetime_fromtimestamp(st_mtime, True)
        if ddt > 0xFFFFFFFF: ddt = 0
      # set ddt = 0 if st_mtime is lower than 1980-01-01 00:00:00 (eg < 315532800 in GMT+0 systems)
      # anyway, ntfs time has priority over dos date time.
      except ValueError: ddt = 0
      #nte = zipfile_struct_mkunixtimeextrafield(intceil(st_mtime))
      nte = zipfile_struct_mkntfstimeextrafield(ntfstime_fromtimestamp(st_mtime, True), 0, 0)
      if type(path) is bytes: fn = fnu = path; fe = b''  # for backward compat, fn should be cp437 encoded, but I think I don't care for now.
      else:                   fn = path.encode('cp437', 'replace'); fnu = path.encode('utf8'); fe = b''
      if not path.isascii() or fn != fnu: fe = zipfile_struct_mkunicodepathextrafield(zlib_crc32(fn), fnu)
      if is_dir:
        if fn[-1:] != b'/': raise ValueError("invalid dir path")
        uncompressed_size_32 = compressed_size_32 = 0
        ea = (st_mode << 16) | 0x10
        offset_32 = offset = loc_size
        # 7zip handles both >= and >. 7zip adds a zip64 extra field so it uses >=.
        if force_zip64 or offset >= 0xFFFFFFFF: z64e = zipfile_struct_mkzip64extrafield(uncompressed_size, compressed_size, offset); uncompressed_size_32 = compressed_size_32 = offset_32 = 0xFFFFFFFF
        else:                                   z64e = b''
        loc = zipfile_struct_mklocrecord(0x14, 0, 0, ddt, 0, 0, 0, fn, fe)
        res.append(loc)
        loc_size += len(loc)
        cen_data += zipfile_struct_mkcenrecord(vm, 0x2D if z64e else 0x14, 0, 0, ddt, 0, compressed_size_32, uncompressed_size_32, 0, 0, ea, offset_32, fn, nte + fe + z64e)
        entry_count += 1
      else:
        if fn[-1:] == b'/': raise ValueError("invalid file path")
        crc32 = uncompressed_size = compressed_size = 0
        ea = (st_mode << 16) | 0x80
        offset = loc_size
        # LOC version needed: 7zip uses 0x2D for zip64, but here we don't put zip64 extrafield.
        loc = zipfile_struct_mklocrecord(0xA, BF_STREAM, CM_STORE, ddt, 0, 0, 0, fn, fe)
        res.append(loc)
        loc_size += len(loc)
        state = 1
  elif state == 1: # sending loc data
    t, chunk = value
    if t != 'data': raise ValueError('expected data')
    chunk = memoryview(chunk)  # XXX handle other types?
    crc32 = zlib_crc32(chunk, crc32)
    uncompressed_size += len(chunk)
    compressed_chunk = chunk  # compress chunk here
    compressed_chunk_len = len(compressed_chunk)
    compressed_size += compressed_chunk_len
    res.append(compressed_chunk)
    loc_size += compressed_chunk_len
  else:
    raise RuntimeError('invalid state')
  return (state, loc_size, entry_count, cen_data, fn, fe, nte, vm, ddt, ea, offset, crc32, compressed_size, uncompressed_size), b''.join(res), False
zipfile_archive_pipealgo._required_globals = ['dosdatetime_fromtimestamp', 'dosdatetime_fromutctimestamp', 'ntfstime_fromtimestamp', 'zipfile_struct_mkcenrecord', 'zipfile_struct_mkdd64record', 'zipfile_struct_mkddrecord', 'zipfile_struct_mkeocd64record', 'zipfile_struct_mkeocd64locatorrecord', 'zipfile_struct_mkeocdrecord', 'zipfile_struct_mklocrecord', 'zipfile_struct_mkntfstimeextrafield', 'zipfile_struct_mkunicodepathextrafield', 'zipfile_struct_mkzip64extrafield', 'zlib_crc32']
