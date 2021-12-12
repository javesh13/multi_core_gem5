#!/usr/bin/python3
import sys, re, os
from collections import deque

# if len(sys.argv) < 2:
#     print("SCRIPT INPUT_FILE OUTPUT_FILE")


# print(sys.argv[1])
result_file = open(sys.argv[1], "w")

source_file = sys.stdin


add_list = []
final_data = []
count = 0
prev_val = 0
q = deque()

with sys.stdin as f:
    for line in f:
        if(len(line) == 0):
            continue
        x = re.search("0x[a-f0-9]*", line)
        if( x == None):
            
            continue
        # pbar.update(len(line))
        addr = x.group()
        # print(addr)
        if "PC" in line:
            pc = addr

            for addr in add_list:
                delta = str(hex(int(addr, 16) - prev_val))
                q.append((int(addr, 16), int(pc, 16)))

            # print("Entering")
            while len(q) != 1:
                
                addr = q[0][0]
                pc = q[0][1]
                delta = q[1][0] - addr 
                result_file.write("{},{},{}\n".format(addr, pc, delta))
                q.popleft()
            add_list.clear()   
        else:
            # if addr not in add_list:
            add_list.append(addr)

source_file.close()
result_file.close()

