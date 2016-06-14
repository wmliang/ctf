from z3 import *
import string

def str_to_bv(s):
    return [BitVecVal(ord(i), 8) for i in list(s)]

def bv_to_str(s):
    return ''.join([chr(i.as_long()) for i in s])

def gen_str(size, cand=None):
    bytes = [BitVec('s%d' % i, 8) for i in range(size)]
    if cand == None:
        return bytes, And([And(0x20 <= x, x <= 0x7f) for x in bytes])
    else:
        return bytes, And([Or([x == ord(c) for c in cand]) for x in bytes])

def pp(v):
    return hex(simplify(v).as_long())




def xor(v1, v2):
    return v1^v2

def swap_byte(a1, a2, a3):
    v1 = (LShR(a1, 8*a2)&0xFF) << 8*a3
    v2 = (LShR(a1, 8*a3)&0xFF) << 8*a2
    m = ~(255 << 8 * a2) & ~(255 << 8 * a3) & a1
    return v1 | v2 | m

def ror(a1, a2):
    return RotateRight(a1, a2)

def rol(a1, a2):
    return RotateLeft(a1, a2)

def func1(a1):
    v0 = ((a1 << 56) ^ a1) & 0xFF00000000000000
    v1 = (LShR(a1 & 0xFF00, 8) ^ a1)&0xFF
    v2 = (LShR(a1 & 0xFF0000, 8) ^ a1) & 0xFF00
    v3 = (LShR(a1 & 0xFF000000, 8) ^ a1) & 0xFF0000
    v4 = (LShR(a1 & 0xFF00000000, 8) ^ a1) & 0xFF000000
    v5 = (LShR(a1 & 0xFF0000000000, 8) ^ a1) & 0xFF00000000
    v6 = (LShR(a1 & 0xFF000000000000, 8) ^ a1) & 0xFF0000000000
    v7 = (LShR(a1 & 0xFF00000000000000, 8) ^ a1) & 0xFF000000000000
    v = v0 | v1 | v2 | v3 | v4 | v5 | v6 | v7
    return v

def permuate(a1):
    p1 = LShR(a1 & 0xFF00000000000000, 8)
    p2 = LShR(a1 & 0xFF000000000000, 40)
    p3 = LShR(a1 & 0xFF0000000000, 40)
    p4 = LShR(a1 & 0xFF00000000, 16)
    p5 = (a1 & 0xFF000000) << 16
    p6 = (a1 & 0xFF0000) << 40
    p7 = (a1 & 0xFF00) << 24
    p8 = (a1 << 24) & 0xFFFFFFFF
    p = p1 | p2 | p3 | p4 | p5 | p6 | p7 | p8
    return p

def enc1(a1):
  v1 = xor(a1, 0x35966A685C73335A)
  v2 = swap_byte(v1, 2, 0)
  v3 = xor(v2, 0x89FDAF6604952DF1)
  v4 = xor(v3, 0xE9F30F0CE704876A)
  v5 = swap_byte(v4, 2, 3)
  v6 = xor(v5, 0xBDC5026D3C0B56E6)
  v7 = rol(v6, 16)
  v8 = rol(v7, 35)
  v9 = ror(v8, 19)
  v10 = func1(v9)
  v11 = rol(v10, 36)
  v12 = ror(v11, 40)
  v13 = swap_byte(v12, 1, 0)
  v14 = xor(v13, 0x5DE229FB3804DB17)
  v15 = permuate(v14)
  v16 = permuate(v15)
  v17 = swap_byte(v16, 2, 1)
  v18 = xor(v17, 0x6AAD877366E921F5)
  v19 = swap_byte(v18, 3, 0)
  v20 = permuate(v19)
  v21 = xor(v20, 0x58D83E9D5E6D5083)
  v22 = ror(v21, 22)
  v23 = func1(v22)
  v24 = xor(v23, 0x47B4D980070A9B73)
  v25 = func1(v24)
  v26 = func1(v25)
  v27 = swap_byte(v26, 6, 5)
  v28 = rol(v27, 59)
  v29 = swap_byte(v28, 5, 2)
  v30 = swap_byte(v29, 2, 3)
  v31 = rol(v30, 12)
  v32 = xor(v31, 0xAD25307F8E364B17)
  v33 = xor(v32, 0x48A56D5AFE0DA4C2)
  v34 = rol(v33, 6)
  v35 = swap_byte(v34, 6, 5)
  v36 = ror(v35, 11)
  v37 = permuate(v36)
  v38 = xor(v37, 0x869365DB4C9F3CB6)
  v39 = permuate(v38)
  v40 = ror(v39, 2)
  v41 = xor(v40, 0x4085AA8C0693425B)
  v42 = rol(v41, 35)
  v43 = rol(v42, 9)
  v44 = func1(v43)
  v45 = rol(v44, 7)
  v46 = rol(v45, 38)
  v47 = func1(v46)
  v48 = xor(v47, 0xDEF2D72447EF4E1B)
  v49 = permuate(v48)
  v50 = permuate(v49)
  v51 = swap_byte(v50, 2, 7)
  v52 = ror(v51, 51)
  v53 = permuate(v52)
  v54 = ror(v53, 19)
  v55 = xor(v54, 0x95DE49591A44EE21)
  v56 = func1(v55)
  v57 = permuate(v56)
  return ror(v57, 16)

def enc2(a1):
  v1 = rol(a1, 22)
  v2 = permuate(v1)
  v3 = swap_byte(v2, 4, 1)
  v4 = permuate(v3)
  v5 = func1(v4)
  v6 = rol(v5, 35)
  v7 = swap_byte(v6, 2, 6)
  v8 = xor(v7, 0x80A9EA4F90944FEA)
  v9 = rol(v8, 3)
  v10 = swap_byte(v9, 0, 1)
  v11 = swap_byte(v10, 1, 2)
  v12 = permuate(v11)
  v13 = func1(v12)
  v14 = swap_byte(v13, 5, 1)
  v15 = ror(v14, 24)
  v16 = rol(v15, 39)
  v17 = swap_byte(v16, 2, 4)
  v18 = xor(v17, 0x678E70A16230A437)
  v19 = swap_byte(v18, 4, 3)
  v20 = swap_byte(v19, 0, 7)
  v21 = rol(v20, 62)
  v22 = permuate(v21)
  v23 = swap_byte(v22, 7, 6)
  v24 = swap_byte(v23, 2, 6)
  v25 = permuate(v24)
  v26 = func1(v25)
  v27 = swap_byte(v26, 5, 2)
  v28 = func1(v27)
  v29 = swap_byte(v28, 1, 7)
  v30 = xor(v29, 0x41EA5CF418A918E7)
  v31 = permuate(v30)
  v32 = func1(v31)
  v33 = swap_byte(v32, 1, 4)
  v34 = rol(v33, 10)
  v35 = permuate(v34)
  v36 = permuate(v35)
  v37 = ror(v36, 24)
  v38 = swap_byte(v37, 0, 4)
  v39 = ror(v38, 61)
  v40 = swap_byte(v39, 3, 4)
  v41 = ror(v40, 35)
  v42 = rol(v41, 55)
  v43 = rol(v42, 34)
  v44 = func1(v43)
  v45 = func1(v44)
  v46 = ror(v45, 23)
  v47 = rol(v46, 59)
  v48 = ror(v47, 20)
  v49 = rol(v48, 28)
  v50 = xor(v49, 0xC26499379C0927CD)
  v51 = func1(v50)
  return ror(v51, 13)

def enc3(a1):
  v1 = rol(a1, 18)
  v2 = rol(v1, 29)
  v3 = swap_byte(v2, 5, 3)
  v4 = swap_byte(v3, 0, 7)
  v5 = rol(v4, 18)
  v6 = xor(v5, 0xC9AB604BB92038AD)
  v7 = ror(v6, 33)
  v8 = swap_byte(v7, 0, 4)
  v9 = func1(v8)
  v10 = swap_byte(v9, 6, 2)
  v11 = ror(v10, 13)
  v12 = ror(v11, 20)
  v13 = xor(v12, 0x58609BE21EB37866)
  v14 = func1(v13)
  v15 = permuate(v14)
  v16 = ror(v15, 46)
  v17 = swap_byte(v16, 2, 3)
  v18 = ror(v17, 44)
  v19 = ror(v18, 3)
  v20 = swap_byte(v19, 4, 3)
  v21 = func1(v20)
  v22 = swap_byte(v21, 7, 6)
  v23 = ror(v22, 59)
  v24 = ror(v23, 38)
  v25 = permuate(v24)
  v26 = swap_byte(v25, 1, 5)
  v27 = permuate(v26)
  v28 = rol(v27, 27)
  v29 = xor(v28, 0xBED577A97EB7966F)
  v30 = ror(v29, 14)
  v31 = rol(v30, 7)
  v32 = rol(v31, 18)
  v33 = rol(v32, 57)
  v34 = xor(v33, 0xB44427BE7889C31B)
  v35 = xor(v34, 0xCE745C65ABECB66)
  v36 = xor(v35, 0x94B1608ADB7F7221)
  v37 = xor(v36, 0x85BEF139817EBC4A)
  v38 = swap_byte(v37, 5, 1)
  v39 = rol(v38, 20)
  v40 = rol(v39, 24)
  v41 = ror(v40, 46)
  v42 = ror(v41, 13)
  v43 = xor(v42, 0xC95E5C35034B9775)
  v44 = rol(v43, 7)
  v45 = xor(v44, 0x8E60900383FA5EA)
  v46 = xor(v45, 0x59D5BCBF8B0CC9FD)
  v47 = func1(v46)
  v48 = swap_byte(v47, 4, 7)
  v49 = func1(v48)
  v50 = ror(v49, 22)
  v51 = ror(v50, 50)
  return func1(v51)

def enc4(a1):
  v1 = swap_byte(a1, 1, 7)
  v2 = rol(v1, 6)
  v3 = swap_byte(v2, 2, 5)
  v4 = ror(v3, 57)
  v5 = xor(v4, 0xC852FA4047662CE)
  v6 = swap_byte(v5, 5, 1)
  v7 = rol(v6, 1)
  v8 = func1(v7)
  v9 = xor(v8, 0x5DDFC2422C2A449E)
  v10 = func1(v9)
  v11 = rol(v10, 6)
  v12 = func1(v11)
  v13 = rol(v12, 33)
  v14 = ror(v13, 25)
  v15 = func1(v14)
  v16 = xor(v15, 0xA94A4C87A942C60)
  v17 = swap_byte(v16, 6, 2)
  v18 = func1(v17)
  v19 = xor(v18, 0xCC508FA31A0DA5AB)
  v20 = xor(v19, 0x880218B9F910DCBC)
  v21 = func1(v20)
  v22 = xor(v21, 0x85D7E666ECDBA611)
  v23 = ror(v22, 8)
  v24 = ror(v23, 43)
  v25 = xor(v24, 0x633A915BD59AC97B)
  v26 = swap_byte(v25, 3, 1)
  v27 = swap_byte(v26, 5, 7)
  v28 = permuate(v27)
  v29 = func1(v28)
  v30 = ror(v29, 59)
  v31 = ror(v30, 10)
  v32 = func1(v31)
  v33 = swap_byte(v32, 2, 1)
  v34 = swap_byte(v33, 7, 2)
  v35 = func1(v34)
  v36 = xor(v35, 0x648FFF323D235735)
  v37 = xor(v36, 0xFC9F8D635FD85EB3)
  v38 = xor(v37, 0xFF651571C16E5CB3)
  v39 = swap_byte(v38, 2, 4)
  v40 = swap_byte(v39, 5, 4)
  v41 = ror(v40, 11)
  v42 = func1(v41)
  v43 = rol(v42, 39)
  v44 = permuate(v43)
  v45 = func1(v44)
  v46 = xor(v45, 0xC798D4E5C0E97B1C)
  v47 = permuate(v46)
  v48 = func1(v47)
  v49 = rol(v48, 35)
  v50 = swap_byte(v49, 3, 5)
  v51 = func1(v50)
  v52 = permuate(v51)
  return func1(v52)









def checksum(flag):
    s = [BitVecVal(0, 64) for i in range(4)]
    enc = [enc1, enc2, enc3, enc4]
    for j in range(4):
        for i in range(8):
            s[j] = s[j] + (ZeroExt(56, flag[j*8+i]) << i*8)
        s[j] = enc[j](s[j])
    return s[0]^s[1]^s[2]^s[3]

def test():
    flag = 'AaaaaaaaBaaaaaaaCaaaaaaaDaaaaaaa'
    print 'checksum = ' + pp(checksum(str_to_bv(flag)))

def go():
    n = 32
    print 'flag length = %d' % n
    cand = [chr(i) for i in range(0x41, 0x7b)]+[' ']
    cand.remove(']')
    cand.remove('\\')
    cand.remove('^')
    cand.remove('`')
    cand.remove('[')

    flag, constraints = gen_str(n, cand)
    sum_ = checksum(flag)

    s = Solver()
    s.add(sum_ == 0xB101124831C0110A, constraints)

    if s.check() == sat:
        m = s.model()
        sol = ''.join(chr(m[i].as_long()) for i in flag)
        # ZQB RILJMGHPyLXs F _  u DXzMJbBU
        print pp(checksum(str_to_bv(sol))), sol
    else:
        print 'unsat'

if __name__ == '__main__':
#    test()
    go()
