#class O(object):
#  def __init__(self, chunks):
#    self.chunks = chunks
#    self.index = 0
#  def read(self, fd, n):
#    return self.chunks.pop(0) if self.chunks else b""
#  def lseek(self, fd, p, w):
#    self.index += p
#    return self.index
#  SEEK_CUR = 1
#
#print(os_read(None, 2, os_module=O([b"ab", b"cd"])), b"ab")
#print(os_read(None, 4, os_module=O([b"ab", b"cd"])), b"ab")
#print(os_read(None, 4, exact=True, os_module=O([b"ab", b"cd"])), b"abcd")
#print(os_read(None, 4, exact=True, os_module=O([b"ab", b"cd"])), b"abcd")
#print(os_read(None, 4, seek=True, exact=True, os_module=O([b"ab", b"cd"])), b"abcd")
#
#import os
#fd = os.open("\\\\.\\PhysicalDrive0", os.O_BINARY)
#print(os_read(fd, 1024)[:10])
#print(os_read(fd, 1024)[:10])
#print(os_read(fd, 1024)[:10])
