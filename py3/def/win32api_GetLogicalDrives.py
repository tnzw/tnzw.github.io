# win32api_GetLogicalDrives.py Version 1.0.0
#   This is free and unencumbered software released into the public domain.
#   SPDX: Unlicense <http://unlicense.org/>
#   Contributors: 2024 <tnzw@github.triton.ovh>

def win32api_GetLogicalDrives():
  # win32api_GetLogicalDrives() -> ['C:', 'D:', ...]
  # https://learn.microsoft.com/fr-fr/windows/win32/api/fileapi/nf-fileapi-getlogicaldrives
  # https://stackoverflow.com/questions/827371/is-there-a-way-to-list-all-the-available-windows-drives
  drives = []
  bitmask = ctypes.windll.kernel32.GetLogicalDrives()
  if bitmask == 0:
    raise SystemError(f'ctypes.windll.kernel32.GetLogicalDrives() failed with error code {ctypes.GetLastError()}')
  for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
    if bitmask & 1:
      drives.append(letter + ':')
    bitmask >>= 1
  return drives
win32api_GetLogicalDrives._required_globals = ['ctypes']
