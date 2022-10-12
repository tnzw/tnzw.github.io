# os_win32_wmic_diskdrive_list.py Version 1.0.0
# Copyright (c) 2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_win32_wmic_diskdrive_list():
  # https://docs.microsoft.com/fr-fr/windows/win32/cimwin32prov/win32-diskdrive
  win32_diskdrive_types = {
    b'Availability': 'uint16',
    b'BytesPerSector': 'uint32',
    b'Capabilities': 'uint16[]',
    b'CapabilityDescriptions': 'string[]',
    b'Caption': 'string',
    b'CompressionMethod': 'string',
    b'ConfigManagerErrorCode': 'uint32',
    b'ConfigManagerUserConfig': 'boolean',
    b'CreationClassName': 'string',
    b'DefaultBlockSize': 'uint64',
    b'Description': 'string',
    b'DeviceID': 'string',
    b'ErrorCleared': 'boolean',
    b'ErrorDescription': 'string',
    b'ErrorMethodology': 'string',
    b'FirmwareRevision': 'string',
    b'Index': 'uint32',
    b'InstallDate': 'datetime',
    b'InterfaceType': 'string',
    b'LastErrorCode': 'uint32',
    b'Manufacturer': 'string',
    b'MaxBlockSize': 'uint64',
    b'MaxMediaSize': 'uint64',
    b'MediaLoaded': 'boolean',
    b'MediaType': 'string',
    b'MinBlockSize': 'uint64',
    b'Model': 'string',
    b'Name': 'string',
    b'NeedsCleaning': 'boolean',
    b'NumberOfMediaSupported': 'uint32',
    b'Partitions': 'uint32',
    b'PNPDeviceID': 'string',
    b'PowerManagementCapabilities': 'uint16[]',
    b'PowerManagementSupported': 'boolean',
    b'SCSIBus': 'uint32',
    b'SCSILogicalUnit': 'uint16',
    b'SCSIPort': 'uint16',
    b'SCSITargetId': 'uint16',
    b'SectorsPerTrack': 'uint32',
    b'SerialNumber': 'string',
    b'Signature': 'uint32',
    b'Size': 'uint64',
    b'Status': 'string',
    b'StatusInfo': 'uint16',
    b'SystemCreationClassName': 'string',
    b'SystemName': 'string',
    b'TotalCylinders': 'uint64',
    b'TotalHeads': 'uint32',
    b'TotalSectors': 'uint64',
    b'TotalTracks': 'uint64',
    b'TracksPerCylinder': 'uint32',
  }
  def _parse(t, value):
    if t == 'string': return value
    if t == 'string[]':
      if value in (b'', b'{}'): return []
      return [_ for _ in value[2:-2].split(b'","')]
    if t in ('uint16', 'uint32', 'uint64'):
      if value == b'': return None
      return int(value)
    if t in ('uint16[]', 'uint32[]', 'uint64[]'):
      if value in (b'', b'{}'): return []
      return [int(_) for _ in value[1:-1].split(b',')]
    if t == 'boolean':
      if value == b'': return None
      if value == b'TRUE': return True
      if value == b'FALSE': return False
      raise ValueError(f'invalid boolean: {value!r}')
    if t == 'datetime':
      if value == b'': return None
      return b'<datetime ' + value + b'>'
    raise ValueError(f'unhandled type: {t!r}')
  #cp = subprocess.run(["wmic", "volume", "get", "/format:list"], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
  cp = subprocess.run(["wmic", "diskdrive", "list", "/format:list"], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
  line = re.compile(b'([^\\r\\n=]*)=([^\\r\\n]*)\\r*\\n')
  sep = re.compile(b'\\r*\\n(?:\\r*\\n)*')
  l = []
  m = sep.match(cp.stdout)
  while m:
    o = {}
    cur = m.end()
    m = line.match(cp.stdout, cur)
    while m:
      cur = m.end()
      o[m.group(1)] = _parse(win32_diskdrive_types.get(m.group(1), 'string'), m.group(2))
      m = line.match(cp.stdout, cur)
    if o: l.append(o)
    m = sep.match(cp.stdout, cur)
  return l
os_win32_wmic_diskdrive_list._required_globals = ["re", "subprocess"]
