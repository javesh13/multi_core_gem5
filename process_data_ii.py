import sys, copy
from collections import Counter
if(len(sys.argv) < 2):
    print("Please supply file name")

count =  0
source_file = open(sys.argv[1], "r")
cache_list = []
pc_list = []
delta_list = []

"""
Now we want those deltas suck that by including them we can cover up atleast 50% deltas.
"""
coverage_percentage = 90
min_frq_to_be_valid = 10
freq_gt = 0
while True:
    line = source_file.readline()

    if not line:
        break
    count += 1
    line = line.strip()
    c,p,d = line.split(",")

    cache_list.append(c)
    pc_list.append(p)
    delta_list.append(d)

    if int(d, 10) >= min_frq_to_be_valid:
        freq_gt+=1

freq_distribution = Counter(delta_list)



# print(freq_gt_10)

print("Total deltas are ", len(delta_list))
print("Total Unique deltas are {}".format(len(freq_distribution)))
print("Total deltas that appear more than {} times are ".format(min_frq_to_be_valid), freq_gt)

"""
Now we want those deltas such that by including them we can cover up atleast 90 % deltas.
"""
coverage_percentage = 90


my_list = [(key, val) for key, val in freq_distribution.items()]


my_list.sort(key = lambda x: x[1], reverse=True)
print("Delta {} has the highest freq of {}".format(my_list[0][0], my_list[0][1]))
top_deltas = []
current_count = 0
print((coverage_percentage*len(delta_list)) //100)
for i in range(len(my_list)):
    if current_count <= (coverage_percentage*len(delta_list)) //100:
        #include current delta in vocabulary
        top_deltas.append(my_list[i][0])
        current_count += my_list[i][1]
    else:
        top_deltas.append(my_list[i][0])
        current_count += my_list[i][1]
        break
        


print("Number of top deltas that cover {}% of total deltas are {}".format(coverage_percentage, len(top_deltas)))


source_file.close()

result_file = open(sys.argv[1]+"_final_data.csv", "w")
source_file = open(sys.argv[1], "r")


result_file.write("Cache,PC,Delta\n")
written_line = 0
not_written_line = 0

while True:
    line = source_file.readline()
    
    if not line:
        break
    line = line.strip()
    a, b, c = line.split(",") 

  
    if freq_distribution[c] >= min_frq_to_be_valid:#if this delta occurs at least 10 times then only we need to consider this
        written_line+=1
        result_file.write("{},{},{}\n ".format(int(a, 10), int(b, 10), int(c, 10)))
    elif freq_distribution[c] < min_frq_to_be_valid:
        # print(freq_distribution[c],  " < " , min_frq_to_be_valid) 
        not_written_line += 1
    


print("wrote {} line in result_ii.txt".format(written_line))
print("skipped {} line in result_ii.txt".format(not_written_line))
source_file.close()
result_file.close()


vocab_file = open(sys.argv[1]+"_vocab_deltas.txt", "w")

vocab_file.write("top_deltas\n")

for x in top_deltas:
    vocab_file.write(x+"\n")

vocab_file.close()

