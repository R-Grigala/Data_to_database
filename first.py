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

for x in range(30):
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
        temp_lines_total.append(line)
    else:
        
        temp_lines_data.append(line)

for x in temp_lines_data:
    print(x)
