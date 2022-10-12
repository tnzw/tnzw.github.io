# winreg_dumpkey.py Version 0.0.1
# Copyright (c) 2022 <tnzw@github.triton.ovh>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def winreg_dumpkey(key, sub_key, *, banner=False, key_name=None, permission_errors='strict'):
  # data = winreg_dumpkey(winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\\Python', banner=True)
  # with open('save.reg', 'wb') as f: f.write(b'\xff\xfe' + data.encode('utf-16-le'))
  #
  # some keys cannot be exported even if running as admin
  #   like "Microsoft-Windows-Activation"
  ## https://stackoverflow.com/questions/8568175/using-a-python-script-to-backup-windows-registry-to-file-before-editing
  #import winreg, win32security, win32api
  #win32security.AdjustTokenPrivileges(win32security.OpenProcessToken(win32api.GetCurrentProcess(), 40), 0, [(win32security.LookupPrivilegeValue(None, 'SeBackupPrivilege'), 2)])  # Basically, adjusts permissions for the interpreter to allow registry backups

  def check_errors(errors):
    if errors in ('strict', 'exclude_key', 'comment', 'ignore', 'pass'): return errors
    raise LookupError(f"unknown error handler name {errors!r}")

  def joinhex(bytes, wrap=80, offset=0):
    if wrap <= 0:
      return ','.join(f'{b:02x}' for b in bytes)
    rr = []
    r = []
    for b in bytes:
      r.append(f'{b:02x}')
      offset += 3
      if offset + 3 >= wrap:
        rr.append(r); r = []
        offset = 2
    if r: rr.append(r)
    return ',\\\n  '.join(','.join(r) for r in rr)

  def sz_tostr(sz):
    return '"' + sz.replace('\\', '\\\\').replace('"', '\\"') + '"'

  s = ['Windows Registry Editor Version 5.00\n\n'] if banner else []
  _00 = b'\x00\x00'

  if key_name is None:
    for _ in dir(winreg):
      if _.startswith('HKEY_') and getattr(winreg, _) == key:
        key_name = _
        break
    else: raise ValueError('cannot guess key name')

  s.append(f'[{key_name}\\{sub_key}]\n')
  with winreg_scankey(key, sub_key) as scan:  # XXX set winreg_scankey order=('values', 'keys')?
    k = []
    for _ in scan:
      n = sz_tostr(_.name) if _.name else '@'
      if _.type == 'key':
        try:
          k.append('\n')
          k.append(winreg_dumpkey(key, sub_key + '\\' + _.name, key_name=key_name))
        except PermissionError:
          if check_errors(permission_errors) == 'strict': raise
          elif permission_errors == 'exclude_key': pass
          elif permission_errors == 'comment':
            k.append(f'[{key_name}\\{sub_key}\\{_.name}]\n; PERMISSION ERROR!\n')
          else:  # ignore | pass
            k.append(f'[{key_name}\\{sub_key}\\{_.name}]\n')
      elif _.data_type == winreg.REG_NONE:
        s.append(f'{n}=hex(0):\n')
      elif _.data_type == winreg.REG_SZ:
        s.append(f'{n}={sz_tostr(_.data)}\n')
      elif _.data_type == winreg.REG_BINARY:
        p = f'{n}=hex:'
        s.append(f'{p}{joinhex(b"" if _.data is None else _.data, offset=len(p))}\n')
      elif _.data_type == winreg.REG_DWORD_LITTLE_ENDIAN:
        s.append(f'{n}=dword:{_.data:08x}\n')
      elif _.data_type == winreg.REG_QWORD_LITTLE_ENDIAN:
        p = f'{n}=hex(b):'
        s.append(f'{p}{joinhex(uint64_littleendian_tobytes(_.data), offset=len(p))}\n')
      elif _.data_type == winreg.REG_EXPAND_SZ:
        p = f'{n}=hex(2):'
        s.append(f'{p}{joinhex(_.data.encode("utf-16-le") + _00, offset=len(p))}\n')
        #s.append(f'{n}={sz_tostr(_.data)}\n')
      elif _.data_type == winreg.REG_MULTI_SZ:
        p = f'{n}=hex(7):'
        if _.data is None: d = b''
        elif _.data: d = _00.join(e.encode('utf-16-le') for e in _.data) + _00 + _00
        else: d = _00
        s.append(f'{p}{joinhex(d, offset=len(p))}\n')
        del d
      else: raise NotImplementedError(key_name, sub_key, _.name, _.data, _.data_type, [w for w in dir(winreg) if getattr(winreg, w) == _.data_type])
    if k: s.extend(k)
  return ''.join(s)
winreg_dumpkey._required_globals = ['winreg', 'winreg_scankey', 'uint64_littleendian_tobytes']
