# os_win32_wmic_logicaldisk_get.py Version 1.0.0
# Copyright (c) 2022 Tristan Cavelier <t.cavelier@free.fr>
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://www.wtfpl.net/ for more details.

def os_win32_wmic_logicaldisk_get():
  # https://docs.microsoft.com/fr-fr/windows/win32/cimwin32prov/win32-logicaldisk
  win32_logicaldisk_types = {
    b'Access': 'uint16',
    b'Availability': 'uint16',
    b'BlockSize': 'uint64',
    b'Caption': 'string',
    b'Compressed': 'boolean',
    b'ConfigManagerErrorCode': 'uint32',
    b'ConfigManagerUserConfig': 'boolean',
    b'CreationClassName': 'string',
    b'Description': 'string',
    b'DeviceID': 'string',
    b'DriveType': 'uint32',
    b'ErrorCleared': 'boolean',
    b'ErrorDescription': 'string',
    b'ErrorMethodology': 'string',
    b'FileSystem': 'string',
    b'FreeSpace': 'uint64',
    b'InstallDate': 'datetime',
    b'LastErrorCode': 'uint32',
    b'MaximumComponentLength': 'uint32',
    b'MediaType': 'uint32',
    b'Name': 'string',
    b'NumberOfBlocks': 'uint64',
    b'PNPDeviceID': 'string',
    b'PowerManagementCapabilities': 'uint16[]',
    b'PowerManagementSupported': 'boolean',
    b'ProviderName': 'string',
    b'Purpose': 'string',
    b'QuotasDisabled': 'boolean',
    b'QuotasIncomplete': 'boolean',
    b'QuotasRebuilding': 'boolean',
    b'Size': 'uint64',
    b'Status': 'string',
    b'StatusInfo': 'uint16',
    b'SupportsDiskQuotas': 'boolean',
    b'SupportsFileBasedCompression': 'boolean',
    b'SystemCreationClassName': 'string',
    b'SystemName': 'string',
    b'VolumeDirty': 'boolean',
    b'VolumeName': 'string',
    b'VolumeSerialNumber': 'string',
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
      return value  # XXX
    raise ValueError(f'unhandled type: {t!r}')
  cp = subprocess.run(["wmic", "logicaldisk", "get", "/format:list"], input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
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
      o[m.group(1)] = _parse(win32_logicaldisk_types.get(m.group(1), 'string'), m.group(2))
      m = line.match(cp.stdout, cur)
    if o: l.append(o)
    m = sep.match(cp.stdout, cur)
  return l
os_win32_wmic_logicaldisk_get.DRIVETYPE_UNKNOWN = 0
os_win32_wmic_logicaldisk_get.DRIVETYPE_NO_ROOT_DIRECTORY = 1
os_win32_wmic_logicaldisk_get.DRIVETYPE_REMOVABLE_DISK = 2
os_win32_wmic_logicaldisk_get.DRIVETYPE_LOCAL_DISK = 3
os_win32_wmic_logicaldisk_get.DRIVETYPE_NETWORK_DRIVE = 4
os_win32_wmic_logicaldisk_get.DRIVETYPE_COMPACT_DISC = 5
os_win32_wmic_logicaldisk_get.DRIVETYPE_RAM_DISK = 6
os_win32_wmic_logicaldisk_get._required_globals = ["re", "subprocess"]
