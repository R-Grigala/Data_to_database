class Data:
    def __init__(self,date,st,p_fa,p_time,sfa,s_time,s_p,sour_t,eph,epr,t_p,t_s,t_S,):
        pass




lines = []

with open('199207', 'r') as f:
    for line in f:
        if line.endswith(','):
            lines.append(line)
        else:
            line = line.strip()+','
            lines.append(line)

temp_lines_data = []
temp_lines_total = []

empty_count = 0

for x in range(len(lines)):
    line = lines[x].replace(",,",",")
    if line.startswith(','):
        temp_list = []
        change = True
        for z in line:
            if change:
                change = False
                continue
            else:
                temp_list.append(z)
        line = ''.join(temp_list)

    if len(line) < 50:
        if line == '':
            empty_count +=1
            if empty_count >= 2:
                continue

            temp_lines_total.append("SSSSS")
            temp_lines_data.append("SSSSS")
        else:
            empty_count = 0
            temp_lines_total.append(line)
    else:
        temp_lines_data.append(line)

able = True


lines_total = []

temp_list = []

for x in temp_lines_total:
    if x == "SSSSS":
        lines_total.append(temp_list)
        temp_list = []
    else:
        temp_list.append(x)

for x in lines_total:
    print(x)

for x in temp_lines_data:
    test_list = x.split(',')
    #if len(test_list) == 23:
    if "*" in test_list[0]:
        print(len(test_list),test_list)

# lines_data = []

# temp_list = []

# for x in temp_lines_data:
#     if x == "SSSSS":
#         lines_data.append(temp_list)
#         temp_list = []
#     else:
#         temp_list.append(x)

# for x in lines_data:
#     print("-------------------")
#     for j in x:
#         print(j)
#     print("-------------------")
    



