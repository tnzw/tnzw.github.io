# pysetupdi.py Version 20201022-2
# https://github.com/gwangyi/pysetupdi

# MIT License
#
# Copyright (c) 2016 gwangyi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

def pysetupdi():
  '''\
Python SetupAPI Wrapper

`devices` function generates iterable of Devices which is selected by given parameters. The parameters of `devices`
is similar to SetupDiGetClassDevs. Properties of each device can be accessed by accessing pre-defined properties or
giving DevicePropertyKey object as an index to device object.

~~~python
hard_disk_drives = devices('{4d36e967-e325-11ce-bfc1-08002be10318}')
for hard_disk_drive in hard_disk_drives:
    print(hard_disk_drive.device_desc)
~~~

You can also query information about devices by console command

~~~
C:\> pysetupdi -g {4d36e967-e325-11ce-bfc1-08002be10318} list
C:\> pysetupdi -i "SCSI\DISK&VEN_SAMSUN_&PROD_MZNTE256HMHP-000\4&103D1686&0&000000" get pdo_name
~~~
'''
  class pysetupdi(object): pass
  pysetupdi = pysetupdi()
  if sys.platform != "win32": return pysetupdi

  ### structures.py

  _ole32 = ctypes.WinDLL('ole32')


  class _GUID(ctypes.Structure):
      _fields_ = [
          ('Data1', ctypes.c_uint32),
          ('Data2', ctypes.c_uint16),
          ('Data3', ctypes.c_uint16),
          ('Data4', ctypes.c_ubyte * 8)
      ]

      def __init__(self, guid="{00000000-0000-0000-0000-000000000000}"):
          super().__init__()
          if isinstance(guid, str):
              ret = _ole32.CLSIDFromString(ctypes.create_unicode_buffer(guid), ctypes.byref(self))
              if ret < 0:
                  err_no = ctypes.GetLastError()
                  raise WindowsError(err_no, ctypes.FormatError(err_no), guid)
          else:
              ctypes.memmove(ctypes.byref(self), bytes(guid), ctypes.sizeof(self))

      def __str__(self):
          s = ctypes.c_wchar_p()
          ret = _ole32.StringFromCLSID(ctypes.byref(self), ctypes.byref(s))
          if ret < 0:
              err_no = ctypes.GetLastError()
              raise WindowsError(err_no, ctypes.FormatError(err_no))
          ret = str(s.value)
          _ole32.CoTaskMemFree(s)
          return ret

      def __repr__(self):
          return "<GUID: {}>".format(str(self))

  assert ctypes.sizeof(_GUID) == 16


  class GUID(object):
      def __init__(self, guid="{00000000-0000-0000-0000-000000000000}"):
          self._guid = _GUID(guid)

      def __bytes__(self):
          return bytes(self._guid)

      def __str__(self):
          return str(self._guid)

      def __repr__(self):
          return repr(self._guid)

  class DevicePropertyKey(ctypes.Structure):
      # noinspection SpellCheckingInspection
      _fields_ = [
          ('fmtid', _GUID),
          ('pid', ctypes.c_ulong)
      ]

      def __init__(self, guid, pid, name=None):
          super().__init__()
          self.fmtid.__init__(guid)
          self.pid = pid
          self.name = name
          self.__doc__ = str(self)

      def __repr__(self):
          return "<DevPropKey: {}>".format(str(self))

      def __str__(self):
          if not hasattr(self, 'name') or self.name is None:
              # noinspection SpellCheckingInspection
              return "{} {}".format(self.fmtid, self.pid)
          else:
              # noinspection SpellCheckingInspection
              return "{}, {} {}".format(self.name, self.fmtid, self.pid)

      def __eq__(self, key):
          if not isinstance(key, DevicePropertyKey):
              return False
          return bytes(self) == bytes(key)


  class DeviceInfoData(ctypes.Structure):
      _fields_ = [
          ('cbSize', ctypes.c_ulong),
          ('ClassGuid', _GUID),
          ('DevInst', ctypes.c_ulong),
          ('Reserved', ctypes.c_void_p)
      ]

      def __init__(self):
          super().__init__()
          self.cbSize = ctypes.sizeof(self)

  DeviceInfoData.size = DeviceInfoData.cbSize
  DeviceInfoData.dev_inst = DeviceInfoData.DevInst
  DeviceInfoData.class_guid = DeviceInfoData.ClassGuid
  # noinspection SpellCheckingInspection
  SP_DEVINFO_DATA = DeviceInfoData
  # noinspection SpellCheckingInspection
  DEVPROPKEY = DevicePropertyKey

  ### constants.py

  """:mod:`pysetupdi.constants`

  Pre-defined constants from windows SDK
  """


  # noinspection SpellCheckingInspection
  class DiOpenDeviceInfo(enum.IntEnum):
      """DIOD_xxx constants
      """
      InheritClassDrvs = 2
      CancelRemove = 4


  # noinspection SpellCheckingInspection
  class DiGetClassDevsFlags(enum.IntEnum):
      """DIGCF_xxx constants
      """
      Default = 0x00000001
      Present = 0x00000002,
      AllClasses = 0x00000004,
      Profile = 0x00000008,
      DeviceInterface = 0x00000010,


  # noinspection SpellCheckingInspection
  class DevicePropertyKeys(object):
      """DEVPKEY_xxx constants"""
      NAME = DevicePropertyKey('{b725f130-47ef-101a-a5f1-02608c9eebac}', 10, 'DEVPKEY_NAME')
      Numa_Proximity_Domain = DevicePropertyKey('{540b947e-8b40-45bc-a8a2-6a0b894cbda2}', 1,
                                                'DEVPKEY_Numa_Proximity_Domain')

      # noinspection SpellCheckingInspection
      class Device(object):
          """DEVPKEY_Device_xxx constants"""
          DeviceDesc = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 2,
                                         'DEVPKEY_Device_DeviceDesc')
          HardwareIds = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 3,
                                          'DEVPKEY_Device_HardwareIds')
          CompatibleIds = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 4,
                                            'DEVPKEY_Device_CompatibleIds')
          Service = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 6,
                                      'DEVPKEY_Device_Service')
          Class = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 9,
                                    'DEVPKEY_Device_Class')
          ClassGuid = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 10,
                                        'DEVPKEY_Device_ClassGuid')
          Driver = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 11,
                                     'DEVPKEY_Device_Driver')
          ConfigFlags = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 12,
                                          'DEVPKEY_Device_ConfigFlags')
          Manufacturer = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 13,
                                           'DEVPKEY_Device_Manufacturer')
          FriendlyName = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 14,
                                           'DEVPKEY_Device_FriendlyName')
          LocationInfo = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 15,
                                           'DEVPKEY_Device_LocationInfo')
          PDOName = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 16,
                                      'DEVPKEY_Device_PDOName')
          Capabilities = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 17,
                                           'DEVPKEY_Device_Capabilities')
          UINumber = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 18,
                                       'DEVPKEY_Device_UINumber')
          UpperFilters = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 19,
                                           'DEVPKEY_Device_UpperFilters')
          LowerFilters = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 20,
                                           'DEVPKEY_Device_LowerFilters')
          BusTypeGuid = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 21,
                                          'DEVPKEY_Device_BusTypeGuid')
          LegacyBusType = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 22,
                                            'DEVPKEY_Device_LegacyBusType')
          BusNumber = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 23,
                                        'DEVPKEY_Device_BusNumber')
          EnumeratorName = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 24,
                                             'DEVPKEY_Device_EnumeratorName')
          Security = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 25,
                                       'DEVPKEY_Device_Security')
          SecuritySDS = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 26,
                                          'DEVPKEY_Device_SecuritySDS')
          DevType = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 27,
                                      'DEVPKEY_Device_DevType')
          Exclusive = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 28,
                                        'DEVPKEY_Device_Exclusive')
          Characteristics = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 29,
                                              'DEVPKEY_Device_Characteristics')
          Address = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 30,
                                      'DEVPKEY_Device_Address')
          UINumberDescFormat = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 31,
                                                 'DEVPKEY_Device_UINumberDescFormat')
          PowerData = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 32,
                                        'DEVPKEY_Device_PowerData')
          RemovalPolicy = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 33,
                                            'DEVPKEY_Device_RemovalPolicy')
          RemovalPolicyDefault = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 34,
                                                   'DEVPKEY_Device_RemovalPolicyDefault')
          RemovalPolicyOverride = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 35,
                                                    'DEVPKEY_Device_RemovalPolicyOverride')
          InstallState = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 36,
                                           'DEVPKEY_Device_InstallState')
          LocationPaths = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 37,
                                            'DEVPKEY_Device_LocationPaths')
          BaseContainerId = DevicePropertyKey('{a45c254e-df1c-4efd-8020-67d146a850e0}', 38,
                                              'DEVPKEY_Device_BaseContainerId')
          DevNodeStatus = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 2,
                                            'DEVPKEY_Device_DevNodeStatus')
          ProblemCode = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 3,
                                          'DEVPKEY_Device_ProblemCode')
          EjectionRelations = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 4,
                                                'DEVPKEY_Device_EjectionRelations')
          RemovalRelations = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 5,
                                               'DEVPKEY_Device_RemovalRelations')
          PowerRelations = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 6,
                                             'DEVPKEY_Device_PowerRelations')
          BusRelations = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 7,
                                           'DEVPKEY_Device_BusRelations')
          Parent = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 8,
                                     'DEVPKEY_Device_Parent')
          Children = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 9,
                                       'DEVPKEY_Device_Children')
          Siblings = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 10,
                                       'DEVPKEY_Device_Siblings')
          TransportRelations = DevicePropertyKey('{4340a6c5-93fa-4706-972c-7b648008a5a7}', 11,
                                                 'DEVPKEY_Device_TransportRelations')
          Reported = DevicePropertyKey('{80497100-8c73-48b9-aad9-ce387e19c56e}', 2,
                                       'DEVPKEY_Device_Reported')
          Legacy = DevicePropertyKey('{80497100-8c73-48b9-aad9-ce387e19c56e}', 3,
                                     'DEVPKEY_Device_Legacy')
          InstanceId = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 256,
                                         'DEVPKEY_Device_InstanceId')
          ContainerId = DevicePropertyKey('{8c7ed206-3f8a-4827-b3ab-ae9e1faefc6c}', 2,
                                          'DEVPKEY_Device_ContainerId')
          ModelId = DevicePropertyKey('{80d81ea6-7473-4b0c-8216-efc11a2c4c8b}', 2,
                                      'DEVPKEY_Device_ModelId')
          FriendlyNameAttributes = DevicePropertyKey('{80d81ea6-7473-4b0c-8216-efc11a2c4c8b}', 3,
                                                     'DEVPKEY_Device_FriendlyNameAttributes')
          ManufacturerAttributes = DevicePropertyKey('{80d81ea6-7473-4b0c-8216-efc11a2c4c8b}', 4,
                                                     'DEVPKEY_Device_ManufacturerAttributes')
          PresenceNotForDevice = DevicePropertyKey('{80d81ea6-7473-4b0c-8216-efc11a2c4c8b}', 5,
                                                   'DEVPKEY_Device_PresenceNotForDevice')
          DHP_Rebalance_Policy = DevicePropertyKey('{540b947e-8b40-45bc-a8a2-6a0b894cbda2}', 2,
                                                   'DEVPKEY_Device_DHP_Rebalance_Policy')
          Numa_Node = DevicePropertyKey('{540b947e-8b40-45bc-a8a2-6a0b894cbda2}', 3,
                                        'DEVPKEY_Device_Numa_Node')
          BusReportedDeviceDesc = DevicePropertyKey('{540b947e-8b40-45bc-a8a2-6a0b894cbda2}', 4,
                                                    'DEVPKEY_Device_BusReportedDeviceDesc')
          SessionId = DevicePropertyKey('{83da6326-97a6-4088-9453-a1923f573b29}', 6,
                                        'DEVPKEY_Device_SessionId')
          InstallDate = DevicePropertyKey('{83da6326-97a6-4088-9453-a1923f573b29}', 100,
                                          'DEVPKEY_Device_InstallDate')
          FirstInstallDate = DevicePropertyKey('{83da6326-97a6-4088-9453-a1923f573b29}', 101,
                                               'DEVPKEY_Device_FirstInstallDate')
          DriverDate = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 2,
                                         'DEVPKEY_Device_DriverDate')
          DriverVersion = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 3,
                                            'DEVPKEY_Device_DriverVersion')
          DriverDesc = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 4,
                                         'DEVPKEY_Device_DriverDesc')
          DriverInfPath = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 5,
                                            'DEVPKEY_Device_DriverInfPath')
          DriverInfSection = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 6,
                                               'DEVPKEY_Device_DriverInfSection')
          DriverInfSectionExt = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 7,
                                                  'DEVPKEY_Device_DriverInfSectionExt')
          MatchingDeviceId = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 8,
                                               'DEVPKEY_Device_MatchingDeviceId')
          DriverProvider = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 9,
                                             'DEVPKEY_Device_DriverProvider')
          DriverPropPageProvider = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 10,
                                                     'DEVPKEY_Device_DriverPropPageProvider')
          DriverCoInstallers = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 11,
                                                 'DEVPKEY_Device_DriverCoInstallers')
          ResourcePickerTags = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 12,
                                                 'DEVPKEY_Device_ResourcePickerTags')
          ResourcePickerExceptions = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 13,
                                                       'DEVPKEY_Device_ResourcePickerExceptions')
          DriverRank = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 14,
                                         'DEVPKEY_Device_DriverRank')
          DriverLogoLevel = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 15,
                                              'DEVPKEY_Device_DriverLogoLevel')
          NoConnectSound = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 17,
                                             'DEVPKEY_Device_NoConnectSound')
          GenericDriverInstalled = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 18,
                                                     'DEVPKEY_Device_GenericDriverInstalled')
          AdditionalSoftwareRequested = DevicePropertyKey('{a8b865dd-2e3d-4094-ad97-e593a70c75d6}', 19,
                                                          'DEVPKEY_Device_AdditionalSoftwareRequested')
          SafeRemovalRequired = DevicePropertyKey('{afd97640-86a3-4210-b67c-289c41aabe55}', 2,
                                                  'DEVPKEY_Device_SafeRemovalRequired')
          SafeRemovalRequiredOverride = DevicePropertyKey('{afd97640-86a3-4210-b67c-289c41aabe55}', 3,
                                                          'DEVPKEY_Device_SafeRemovalRequiredOverride')

      class DriverPackage(object):
          """DEVPKEY_DriverPackage_xxx constants"""
          Model = DevicePropertyKey('{cf73bb51-3abf-44a2-85e0-9a3dc7a12132}', 2,
                                    'DEVPKEY_DriverPackage_Model')
          VendorWebSite = DevicePropertyKey('{cf73bb51-3abf-44a2-85e0-9a3dc7a12132}', 3,
                                            'DEVPKEY_DriverPackage_VendorWebSite')
          DetailedDescription = DevicePropertyKey('{cf73bb51-3abf-44a2-85e0-9a3dc7a12132}', 4,
                                                  'DEVPKEY_DriverPackage_DetailedDescription')
          DocumentationLink = DevicePropertyKey('{cf73bb51-3abf-44a2-85e0-9a3dc7a12132}', 5,
                                                'DEVPKEY_DriverPackage_DocumentationLink')
          Icon = DevicePropertyKey('{cf73bb51-3abf-44a2-85e0-9a3dc7a12132}', 6,
                                   'DEVPKEY_DriverPackage_Icon')
          BrandingIcon = DevicePropertyKey('{cf73bb51-3abf-44a2-85e0-9a3dc7a12132}', 7,
                                           'DEVPKEY_DriverPackage_BrandingIcon')

      # noinspection SpellCheckingInspection
      class DeviceClass(object):
          """DEVPKEY_DeviceClass_xxx constants"""
          UpperFilters = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 19,
                                           'DEVPKEY_DeviceClass_UpperFilters')
          LowerFilters = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 20,
                                           'DEVPKEY_DeviceClass_LowerFilters')
          Security = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 25,
                                       'DEVPKEY_DeviceClass_Security')
          SecuritySDS = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 26,
                                          'DEVPKEY_DeviceClass_SecuritySDS')
          DevType = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 27,
                                      'DEVPKEY_DeviceClass_DevType')
          Exclusive = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 28,
                                        'DEVPKEY_DeviceClass_Exclusive')
          Characteristics = DevicePropertyKey('{4321918b-f69e-470d-a5de-4d88c75ad24b}', 29,
                                              'DEVPKEY_DeviceClass_Characteristics')
          Name = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 2,
                                   'DEVPKEY_DeviceClass_Name')
          ClassName = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 3,
                                        'DEVPKEY_DeviceClass_ClassName')
          Icon = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 4,
                                   'DEVPKEY_DeviceClass_Icon')
          ClassInstaller = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 5,
                                             'DEVPKEY_DeviceClass_ClassInstaller')
          PropPageProvider = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 6,
                                               'DEVPKEY_DeviceClass_PropPageProvider')
          NoInstallClass = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 7,
                                             'DEVPKEY_DeviceClass_NoInstallClass')
          NoDisplayClass = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 8,
                                             'DEVPKEY_DeviceClass_NoDisplayClass')
          SilentInstall = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 9,
                                            'DEVPKEY_DeviceClass_SilentInstall')
          NoUseClass = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 10,
                                         'DEVPKEY_DeviceClass_NoUseClass')
          DefaultService = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 11,
                                             'DEVPKEY_DeviceClass_DefaultService')
          IconPath = DevicePropertyKey('{259abffc-50a7-47ce-af08-68c9a7d73366}', 12,
                                       'DEVPKEY_DeviceClass_IconPath')
          DHPRebalanceOptOut = DevicePropertyKey('{d14d3ef3-66cf-4ba2-9d38-0ddb37ab4701}', 2,
                                                 'DEVPKEY_DeviceClass_DHPRebalanceOptOut')
          ClassCoInstallers = DevicePropertyKey('{713d1703-a2e2-49f5-9214-56472ef3da5c}', 2,
                                                'DEVPKEY_DeviceClass_ClassCoInstallers')

      class DeviceInterface(object):
          """DEVPKEY_DeviceInterface_xxx constants"""
          FriendlyName = DevicePropertyKey('{026e516e-b814-414b-83cd-856d6fef4822}', 2,
                                           'DEVPKEY_DeviceInterface_FriendlyName')
          Enabled = DevicePropertyKey('{026e516e-b814-414b-83cd-856d6fef4822}', 3,
                                      'DEVPKEY_DeviceInterface_Enabled')
          ClassGuid = DevicePropertyKey('{026e516e-b814-414b-83cd-856d6fef4822}', 4,
                                        'DEVPKEY_DeviceInterface_ClassGuid')

      class DeviceInterfaceClass(object):
          """DEVPKEY_DeviceInterfaceClass_xxx constants"""
          DefaultInterface = DevicePropertyKey('{14c83a99-0b3f-44b7-be4c-a178d3990564}', 2,
                                               'DEVPKEY_DeviceInterfaceClass_DefaultInterface')

      # noinspection SpellCheckingInspection
      class DeviceDisplay(object):
          """DEVPKEY_DeviceDisplay_xxx constants"""
          IsShowInDisconnectedState = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 0x44,
                                                        'DEVPKEY_DeviceDisplay_IsShowInDisconnectedState')
          IsNotInterestingForDisplay = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 0x4a,
                                                         'DEVPKEY_DeviceDisplay_IsNotInterestingForDisplay')
          Category = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 0x5a,
                                       'DEVPKEY_DeviceDisplay_Category')
          UnpairUninstall = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 0x62,
                                              'DEVPKEY_DeviceDisplay_UnpairUninstall')
          RequiresUninstallElevation = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 0x63,
                                                         'DEVPKEY_DeviceDisplay_RequiresUninstallElevation')
          AlwaysShowDeviceAsConnected = DevicePropertyKey('{78c34fc8-104a-4aca-9ea4-524d52996e57}', 0x65,
                                                          'DEVPKEY_DeviceDisplay_AlwaysShowDeviceAsConnected')


  # noinspection SpellCheckingInspection
  class DevicePropertyType(enum.IntEnum):
      """DEVPROP_TYPE_xxx, DEVPROP_TYPEMOD_xxx constants"""
      ModArray = 0x00001000  # array of fixed - sized data elements
      ModList = 0x00002000  # list of variable - sized data elements

      Empty = 0x00000000  # nothing, no property data
      Null = 0x00000001  # null property data
      Sbyte = 0x00000002  # 8 - bit signed int (SBYTE)
      Byte = 0x00000003  # 8 - bit unsigned int (BYTE)
      Int16 = 0x00000004  # 16-bit signed int (SHORT)
      Uint16 = 0x00000005  # 16-bit unsigned int (USHORT)
      Int32 = 0x00000006  # 32-bit signed int (LONG)
      Uint32 = 0x00000007  # 32-bit unsigned int (ULONG)
      Int64 = 0x00000008  # 64-bit signed int (LONG64)
      Uint64 = 0x00000009  # 64-bit unsigned int (ULONG64)
      Float = 0x0000000A  # 32 - bit floating - point (FLOAT)
      Double = 0x0000000B  # 64 - bit floating - point (DOUBLE)
      Decimal = 0x0000000C  # 128 - bit data (DECIMAL)
      Guid = 0x0000000D  # 128 - bit unique identifier (GUID)
      Currency = 0x0000000E  # 64 bit signed int currency value (CURRENCY)
      Date = 0x0000000F  # date (DATE)
      Filetime = 0x00000010  # file time (FILETIME)
      Boolean = 0x00000011  # 8 - bit boolean (DEVPROP_BOOLEAN)
      String = 0x00000012  # null - terminated string
      StringList = String | ModList  # multi-sz string list
      SecurityDescriptor = 0x00000013  # self - relative binary SECURITY_DESCRIPTOR
      SecurityDescriptorString = 0x00000014  # security descriptor string (SDDL format)
      DevicePropertyKey = 0x00000015  # device property key (DEVPROPKEY)
      DevicePropertyType = 0x00000016  # device property type (DEVPROPTYPE)
      Binary = Byte | ModArray  # custom binary data
      Error = 0x00000017  # 32 - bit Win32 system error code
      NtStatus = 0x00000018  # 32 - bit NTSTATUS code
      StringIndirect = 0x00000019  # string resource (@[path\] < dllname > , -<strId >)

      MaskType = 0x00000FFF  # range for base DEVPROP_TYPE_ values
      MaskTypeMod = 0x0000F000  # mask for DEVPROP_TYPEMOD_ type modifiers

      # noinspection SpellCheckingInspection
      MaxType = StringIndirect  # max valid DEVPROP_TYPE_ value
      # noinspection SpellCheckingInspection
      MaxTypeMod = ModList  # max valid DEVPROP_TYPEMOD_ value


  class FormatMessage(enum.IntEnum):
      """FORMAT_MESSAGE_xxx constants"""
      AllocateBuffer = 0x00000100
      IgnoreInserts = 0x00000200
      FromString = 0x00000400
      FromHmodule = 0x00000800
      FromSystem = 0x00001000
      ArgumentArray = 0x00002000
      MaxWidthMask = 0x000000FF


  # Below declarations makes C-like synonym of declared constants

  # noinspection SpellCheckingInspection
  DIGCF_DEFAULT = DiGetClassDevsFlags.Default
  # noinspection SpellCheckingInspection
  DIGCF_PRESENT = DiGetClassDevsFlags.Present
  # noinspection SpellCheckingInspection
  DIGCF_ALLCLASSES = DiGetClassDevsFlags.AllClasses
  # noinspection SpellCheckingInspection
  DIGCF_PROFILE = DiGetClassDevsFlags.Profile
  # noinspection SpellCheckingInspection
  DIGCF_DEVICEINTERFACE = DiGetClassDevsFlags.DeviceInterface

  # noinspection SpellCheckingInspection
  DEVPROP_TYPE = DevicePropertyType

  # noinspection SpellCheckingInspection
  DEVPROP_TYPEMOD_ARRAY = DevicePropertyType.ModArray  # array of fixed - sized data elements
  # noinspection SpellCheckingInspection
  DEVPROP_TYPEMOD_LIST = DevicePropertyType.ModList  # list of variable - sized data elements

  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_EMPTY = DevicePropertyType.Empty
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_NULL = DevicePropertyType.Null
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_SBYTE = DevicePropertyType.Sbyte
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_BYTE = DevicePropertyType.Byte
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_INT16 = DevicePropertyType.Int16
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_UINT16 = DevicePropertyType.Uint16
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_INT32 = DevicePropertyType.Int32
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_UINT32 = DevicePropertyType.Uint32
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_INT64 = DevicePropertyType.Int64
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_UINT64 = DevicePropertyType.Uint64
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_FLOAT = DevicePropertyType.Float
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_DOUBLE = DevicePropertyType.Double
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_DECIMAL = DevicePropertyType.Decimal
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_GUID = DevicePropertyType.Guid
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_CURRENCY = DevicePropertyType.Currency
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_DATE = DevicePropertyType.Date
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_FILETIME = DevicePropertyType.Filetime
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_BOOLEAN = DevicePropertyType.Boolean
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_STRING = DevicePropertyType.String
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_STRING_LIST = DevicePropertyType.StringList
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_SECURITY_DESCRIPTOR = DevicePropertyType.SecurityDescriptor
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_SECURITY_DESCRIPTOR_STRING = DevicePropertyType.SecurityDescriptorString
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_DEVPROPKEY = DevicePropertyType.DevicePropertyKey
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_DEVPROPTYPE = DevicePropertyType.DevicePropertyType
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_BINARY = DevicePropertyType.Binary
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_ERROR = DevicePropertyType.Error
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_NTSTATUS = DevicePropertyType.NtStatus
  # noinspection SpellCheckingInspection
  DEVPROP_TYPE_STRING_INDIRECT = DevicePropertyType.StringIndirect

  # noinspection SpellCheckingInspection
  MAX_DEVPROP_TYPE = DEVPROP_TYPE_STRING_INDIRECT  # max valid DEVPROP_TYPE_ value
  # noinspection SpellCheckingInspection
  MAX_DEVPROP_TYPEMOD = DEVPROP_TYPEMOD_LIST  # max valid DEVPROP_TYPEMOD_ value

  # noinspection SpellCheckingInspection
  DEVPROP_MASK_TYPE = DevicePropertyType.MaskType  # range for base DEVPROP_TYPE_ values
  # noinspection SpellCheckingInspection
  DEVPROP_MASK_TYPEMOD = DevicePropertyType.MaskTypeMod  # mask for DEVPROP_TYPEMOD_ type modifiers

  FORMAT_MESSAGE_ALLOCATE_BUFFER = FormatMessage.AllocateBuffer
  FORMAT_MESSAGE_IGNORE_INSERTS = FormatMessage.IgnoreInserts
  FORMAT_MESSAGE_FROM_STRING = FormatMessage.FromString
  FORMAT_MESSAGE_FROM_HMODULE = FormatMessage.FromHmodule
  FORMAT_MESSAGE_FROM_SYSTEM = FormatMessage.FromSystem
  FORMAT_MESSAGE_ARGUMENT_ARRAY = FormatMessage.ArgumentArray
  FORMAT_MESSAGE_MAX_WIDTH_MASK = FormatMessage.MaxWidthMask

  # noinspection SpellCheckingInspection
  DIOD_INHERIT_CLASSDRVS = DiOpenDeviceInfo.InheritClassDrvs
  # noinspection SpellCheckingInspection
  DIOD_CANCEL_REMOVE = DiOpenDeviceInfo.CancelRemove

  # noinspection SpellCheckingInspection
  DEVPKEY = DevicePropertyKeys

  # noinspection SpellCheckingInspection
  DEVPKEY_NAME = DevicePropertyKeys.NAME
  # noinspection SpellCheckingInspection
  DEVPKEY_Numa_Proximity_Domain = DevicePropertyKeys.Numa_Proximity_Domain

  DEVPKEY_Device_DeviceDesc = DevicePropertyKeys.Device.DeviceDesc
  DEVPKEY_Device_HardwareIds = DevicePropertyKeys.Device.HardwareIds
  DEVPKEY_Device_CompatibleIds = DevicePropertyKeys.Device.CompatibleIds
  DEVPKEY_Device_Service = DevicePropertyKeys.Device.Service
  DEVPKEY_Device_Class = DevicePropertyKeys.Device.Class
  DEVPKEY_Device_ClassGuid = DevicePropertyKeys.Device.ClassGuid
  DEVPKEY_Device_Driver = DevicePropertyKeys.Device.Driver
  DEVPKEY_Device_ConfigFlags = DevicePropertyKeys.Device.ConfigFlags
  DEVPKEY_Device_Manufacturer = DevicePropertyKeys.Device.Manufacturer
  DEVPKEY_Device_FriendlyName = DevicePropertyKeys.Device.FriendlyName
  DEVPKEY_Device_LocationInfo = DevicePropertyKeys.Device.LocationInfo
  DEVPKEY_Device_PDOName = DevicePropertyKeys.Device.PDOName
  DEVPKEY_Device_Capabilities = DevicePropertyKeys.Device.Capabilities
  DEVPKEY_Device_UINumber = DevicePropertyKeys.Device.UINumber
  DEVPKEY_Device_UpperFilters = DevicePropertyKeys.Device.UpperFilters
  DEVPKEY_Device_LowerFilters = DevicePropertyKeys.Device.LowerFilters
  DEVPKEY_Device_BusTypeGuid = DevicePropertyKeys.Device.BusTypeGuid
  DEVPKEY_Device_LegacyBusType = DevicePropertyKeys.Device.LegacyBusType
  DEVPKEY_Device_BusNumber = DevicePropertyKeys.Device.BusNumber
  DEVPKEY_Device_EnumeratorName = DevicePropertyKeys.Device.EnumeratorName
  DEVPKEY_Device_Security = DevicePropertyKeys.Device.Security
  DEVPKEY_Device_SecuritySDS = DevicePropertyKeys.Device.SecuritySDS
  DEVPKEY_Device_DevType = DevicePropertyKeys.Device.DevType
  DEVPKEY_Device_Exclusive = DevicePropertyKeys.Device.Exclusive
  DEVPKEY_Device_Characteristics = DevicePropertyKeys.Device.Characteristics
  DEVPKEY_Device_Address = DevicePropertyKeys.Device.Address
  DEVPKEY_Device_UINumberDescFormat = DevicePropertyKeys.Device.UINumberDescFormat
  DEVPKEY_Device_PowerData = DevicePropertyKeys.Device.PowerData
  DEVPKEY_Device_RemovalPolicy = DevicePropertyKeys.Device.RemovalPolicy
  DEVPKEY_Device_RemovalPolicyDefault = DevicePropertyKeys.Device.RemovalPolicyDefault
  DEVPKEY_Device_RemovalPolicyOverride = DevicePropertyKeys.Device.RemovalPolicyOverride
  DEVPKEY_Device_InstallState = DevicePropertyKeys.Device.InstallState
  DEVPKEY_Device_LocationPaths = DevicePropertyKeys.Device.LocationPaths
  DEVPKEY_Device_BaseContainerId = DevicePropertyKeys.Device.BaseContainerId
  DEVPKEY_Device_DevNodeStatus = DevicePropertyKeys.Device.DevNodeStatus
  DEVPKEY_Device_ProblemCode = DevicePropertyKeys.Device.ProblemCode
  DEVPKEY_Device_EjectionRelations = DevicePropertyKeys.Device.EjectionRelations
  DEVPKEY_Device_RemovalRelations = DevicePropertyKeys.Device.RemovalRelations
  DEVPKEY_Device_PowerRelations = DevicePropertyKeys.Device.PowerRelations
  DEVPKEY_Device_BusRelations = DevicePropertyKeys.Device.BusRelations
  DEVPKEY_Device_Parent = DevicePropertyKeys.Device.Parent
  DEVPKEY_Device_Children = DevicePropertyKeys.Device.Children
  DEVPKEY_Device_Siblings = DevicePropertyKeys.Device.Siblings
  DEVPKEY_Device_TransportRelations = DevicePropertyKeys.Device.TransportRelations
  DEVPKEY_Device_Reported = DevicePropertyKeys.Device.Reported
  DEVPKEY_Device_Legacy = DevicePropertyKeys.Device.Legacy
  DEVPKEY_Device_InstanceId = DevicePropertyKeys.Device.InstanceId
  DEVPKEY_Device_ContainerId = DevicePropertyKeys.Device.ContainerId
  DEVPKEY_Device_ModelId = DevicePropertyKeys.Device.ModelId
  DEVPKEY_Device_FriendlyNameAttributes = DevicePropertyKeys.Device.FriendlyNameAttributes
  DEVPKEY_Device_ManufacturerAttributes = DevicePropertyKeys.Device.ManufacturerAttributes
  DEVPKEY_Device_PresenceNotForDevice = DevicePropertyKeys.Device.PresenceNotForDevice
  # noinspection SpellCheckingInspection
  DEVPKEY_Device_DHP_Rebalance_Policy = DevicePropertyKeys.Device.DHP_Rebalance_Policy
  # noinspection SpellCheckingInspection
  DEVPKEY_Device_Numa_Node = DevicePropertyKeys.Device.Numa_Node
  DEVPKEY_Device_BusReportedDeviceDesc = DevicePropertyKeys.Device.BusReportedDeviceDesc
  DEVPKEY_Device_SessionId = DevicePropertyKeys.Device.SessionId
  DEVPKEY_Device_InstallDate = DevicePropertyKeys.Device.InstallDate
  DEVPKEY_Device_FirstInstallDate = DevicePropertyKeys.Device.FirstInstallDate
  DEVPKEY_Device_DriverDate = DevicePropertyKeys.Device.DriverDate
  DEVPKEY_Device_DriverVersion = DevicePropertyKeys.Device.DriverVersion
  DEVPKEY_Device_DriverDesc = DevicePropertyKeys.Device.DriverDesc
  DEVPKEY_Device_DriverInfPath = DevicePropertyKeys.Device.DriverInfPath
  DEVPKEY_Device_DriverInfSection = DevicePropertyKeys.Device.DriverInfSection
  DEVPKEY_Device_DriverInfSectionExt = DevicePropertyKeys.Device.DriverInfSectionExt
  DEVPKEY_Device_MatchingDeviceId = DevicePropertyKeys.Device.MatchingDeviceId
  DEVPKEY_Device_DriverProvider = DevicePropertyKeys.Device.DriverProvider
  DEVPKEY_Device_DriverPropPageProvider = DevicePropertyKeys.Device.DriverPropPageProvider
  DEVPKEY_Device_DriverCoInstallers = DevicePropertyKeys.Device.DriverCoInstallers
  DEVPKEY_Device_ResourcePickerTags = DevicePropertyKeys.Device.ResourcePickerTags
  DEVPKEY_Device_ResourcePickerExceptions = DevicePropertyKeys.Device.ResourcePickerExceptions
  DEVPKEY_Device_DriverRank = DevicePropertyKeys.Device.DriverRank
  DEVPKEY_Device_DriverLogoLevel = DevicePropertyKeys.Device.DriverLogoLevel
  DEVPKEY_Device_NoConnectSound = DevicePropertyKeys.Device.NoConnectSound
  DEVPKEY_Device_GenericDriverInstalled = DevicePropertyKeys.Device.GenericDriverInstalled
  DEVPKEY_Device_AdditionalSoftwareRequested = DevicePropertyKeys.Device.AdditionalSoftwareRequested
  DEVPKEY_Device_SafeRemovalRequired = DevicePropertyKeys.Device.SafeRemovalRequired
  DEVPKEY_Device_SafeRemovalRequiredOverride = DevicePropertyKeys.Device.SafeRemovalRequiredOverride

  DEVPKEY_DriverPackage_Model = DevicePropertyKeys.DriverPackage.Model
  DEVPKEY_DriverPackage_VendorWebSite = DevicePropertyKeys.DriverPackage.VendorWebSite
  DEVPKEY_DriverPackage_DetailedDescription = DevicePropertyKeys.DriverPackage.DetailedDescription
  DEVPKEY_DriverPackage_DocumentationLink = DevicePropertyKeys.DriverPackage.DocumentationLink
  DEVPKEY_DriverPackage_Icon = DevicePropertyKeys.DriverPackage.Icon
  DEVPKEY_DriverPackage_BrandingIcon = DevicePropertyKeys.DriverPackage.BrandingIcon

  DEVPKEY_DeviceClass_UpperFilters = DevicePropertyKeys.DeviceClass.UpperFilters
  DEVPKEY_DeviceClass_LowerFilters = DevicePropertyKeys.DeviceClass.LowerFilters
  DEVPKEY_DeviceClass_Security = DevicePropertyKeys.DeviceClass.Security
  DEVPKEY_DeviceClass_SecuritySDS = DevicePropertyKeys.DeviceClass.SecuritySDS
  DEVPKEY_DeviceClass_DevType = DevicePropertyKeys.DeviceClass.DevType
  DEVPKEY_DeviceClass_Exclusive = DevicePropertyKeys.DeviceClass.Exclusive
  DEVPKEY_DeviceClass_Characteristics = DevicePropertyKeys.DeviceClass.Characteristics
  DEVPKEY_DeviceClass_Name = DevicePropertyKeys.DeviceClass.Name
  DEVPKEY_DeviceClass_ClassName = DevicePropertyKeys.DeviceClass.ClassName
  DEVPKEY_DeviceClass_Icon = DevicePropertyKeys.DeviceClass.Icon
  DEVPKEY_DeviceClass_ClassInstaller = DevicePropertyKeys.DeviceClass.ClassInstaller
  DEVPKEY_DeviceClass_PropPageProvider = DevicePropertyKeys.DeviceClass.PropPageProvider
  DEVPKEY_DeviceClass_NoInstallClass = DevicePropertyKeys.DeviceClass.NoInstallClass
  DEVPKEY_DeviceClass_NoDisplayClass = DevicePropertyKeys.DeviceClass.NoDisplayClass
  DEVPKEY_DeviceClass_SilentInstall = DevicePropertyKeys.DeviceClass.SilentInstall
  DEVPKEY_DeviceClass_NoUseClass = DevicePropertyKeys.DeviceClass.NoUseClass
  DEVPKEY_DeviceClass_DefaultService = DevicePropertyKeys.DeviceClass.DefaultService
  DEVPKEY_DeviceClass_IconPath = DevicePropertyKeys.DeviceClass.IconPath
  # noinspection SpellCheckingInspection
  DEVPKEY_DeviceClass_DHPRebalanceOptOut = DevicePropertyKeys.DeviceClass.DHPRebalanceOptOut
  DEVPKEY_DeviceClass_ClassCoInstallers = DevicePropertyKeys.DeviceClass.ClassCoInstallers

  DEVPKEY_DeviceInterface_FriendlyName = DevicePropertyKeys.DeviceInterface.FriendlyName
  DEVPKEY_DeviceInterface_Enabled = DevicePropertyKeys.DeviceInterface.Enabled
  DEVPKEY_DeviceInterface_ClassGuid = DevicePropertyKeys.DeviceInterface.ClassGuid

  DEVPKEY_DeviceInterfaceClass_DefaultInterface = DevicePropertyKeys.DeviceInterfaceClass.DefaultInterface

  DEVPKEY_DeviceDisplay_IsShowInDisconnectedState = DevicePropertyKeys.DeviceDisplay.IsShowInDisconnectedState
  DEVPKEY_DeviceDisplay_IsNotInterestingForDisplay = DevicePropertyKeys.DeviceDisplay.IsNotInterestingForDisplay
  DEVPKEY_DeviceDisplay_Category = DevicePropertyKeys.DeviceDisplay.Category
  # noinspection SpellCheckingInspection
  DEVPKEY_DeviceDisplay_UnpairUninstall = DevicePropertyKeys.DeviceDisplay.UnpairUninstall
  DEVPKEY_DeviceDisplay_RequiresUninstallElevation = DevicePropertyKeys.DeviceDisplay.RequiresUninstallElevation
  DEVPKEY_DeviceDisplay_AlwaysShowDeviceAsConnected = DevicePropertyKeys.DeviceDisplay.AlwaysShowDeviceAsConnected

  ### property.py

  # noinspection SpellCheckingInspection
  """mod:`pysetupdi.property` - DEVPROP parser

  Parsing given devprop buffer and type and return python object
  """


  # noinspection SpellCheckingInspection
  _oleaut32 = ctypes.WinDLL('oleaut32')
  _kernel32 = ctypes.WinDLL('kernel32')


  class Property(object):
      """Property parser class"""
      _property_type = dict()  # type: typing.Dict[int, (bytes,) -> object]
      """Property parser objects are placed in this class property"""

      def __new__(cls, buffer, prop_type):
          # noinspection SpellCheckingInspection
          """
          Parse devprop property

          :param buffer: given byte buffer
          :type buffer: bytes
          :param prop_type: DEVPROP_TYPE_xxx type
          :type prop_type: int | DevicePropertyType
          :return: python object
          """
          return Property._property_type[prop_type](buffer)

      @classmethod
      def add_parser(cls, prop_type, length=None, func=None):
          # noinspection SpellCheckingInspection
          """
          Add DEVPROP_TYPE_xxx handler

          :param prop_type: DEVPROP_TYPE_xxx type
          :type prop_type: int | DevicePropertyType
          :param length: If specified, given prop_type support DEVPROP_TYPEMOD_ARRAY modifier and
              unit size is given value
          :type length: None | int
          :param func: real parser
          :type func: (bytes,) -> object
          """
          def decorator(f):
              cls._property_type[prop_type] = f
              if length is not None:
                  def array_parser(buffer):
                      return list(f(buffer[i:i+length] for i in range(0, len(buffer), length)))

                  cls._property_type[prop_type | DEVPROP_TYPEMOD_ARRAY] = array_parser

              return f

          if func is None:
              return decorator
          else:
              return decorator(func)

  def _add_parsers():
      """Add default parsers
      To make each parser be hidden to other modules, each parsers are defined as local function of this function"""

      # noinspection PyUnusedLocal
      @Property.add_parser(DEVPROP_TYPE_EMPTY)
      def empty_parser(buffer):
          # noinspection SpellCheckingInspection
          """DEVPROP_TYPE_EMPTY parser

          Actually, in this case, the attribute does not exists, so it raises `AttributeError`"""
          raise AttributeError("Empty property")

      # noinspection PyUnusedLocal
      @Property.add_parser(DEVPROP_TYPE_NULL)
      def null_parser(buffer):
          # noinspection SpellCheckingInspection
          """DEVPROP_TYPE_NULL parser"""
          return None

      # noinspection SpellCheckingInspection
      @Property.add_parser(DEVPROP_TYPE_SBYTE)
      def sbyte_parser(buffer):
          """DEVPROP_TYPE_SBYTE parser

          Every element of default python byte array is signed byte, so just return first element"""
          return buffer[0]

      # noinspection SpellCheckingInspection
      @Property.add_parser(DEVPROP_TYPE_SBYTE | DEVPROP_TYPEMOD_ARRAY)
      @Property.add_parser(DEVPROP_TYPE_SECURITY_DESCRIPTOR)
      def sbyte_array_parser(buffer):
          """DEVPROP_TYPE_BINARY parser

          Although SECURITY_DESCRIPTOR need to its own parser, the structure of it varies to windows versions and it is
          not used so frequently. So, it handles same as bytes
          """
          return buffer

      @Property.add_parser(DEVPROP_TYPE_BYTE)
      def byte_parser(buffer):
          # noinspection SpellCheckingInspection
          """DEVPROP_TYPE_BYTE parser

          Default python bytes is signed, so to use given bytes as an unsigned byte value, truncate bits above 8th."""
          return buffer[0] & 255

      # noinspection SpellCheckingInspection
      @Property.add_parser(DEVPROP_TYPE_BYTE | DEVPROP_TYPEMOD_ARRAY)
      def sbyte_array_parser(buffer):
          """DEVPROP_TYPE_BYTE | DEVPROP_TYPEMOD_ARRAY parser

          Default python bytes is signed, so to use given bytes as an unsigned byte value, truncate bits above 8th."""
          return tuple(n & 255 for n in buffer)

      def add_simple_type_parser(prop_type, fmt):
          def simple_parser(buffer):
              return array.array(fmt, buffer)[0]

          def array_parser(buffer):
              return list(array.array(fmt, buffer))

          Property.add_parser(prop_type)(simple_parser)
          Property.add_parser(prop_type | DEVPROP_TYPEMOD_ARRAY)(array_parser)

      def add_simple_type_parsers(fmt_map):
          for prop_type in fmt_map:
              fmt = fmt_map[prop_type]
              add_simple_type_parser(prop_type, fmt)

      add_simple_type_parsers({
          DEVPROP_TYPE_INT16: 'h',
          DEVPROP_TYPE_UINT16: 'H',
          DEVPROP_TYPE_INT32: 'l',
          DEVPROP_TYPE_UINT32: 'L',
          DEVPROP_TYPE_INT64: 'q',
          DEVPROP_TYPE_UINT64: 'Q',
          DEVPROP_TYPE_FLOAT: 'f',
          DEVPROP_TYPE_DOUBLE: 'd',
          DEVPROP_TYPE_DEVPROPKEY: 'L',
      })

      @Property.add_parser(DEVPROP_TYPE_DECIMAL, length=16)
      def decimal_parser(buffer):
          # noinspection SpellCheckingInspection
          scale, sign, hi, lo = struct.unpack("xxBBHQ", buffer[:16])
          val = (hi << 64) | lo
          val *= 1 if sign & 0x80 == 0 else -1
          return val / (10 ** scale)

      @Property.add_parser(DEVPROP_TYPE_GUID, length=16)
      def guid_parser(buffer):
          return GUID(buffer[:16])

      @Property.add_parser(DEVPROP_TYPE_CURRENCY, length=8)
      def currency_parser(buffer):
          return struct.unpack('Q', buffer[:8])[0] / 10000

      @Property.add_parser(DEVPROP_TYPE_DATE, length=8)
      def date_parser(buffer):
          t = struct.unpack('d', buffer[:8])[0]
          buf = ctypes.create_string_buffer(16)
          _oleaut32.VartiantTimeToSystemTime(t, ctypes.byref(buf))
          y, m, _, d, hh, mm, ss, ms = struct.unpack("8H", bytes(buf))
          return datetime.datetime(y, m, d, hh, mm, ss, ms * 1000)

      @Property.add_parser(DEVPROP_TYPE_FILETIME, length=8)
      def filetime_parser(buffer):
          buf = ctypes.create_string_buffer(16)
          _kernel32.FileTimeToSystemTime(buffer[:8], ctypes.byref(buf))
          y, m, _, d, hh, mm, ss, ms = struct.unpack("8H", bytes(buf))
          return datetime.datetime(y, m, d, hh, mm, ss, ms * 1000)

      @Property.add_parser(DEVPROP_TYPE_BOOLEAN, length=1)
      def boolean_parser(buffer):
          return buffer[0] != 0

      @Property.add_parser(DEVPROP_TYPE_STRING)
      @Property.add_parser(DEVPROP_TYPE_SECURITY_DESCRIPTOR_STRING)
      @Property.add_parser(DEVPROP_TYPE_STRING_INDIRECT)
      def string_parser(buffer):
          return buffer.decode('utf-16').split('\0', 1)[0]

      @Property.add_parser(DEVPROP_TYPE_STRING_LIST)
      @Property.add_parser(DEVPROP_TYPE_SECURITY_DESCRIPTOR_STRING | DEVPROP_TYPEMOD_LIST)
      def string_list_parser(buffer):
          return buffer.decode('utf-16').strip('\0\0').split('\0')

      # noinspection SpellCheckingInspection
      @Property.add_parser(DEVPROP_TYPE_DEVPROPKEY, length=ctypes.sizeof(DevicePropertyKey))
      def devpropkey_parser(buffer):
          return DevicePropertyKey.from_buffer(bytearray(buffer))

      @Property.add_parser(DEVPROP_TYPE_ERROR)
      def error_parser(buffer):
          err_no = struct.unpack("l", buffer[:4])
          return err_no, ctypes.FormatError(err_no)

      @Property.add_parser(DEVPROP_TYPE_ERROR | DEVPROP_TYPEMOD_ARRAY)
      def error_array_parser(buffer):
          return list((err_no, ctypes.FormatError(err_no)) for err_no in array.array('l', buffer))

      # noinspection SpellCheckingInspection
      def _ntstatus_format_error(ntstatus):
          if ntstatus > 0x80000000:
              ntstatus -= 0x100000000
          msg_ptr = ctypes.c_wchar_p()
          ntdll = _kernel32.LoadLibraryW('NTDLL.DLL')
          try:
              _kernel32.FormatMessageW(FORMAT_MESSAGE_ALLOCATE_BUFFER |
                                       FORMAT_MESSAGE_FROM_SYSTEM |
                                       FORMAT_MESSAGE_FROM_HMODULE,
                                       ntdll, ntstatus, 0x0400,  # LANG_NEUTRAL, SUBLANG_DEFAULT
                                       ctypes.byref(msg_ptr), 0, None)
              return msg_ptr.value.replace("\r\n", "\n").strip("\n")
          finally:
              if msg_ptr.value is not None:
                  _kernel32.LocalFree(msg_ptr)
              _kernel32.FreeLibrary(ntdll)

      # noinspection SpellCheckingInspection
      @Property.add_parser(DEVPROP_TYPE_NTSTATUS)
      def ntstatus_parser(buffer):
          err_no = struct.unpack("l", buffer[:4])[0]
          return err_no, _ntstatus_format_error(err_no)

      # noinspection SpellCheckingInspection
      @Property.add_parser(DEVPROP_TYPE_NTSTATUS | DEVPROP_TYPEMOD_ARRAY)
      def ntstatus_array_parser(buffer):
          return list((err_no, _ntstatus_format_error(err_no)) for err_no in array.array('l', buffer))

  _add_parsers()

  ### setupdi.py

  # noinspection SpellCheckingInspection
  _setupapi = ctypes.WinDLL('setupapi')
  _kernel32 = ctypes.WinDLL('kernel32')

  """
  WINSETUPAPI HDEVINFO SetupDiGetClassDevsW(
    const GUID *ClassGuid,
    PCWSTR     Enumerator,
    HWND       hwndParent,
    DWORD      Flags
  );
  """
  _setupapi.SetupDiGetClassDevsW.restype = ctypes.c_void_p
  """
  WINSETUPAPI BOOL SetupDiDestroyDeviceInfoList(
    HDEVINFO DeviceInfoSet
  );
  """
  _setupapi.SetupDiDestroyDeviceInfoList.argtypes = [ctypes.c_void_p]
  """
  WINSETUPAPI BOOL SetupDiEnumDeviceInfo(
    HDEVINFO         DeviceInfoSet,
    DWORD            MemberIndex,
    PSP_DEVINFO_DATA DeviceInfoData
  );
  """
  _setupapi.SetupDiEnumDeviceInfo.argtypes = [ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]
  """
  WINSETUPAPI BOOL SetupDiGetDevicePropertyW(
    HDEVINFO         DeviceInfoSet,
    PSP_DEVINFO_DATA DeviceInfoData,
    const DEVPROPKEY *PropertyKey,
    DEVPROPTYPE      *PropertyType,
    PBYTE            PropertyBuffer,
    DWORD            PropertyBufferSize,
    PDWORD           RequiredSize,
    DWORD            Flags
  );
  """
  _setupapi.SetupDiGetDevicePropertyW.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p, ctypes.c_uint]
  """
  WINSETUPAPI HDEVINFO SetupDiCreateDeviceInfoList(
    const GUID *ClassGuid,
    HWND       hwndParent
  );
  """
  _setupapi.SetupDiCreateDeviceInfoList.restype = ctypes.c_void_p
  """
  WINSETUPAPI BOOL SetupDiOpenDeviceInfoW(
    HDEVINFO         DeviceInfoSet,
    PCWSTR           DeviceInstanceId,
    HWND             hwndParent,
    DWORD            OpenFlags,
    PSP_DEVINFO_DATA DeviceInfoData
  );
  """
  _setupapi.SetupDiOpenDeviceInfoW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_void_p, ctypes.c_uint, ctypes.c_void_p]


  class DeviceType(type):
      def __new__(mcs, what, bases, member):
          properties = member.get('_properties_', [])
          for pair in properties:
              name, prop_key = pair
              if not isinstance(prop_key, DevicePropertyKey):
                  prop_key = DevicePropertyKey(*str(prop_key).split(' '))

              def getter_closer(prop_key_, name_):
                  def getter(self):
                      if name_ not in self.__dict__:
                          self.__dict__[name_] = self.get_property(prop_key_)
                      return self.__dict__[name_]
                  return getter
              member[name] = property(getter_closer(prop_key, name))
          return type.__new__(mcs, what, bases, member)


  class Device(metaclass=DeviceType):
      pdo_name = ""

      """A class of device"""
      def __init__(self, instance_id):
          """
          Create python Device instance that is associated to device which is specified by given instance id

          :param instance_id: Instance Id of device
          """
          self._handle = None  # SetupDi Device Info List handle and SP_DEVINFO_DATA pair
          self._instance_id = instance_id

      @contextlib.contextmanager
      def open(self):
          """
          Open device to query properties

          :return: context
          """
          handle = _setupapi.SetupDiCreateDeviceInfoList(None, None)
          if handle == -1:
              err_no = ctypes.GetLastError()
              raise WindowsError(err_no, ctypes.FormatError(err_no))
          try:
              dev_info = DeviceInfoData()
              if not _setupapi.SetupDiOpenDeviceInfoW(handle, ctypes.create_unicode_buffer(self._instance_id), None,
                                                      DIOD_INHERIT_CLASSDRVS, ctypes.byref(dev_info)):
                  err_no = ctypes.GetLastError()
                  raise WindowsError(err_no, ctypes.FormatError(err_no))
              self._handle = (handle, dev_info, self._handle)  # Stack
              yield self
          finally:
              if self._handle is not None and \
                              self._handle[0] == handle:  # If last handle is opened in this function, pop it
                  self._handle = self._handle[2]
              _setupapi.SetupDiDestroyDeviceInfoList(handle)  # Close handle

      def get_property(self, key):
          """
          Get device property. See SetupDiGetDeviceProperty from MSDN

          :param key: Key of property
          :return: Property value
          """
          if self._handle is None:  # If the device is not opened yet,
              with self.open():  # Open and retry
                  return self.get_property(key)

          handle, dev_info, _ = self._handle
          prop_type = ctypes.c_ulong()
          required_size = ctypes.c_ulong()
          value = None

          if isinstance(key, DevicePropertyKey):  # If given key is an instance of DEVPROPKEY
              key_ = ctypes.byref(key)

              # Property query function is SetupDiGetDeviceProperty
              get_property_ = _setupapi.SetupDiGetDevicePropertyW
          else:
              raise TypeError("Key must be DevPropKey instance, but {} given".format(key))

          # To retrieve buffer size.
          if not get_property_(handle, ctypes.byref(dev_info),
                               key_,
                               ctypes.byref(prop_type),
                               None, 0, ctypes.byref(required_size), 0):
              err_no = ctypes.GetLastError()
              if err_no == 122:  # ERROR_INSUFFICIENT_BUFFER
                  value_buffer = ctypes.create_string_buffer(required_size.value)
                  if get_property_(handle, ctypes.byref(dev_info),
                                   key_,
                                   ctypes.byref(prop_type),
                                   ctypes.byref(value_buffer),
                                   required_size.value, ctypes.byref(required_size), 0):
                      # Parse property value with retrieved property type
                      value = Property(bytes(value_buffer), prop_type.value)
                  err_no = ctypes.GetLastError()

              if err_no == 1168:  # ERROR_NOT_FOUND: Attribute is not exist
                  raise AttributeError(key)
              if err_no != 0:
                  raise WindowsError(err_no, ctypes.FormatError(err_no))
          return value

      def __getitem__(self, prop_key):
          """
          Alias of get_property

          :param prop_key: Key of property
          :return: Property value
          """
          return self.get_property(prop_key)

      def get_property_keys(self):
          """
          Get all device property keys

          :return: Iterable of device property keys
          """
          if self._handle is None:
              with self.open():
                  return self.get_property_keys()

          handle, dev_info, _ = self._handle
          required_size = ctypes.c_ulong()
          if not _setupapi.SetupDiGetDevicePropertyKeys(handle, ctypes.byref(dev_info), None, 0,
                                                        ctypes.byref(required_size), 0):
              err_no = ctypes.GetLastError()
              if err_no == 122:  # ERROR_INSUFFICIENT_BUFFER
                  # noinspection SpellCheckingInspection
                  devpkeys = (DevicePropertyKey * required_size.value)()
                  if _setupapi.SetupDiGetDevicePropertyKeys(handle, ctypes.byref(dev_info), ctypes.byref(devpkeys),
                                                            required_size.value, None, 0):
                      return list(devpkeys)
                  err_no = ctypes.GetLastError()

              raise WindowsError(err_no, ctypes.FormatError(err_no))
          return []

      @property
      def path(self):
          """
          Return device file path with PDO name

          :return: file path that can be opened by CreateFile
          """
          # noinspection SpellCheckingInspection
          return r'\\?\GLOBALROOT' + self.pdo_name

      @property
      def parent(self):
          """
          Parent device of this device on device tree

          :return: Parent device
          """
          return Device(self.get_property(DevicePropertyKeys.Device.Parent))

      @property
      def children(self):
          """
          Child devices of this device on device tree

          :return: List of child devices
          """
          return list(Device(child_id) for child_id in self.get_property(DevicePropertyKeys.Device.Children))

      @property
      def siblings(self):
          """
          Sibling devices of this device on device tree

          :return: List of sibling devices
          """
          return list(Device(sibling_id) for sibling_id in self.get_property(DevicePropertyKeys.Device.Siblings))

      # noinspection SpellCheckingInspection
      _properties_ = [
          ('device_desc', DevicePropertyKeys.Device.DeviceDesc),
          ('hardware_id', DevicePropertyKeys.Device.HardwareIds),
          ('compatible_ids', DevicePropertyKeys.Device.CompatibleIds),
          ('service', DevicePropertyKeys.Device.Service),
          ('device_class', DevicePropertyKeys.Device.Class),
          ('class_guid', DevicePropertyKeys.Device.ClassGuid),
          ('driver', DevicePropertyKeys.Device.Driver),
          ('config_flags', DevicePropertyKeys.Device.ConfigFlags),
          ('manufacturer', DevicePropertyKeys.Device.Manufacturer),
          ('friendly_name', DevicePropertyKeys.Device.FriendlyName),
          ('location_info', DevicePropertyKeys.Device.LocationInfo),
          ('pdo_name', DevicePropertyKeys.Device.PDOName),
          ('capabilities', DevicePropertyKeys.Device.Capabilities),
          ('ui_number', DevicePropertyKeys.Device.UINumber),
          ('upper_filters', DevicePropertyKeys.Device.UpperFilters),
          ('lower_filters', DevicePropertyKeys.Device.LowerFilters),
          ('bus_type_guid', DevicePropertyKeys.Device.BusTypeGuid),
          ('legacy_bus_type', DevicePropertyKeys.Device.LegacyBusType),
          ('bus_number', DevicePropertyKeys.Device.BusNumber),
          ('enumerator_name', DevicePropertyKeys.Device.EnumeratorName),
          ('security', DevicePropertyKeys.Device.Security),
          ('security_sds', DevicePropertyKeys.Device.SecuritySDS),
          ('dev_type', DevicePropertyKeys.Device.DevType),
          ('exclusive', DevicePropertyKeys.Device.Exclusive),
          ('characteristics', DevicePropertyKeys.Device.Characteristics),
          ('address', DevicePropertyKeys.Device.Address),
          ('ui_number_desc_format', DevicePropertyKeys.Device.UINumberDescFormat),
          ('power_data', DevicePropertyKeys.Device.PowerData),
          ('removal_policy', DevicePropertyKeys.Device.RemovalPolicy),
          ('removal_policy_default', DevicePropertyKeys.Device.RemovalPolicyDefault),
          ('removal_policy_override', DevicePropertyKeys.Device.RemovalPolicyOverride),
          ('install_state', DevicePropertyKeys.Device.InstallState),
          ('location_paths', DevicePropertyKeys.Device.LocationPaths),
          ('base_container_id', DevicePropertyKeys.Device.BaseContainerId),
          ('dev_node_status', DevicePropertyKeys.Device.DevNodeStatus),
          ('problem_code', DevicePropertyKeys.Device.ProblemCode),
          ('ejection_relations', DevicePropertyKeys.Device.EjectionRelations),
          ('removal_relations', DevicePropertyKeys.Device.RemovalRelations),
          ('power_relations', DevicePropertyKeys.Device.PowerRelations),
          ('bus_relations', DevicePropertyKeys.Device.BusRelations),
          # ('parent', DevicePropertyKeys.Device.Parent),
          # ('children', DevicePropertyKeys.Device.Children),
          # ('siblings', DevicePropertyKeys.Device.Siblings),
          ('transport_relations', DevicePropertyKeys.Device.TransportRelations),
          ('reported', DevicePropertyKeys.Device.Reported),
          ('legacy', DevicePropertyKeys.Device.Legacy),
          ('instance_id', DevicePropertyKeys.Device.InstanceId),
          ('container_id', DevicePropertyKeys.Device.ContainerId),
          ('model_id', DevicePropertyKeys.Device.ModelId),
          ('friendly_name_attributes', DevicePropertyKeys.Device.FriendlyNameAttributes),
          ('manufacturer_attributes', DevicePropertyKeys.Device.ManufacturerAttributes),
          ('presence_not_for_device', DevicePropertyKeys.Device.PresenceNotForDevice),
          ('dhp_rebalance_policy', DevicePropertyKeys.Device.DHP_Rebalance_Policy),
          ('numa_node', DevicePropertyKeys.Device.Numa_Node),
          ('bus_reported_device_desc', DevicePropertyKeys.Device.BusReportedDeviceDesc),
          ('session_id', DevicePropertyKeys.Device.SessionId),
          ('install_date', DevicePropertyKeys.Device.InstallDate),
          ('first_install_date', DevicePropertyKeys.Device.FirstInstallDate),
          ('driver_date', DevicePropertyKeys.Device.DriverDate),
          ('driver_version', DevicePropertyKeys.Device.DriverVersion),
          ('driver_desc', DevicePropertyKeys.Device.DriverDesc),
          ('driver_inf_path', DevicePropertyKeys.Device.DriverInfPath),
          ('driver_inf_section', DevicePropertyKeys.Device.DriverInfSection),
          ('driver_inf_section_ext', DevicePropertyKeys.Device.DriverInfSectionExt),
          ('matching_device_id', DevicePropertyKeys.Device.MatchingDeviceId),
          ('driver_provider', DevicePropertyKeys.Device.DriverProvider),
          ('driver_prop_page_provider', DevicePropertyKeys.Device.DriverPropPageProvider),
          ('driver_co_installers', DevicePropertyKeys.Device.DriverCoInstallers),
          ('resource_picker_tags', DevicePropertyKeys.Device.ResourcePickerTags),
          ('resource_picker_exceptions', DevicePropertyKeys.Device.ResourcePickerExceptions),
          ('driver_rank', DevicePropertyKeys.Device.DriverRank),
          ('driver_logo_level', DevicePropertyKeys.Device.DriverLogoLevel),
          ('no_connect_sound', DevicePropertyKeys.Device.NoConnectSound),
          ('generic_driver_installed', DevicePropertyKeys.Device.GenericDriverInstalled),
          ('additional_software_requested', DevicePropertyKeys.Device.AdditionalSoftwareRequested),
          ('safe_removal_required', DevicePropertyKeys.Device.SafeRemovalRequired),
          ('safe_removal_required_override', DevicePropertyKeys.Device.SafeRemovalRequiredOverride),
      ]

      def __str__(self):
          """
          Device name

          :return: Friendly name or device description of instance id of device
          """
          try:
              return self.friendly_name
          except AttributeError:
              try:
                  return self.device_desc
              except AttributeError:
                  return self._instance_id

      def __repr__(self):
          return "<pysetupdi.Device: {}>".format(str(self))


  def devices(guid=None, enumerator=None, hwnd_parent=None, flags=DIGCF_PRESENT):
      """
      Return generator of `Device` objects which is specified by given parameters
      Parameters are almost same to SetupDiGetClassDev's

      :param guid: A string that describes the GUID for a device setup class or a device interface class.
          The format of GUID string is same to CLSIDFromString.
      :param enumerator: An ID of a PnP enumerator.
      :param hwnd_parent: A handle to the top-level window. This handle is optional and can be None
      :param flags: A variable of type DWORD that specifies control options.
      :return: Iterable of Device objects
      """
      if guid is None:
          guid_ = None
          flags |= DIGCF_ALLCLASSES
      elif isinstance(guid, GUID):
          guid_ = bytes(guid)
      else:
          guid_ = bytes(GUID(str(guid)))

      if enumerator is None:
          enumerator_ = None
      else:
          enumerator_ = ctypes.create_unicode_buffer(enumerator)

      handle = _setupapi.SetupDiGetClassDevsW(guid_, enumerator_, hwnd_parent, flags)
      if handle == -1:
          err_no = ctypes.GetLastError()
          raise WindowsError(err_no, ctypes.FormatError(err_no), (guid, enumerator, flags))

      try:
          idx = 0
          dev_info = DeviceInfoData()
          while _setupapi.SetupDiEnumDeviceInfo(handle, idx, ctypes.byref(dev_info)):
              idx += 1
              prop_type = ctypes.c_ulong()
              required_size = ctypes.c_ulong()
              instance_id = None
              if not _setupapi.SetupDiGetDevicePropertyW(handle, ctypes.byref(dev_info),
                                                         ctypes.byref(DEVPKEY.Device.InstanceId),
                                                         ctypes.byref(prop_type),
                                                         None, 0, ctypes.byref(required_size), 0):
                  err_no = ctypes.GetLastError()
                  if err_no == 122:  # ERROR_INSUFFICIENT_BUFFER
                      instance_id_buffer = ctypes.create_string_buffer(required_size.value)
                      if _setupapi.SetupDiGetDevicePropertyW(handle, ctypes.byref(dev_info),
                                                             ctypes.byref(DEVPKEY.Device.InstanceId),
                                                             ctypes.byref(prop_type),
                                                             ctypes.byref(instance_id_buffer),
                                                             required_size.value, ctypes.byref(required_size), 0):
                          instance_id = Property(bytes(instance_id_buffer), prop_type.value)
                      err_no = ctypes.GetLastError()
                  if err_no != 0:
                      raise WindowsError(err_no, ctypes.FormatError(err_no))
              yield Device(instance_id)

          err_no = ctypes.GetLastError()
          if err_no != 259:
              raise WindowsError(err_no, ctypes.FormatError(err_no), (guid, enumerator, flags))

      finally:
          _setupapi.SetupDiDestroyDeviceInfoList(handle)

  for k,v in locals().items(): setattr(pysetupdi, k, v)
  return pysetupdi
pysetupdi = pysetupdi()

pysetupdi._required_globals = [
  "array",
  "ctypes",
  "contextlib",
  "datetime",
  "enum",
  "typing",
  "struct",
  "sys",
]
