import sys

def ROL(data, shift, size=32):
    shift %= size
    remains = data >> (size - shift)
    body = (data << shift) - (remains << size )
    return (body + remains)
     
 
def ROR(data, shift, size=32):
    shift %= size
    body = data >> shift
    remains = (data << (size - shift)) - (body << size)
    return (body + remains)

def wut_encode1(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = ROR(((~new4 & 0xFFFFFFFF) & newc) | (new8 & new4), 0x19) ^ new0
        v = (v + new4) & 0xFFFFFFFF
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += buf[idx+0xc:idx+0x10] + line + buf[idx+4:idx+8] + buf[idx+8:idx+0xc]
    return new

def wut_encode2(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = ROR(((~newc & 0xFFFFFFFF) & new8) | (new4 & newc), 0x19) ^ new0
        v = (v + new4) & 0xFFFFFFFF
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += buf[idx+0xc:idx+0x10] + line + buf[idx+4:idx+8] + buf[idx+8:idx+0xc]
    return new

def wut_encode3(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = ROR((new4 ^ new8) ^ newc, 0x19) ^ new0
        v = (v + new4) & 0xFFFFFFFF
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += buf[idx+0xc:idx+0x10] + line + buf[idx+4:idx+8] + buf[idx+8:idx+0xc]
    return new

def wut_encode4(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = ROR(((~newc & 0xFFFFFFFF) | new4) ^ new8, 0x19) ^ new0
        v = (v + new4) & 0xFFFFFFFF
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += buf[idx+0xc:idx+0x10] + line + buf[idx+4:idx+8] + buf[idx+8:idx+0xc]
    return new

def rearrange(arr):
    c = int(pow(len(arr), 0.5)) - 1
    buf = []
    for j in range(c+1):
        idx = c - j
        for i in range((len(arr)/c)-1):
            try:
                buf.append(arr[idx])
            except:
                print "error, idx = " + hex(idx)
            idx = idx + (c+1)
    return buf

def dump(buf):
    n = 0
    for i in buf:
        if (n%16==0):
            sys.stdout.write("\n")
        sys.stdout.write("0x"+i+" ")
        n = n + 1
    sys.stdout.write("\n")


# encode
input = "p"*256

buf = []
for i in range((len(input)/16)*16):
    buf.append("00")
i = 0
for j in input:
    buf[i] = j.encode('hex')
    i = i + 1

for i in range(128):
    dump(buf)
    j = i & 0x3F
    if j > 0x1F:
        if (i & 0x1F) < 0x10:
            print "encode3"
            buf = rearrange(wut_encode3(buf))
        else:
            print "encode4"
            buf = rearrange(wut_encode4(buf))
    else:
        if (i & 0x1F) < 0x10:
            print "encode1"
            buf = rearrange(wut_encode1(buf))
        else:
            print "encode2"
            buf = rearrange(wut_encode2(buf))
dump(buf)



# decode
print "Decoding ..."

def wut_decode1(buf):
#    print "before wut_decode1" ; dump(buf)
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = (new4-new8)&0xFFFFFFFF
        v = v ^ ROR(((~new8 & 0xFFFFFFFF) & new0) | (newc & new8), 0x19)
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += line + buf[idx+8:idx+0xc] + buf[idx+0xc:idx+0x10] + buf[idx+0:idx+4]
    return new

def wut_decode2(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = (new4-new8)&0xFFFFFFFF
        v = v ^ ROR(((~new0 & 0xFFFFFFFF) & newc) | (new8 & new0), 0x19)
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += line + buf[idx+8:idx+0xc] + buf[idx+0xc:idx+0x10] + buf[idx+0:idx+4]
    return new

def wut_decode3(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = (new4-new8) & 0xFFFFFFFF
        v = v ^ ROR((new8 ^ newc) ^ new0, 0x19)
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += line + buf[idx+8:idx+0xc] + buf[idx+0xc:idx+0x10] + buf[idx+0:idx+4]
    return new

def wut_decode4(buf):
    new = []
    for k in range(len(buf)/16):
        idx = k * 16
        new0 = int("".join(buf[idx+0:idx+4][::-1]), 16)
        new4 = int("".join(buf[idx+4:idx+8][::-1]), 16)
        new8 = int("".join(buf[idx+8:idx+0xc][::-1]), 16)
        newc = int("".join(buf[idx+0xc:idx+0x10][::-1]), 16)
        v = (new4-new8) & 0xFFFFFFFF
        v = v ^ ROR(((~new0 & 0xFFFFFFFF) | new8) ^ newc, 0x19)
        line = format(v, 'x').zfill(8)
        line = [line[i:i+2] for i in range(0, len(line), 2)][::-1]
        new += line + buf[idx+8:idx+0xc] + buf[idx+0xc:idx+0x10] + buf[idx+0:idx+4]
    return new

def unrearrange(arr):
    c = int(pow(len(arr), 0.5)) - 1
    buf = []
    for k in arr:
        buf.append(k)
    for j in range(c+1):
        idx = c - j
        for i in range((len(buf)/c)-1):
            try:
                buf[idx] = arr[0]
                del arr[0]
            except:
                print "error, idx = " + hex(idx)
            idx = idx + (c+1)
    return buf

encrypted = [
0x54,  0x68,  0x65,  0x20,  0x66,  0x6c,  0x61,  0x67, 
0x20,  0x69,  0x73,  0x20,  0x2a,  0x6e,  0x6f,  0x74, 
0x2a,  0x20,  0x70,  0x6f,  0x6f,  0x70,  0x2c,  0x20, 
0x62,  0x75,  0x74,  0x20,  0x79,  0x6f,  0x75,  0x20, 
0x63,  0x61,  0x6e,  0x20,  0x74,  0x72,  0x79,  0x20, 
0x74,  0x68,  0x61,  0x74,  0x20,  0x61,  0x6e,  0x79, 
0x77,  0x61,  0x79,  0x20,  0x62,  0x65,  0x63,  0x61, 
0x75,  0x73,  0x65,  0x20,  0x79,  0x6f,  0x75,  0x20, 
0x73,  0x74,  0x72,  0x69,  0x6e,  0x67,  0x73,  0x27, 
0x64,  0x20,  0x74,  0x68,  0x69,  0x73,  0x20,  0x62, 
0x69,  0x6e,  0x61,  0x72,  0x79,  0x20,  0x61,  0x6e, 
0x64,  0x20,  0x73,  0x61,  0x77,  0x20,  0x73,  0x6f, 
0x6d,  0x65,  0x74,  0x68,  0x69,  0x6e,  0x67,  0x20, 
0x74,  0x68,  0x61,  0x74,  0x20,  0x6c,  0x6f,  0x6f, 
0x6b,  0x65,  0x64,  0x20,  0x69,  0x6e,  0x74,  0x65, 
0x72,  0x65,  0x73,  0x74,  0x69,  0x6e,  0x67,  0x20, 
0x61,  0x6e,  0x64,  0x20,  0x6a,  0x75,  0x73,  0x74, 
0x20,  0x68,  0x61,  0x64,  0x20,  0x74,  0x6f,  0x20, 
0x74,  0x72,  0x79,  0x20,  0x69,  0x74,  0x2e,  0x2e, 
0x2e,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00, 
0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,  0x00,
]


buf = []
for i in encrypted:
    buf.append(hex(i)[2:].zfill(2))

for i in range(127,-1,-1):
    dump(buf)
    j = i & 0x3F
    if j > 0x1F:
        if (i & 0x1F) < 0x10:
            print "decode3"
            buf = wut_decode3(unrearrange(buf))
        else:
            print "decode4"
            buf = wut_decode4(unrearrange(buf))
    else:
        if (i & 0x1F) < 0x10:
            print "decode1"
            buf = wut_decode1(unrearrange(buf))
        else:
            print "decode2"
            buf = wut_decode2(unrearrange(buf))
dump(buf)

key = ""
for i in buf:
    key += i
print "\n./jumble " + key
