import mmap

with open('/dev/uio0','r+b') as f:
        map = mmap.mmap(f.fileno(),4096)
        map.write_byte('A')
        map.write_byte('1')
        map.write_byte('1')
        map.write_byte('1')
        
        map.write_byte('1')
        map.write_byte('1')
        map.write_byte('1')
        map.write_byte('2')

        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')

        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        map.write_byte('2')
        
        map.seek(0)
        print map.readline()
        print map.size()
f.close()
