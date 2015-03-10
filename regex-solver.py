from z3 import *
import re
import sys


def str2int(ss):
    mapping = {'p':1, 'l':2, 'a':4, 'i':8, 'd':16, 'c':32, 't':64, 'f':128}
    v = 0
    for c in ss:
        v = v + mapping[c]
    return v

def parse(s):
    global array, sol
    t_idx = 0
    s_idx = 0
    expr = []
    while s_idx < len(s):
#        print "debug, len(s) = "+str(len(s))+", s_idx = " + str(s_idx) + ", t_idx = " + str(t_idx) 
        if s[s_idx] == '.':
            if s_idx == len(s) - 1:
                t_idx = t_idx + 1
                s_idx = s_idx + 1
                continue
            if s[s_idx+1] == '{':
                start = s_idx + 2
                s_idx = s.find('}', s_idx)
#                print "debug, t_idx += " + s[start:s_idx]
                t_idx = t_idx + int(s[start:s_idx])
                s_idx = s_idx + 1
            else:
                t_idx = t_idx + 1
                s_idx = s_idx + 1
            continue
        if s[s_idx] == '[':
            start = s_idx + 1
            s_idx = s.find(']', s_idx)
#            print "table["+str(t_idx)+"] got " + s[start:s_idx]
            expr.append(array[t_idx] & str2int(s[start:s_idx]) == 0)
            s_idx = s_idx + 1
            t_idx = t_idx + 1
    if (s_idx != len(s)) or (t_idx != 171):
        print "ERROR1"
        exit()

    if len(expr) == 2:
        sol.add( Or(expr[0], expr[1]) )
    elif len(expr) == 3:
        sol.add( Or(expr[0], expr[1], expr[2]) )
    else:
        print "ERROR2"
        exit()
        


buf = open('regex.txt', 'r').read().strip()[34:][:-2].split('|')
array = [BitVec('a%i'%i, 8) for i in range(171)]
sol = Solver()

line_num = 1
for i in buf:
    print "line_num = " + str(line_num)
    parse(i.strip())
    line_num = line_num + 1




for i in range(171):
    sol.add(Or(array[i] == 1, array[i] == 2, array[i] == 4, array[i] == 8, array[i] == 16, array[i] == 32, array[i] == 64, array[i] == 128))

if sol.check() == unsat:
    print "unsat"
    exit()

m = sol.model()
mapping = {1:'p', 2:'l', 4:'a', 8:'i', 16:'d', 32:'c', 64:'t', 128:'f'}
idx = 1
for i in range(171):
    v = int(str(m[BitVec('a%i'%i, 8)]))
    if v not in mapping:
        print "mapping not found"
        continue
    print str(idx) + ":\t" + mapping[v]
    idx = idx + 1

# key = cddliadtatddtcfidafatdaccafddiadpifdicdfldcltiftpdafpaddfdcddipaapfdptapiptaatipccllpttdcitpdpdtapptfcppfdftccfialctdalccftaadlffaffpfpdiiditpacildctdapfiddftclacdpidlpilp

