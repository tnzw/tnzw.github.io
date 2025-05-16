# win32api_GetVolumeInformation.py Version 1.0.0
#   This is free and unencumbered software released into the public domain.
#   SPDX: Unlicense <http://unlicense.org/>
#   Contributors: 2024 <tnzw@github.triton.ovh>

def win32api_GetVolumeInformation(root_path_name):
  # win32api_GetVolumeInformation('C:\\') -> (volume_name, serial_number, max_component_length, file_system_flags, file_system_name)
  # https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getvolumeinformationw
  # https://stackoverflow.com/questions/8319264/how-can-i-get-the-name-of-a-drive-in-python
  volume_name_buffer = ctypes.create_unicode_buffer(1024)
  file_system_name_buffer = ctypes.create_unicode_buffer(1024)
  serial_number = ctypes.wintypes.DWORD()
  max_component_length = ctypes.wintypes.DWORD()
  file_system_flags = ctypes.wintypes.DWORD()
  rc = ctypes.windll.kernel32.GetVolumeInformationW(
      ctypes.c_wchar_p(root_path_name),
      volume_name_buffer,
      ctypes.sizeof(volume_name_buffer),
      ctypes.byref(serial_number),
      ctypes.byref(max_component_length),
      ctypes.byref(file_system_flags),
      file_system_name_buffer,
      ctypes.sizeof(file_system_name_buffer)
  )
  if rc:
    return volume_name_buffer.value, serial_number.value, max_component_length.value, file_system_flags.value, file_system_name_buffer.value
  raise SystemError(f'ctypes.windll.kernel32.GetVolumeInformationW() failed with error code {ctypes.GetLastError()}')
win32api_GetVolumeInformation._required_globals = ['ctypes', 'ctypes.wintypes']
