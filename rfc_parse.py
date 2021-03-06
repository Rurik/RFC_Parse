import os
import struct
import sys
# RecentFileCacheParser - @bbaskin
# Similar stuff:
# https://github.com/sysforensics/RecentFileCacheParser/blob/master/rfcparse.py
# http://www.forensickb.com/2013/12/encase-enscript-to-parse-recent.html

def readRFC(fname):
    magics = [b'\xfe\xff\xee\xff', b'\x11\x22\x00\x00', b'\x03\x00\x00\x00', b'\x01\x00\x00\x00']
    entries = []
    filesize = os.path.getsize(fname)
    if filesize <= 20:
        return ''

    with open(fname,'rb') as fh:
        for i in range(0, len(magics)):
            header = fh.read(4)
            if not header == magics[i]:
                fh.close()
                return ''
        volumeID = fh.read(4) # Disregard this value
        
        while fh.tell() < filesize:
            tmp_buffer = fh.read(4)
            entry_len = (struct.unpack('<i', tmp_buffer)[0]) * 2 # For unicode
            entry = fh.read(entry_len)
            entries.append(entry)
            fh.read(2) # Disregard last two unicode null terminators as they break in decode
    fh.close()
    return entries
    
def main():
    print(sys.argv[1])
    data = readRFC(sys.argv[1])
    print(len(data))
    for entry in data:
        print(entry.decode('utf-16'))

if __name__ == '__main__':
    main()