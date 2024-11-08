import re

# რეგულარული გამონაკლებით
date_pattern = re.compile(r'(\d{2}\.\d{2}\.\d{2})')  # თარიღი: 01.07.92
summary_pattern = re.compile(r'(\d{2} \d{2} \d{2}) O:(\d{2} \d{2} \d{2}\.\d{1,2})\s+([\w\s\(\)\-]+)')  # O: სტრიქონი
location_pattern = re.compile(r'F=(\d{2} \d{2}=\d{2}\.\d{2}N)\s+L=(\d{2} \d{2}=\d{2}\.\d{2}E)')  # F, L სტრიქონი
details_pattern = re.compile(r'kl\s+(\w)\s+h=(\d+-\d+)\s+K=(\d+\.\d+)\s+Mpv=(\d+\.\d+)')  # kl სტრიქონი

# შესამოწმებელი ფაილის მისამართი
file_path = '199207_changed'

# სია ეპიცენტრის მონაცემების შესანახად
epicenters = []
current_epicenter = None

# გახსენით ფაილი და წაიკითხეთ თითოეული ხაზი
with open(file_path, 'r') as file:
    lines = file.readlines()

# გადამუშავება თითოეული ხაზის
for i, line in enumerate(lines):
    line = line.strip()  # ამოღებულმა ზედმეტი სივრცეებმა რომ არ გვეშველოს

    if not line:  # თუ ხაზი ცარიელია, დავიწყებთ ახალი ეპიცენტრის მონაცემების შეგროვებას
        if current_epicenter:
            epicenters.append(current_epicenter)  # თუ არარეგულარული მონაცემები გვყავს, დავამატებთ
        current_epicenter = {
            'Date': '',
            'Time': '',
            'Region': '',
            'Location': '',
            'Magnitude': '',  # დაზოგვა
            'Details': '',
            'Summary': '',
            'Stations': []
        }
        continue

    # თარიღი: თუ გვხვდება თარიღი, დავამატოთ
    date_match = date_pattern.search(line)
    if date_match:
        current_epicenter['Date'] = date_match.group(1)

    # O: სტრიქონის მონაცემები (Summary)
    summary_match = summary_pattern.search(line)
    if summary_match:
        current_epicenter['Summary'] = f"O: {summary_match.group(2)} {summary_match.group(3)}"
        current_epicenter['Date'] = summary_match.group(1)  # თარიღი, რომელიც გვხვდება O: სტრიქონში
        current_epicenter['Time'] = summary_match.group(2)  # დრო
        current_epicenter['Region'] = summary_match.group(3)  # რეგიონი

    # F და L სტრიქონის მონაცემები
    location_match = location_pattern.search(line)
    details_match = details_pattern.search(line)
    
    if location_match:
        current_epicenter['Location'] = f"F={location_match.group(1)} L={location_match.group(2)}"
        
    elif details_match:
        current_epicenter['Details'] = f"kl {details_match.group(1)} h={details_match.group(2)} K={details_match.group(3)} Mpv={details_match.group(4)}"
    
    # თუ გვხვდება სადგური მონაცემები, მათ ვამატებთ
    if line.startswith(','):
        # აქ სადგურის მონაცემები უფრო დეტალურად უნდა ამოიღოს
        station_data = line[1:].strip().split(',')
        if len(station_data) > 1:
            station_info = {
                'Station': station_data[0].strip(),
                'P_Fa': station_data[1].strip() if len(station_data) > 1 else '',
                'P_Time': station_data[2].strip() if len(station_data) > 2 else '',
                'SFa': station_data[3].strip() if len(station_data) > 3 else '',
                'S_Time': station_data[4].strip() if len(station_data) > 4 else '',
                'EpH': station_data[5].strip() if len(station_data) > 5 else '',
                'EpR': station_data[6].strip() if len(station_data) > 6 else '',
                'T_p': station_data[7].strip() if len(station_data) > 7 else '',
                'T_s': station_data[8].strip() if len(station_data) > 8 else '',
                'T_S': station_data[9].strip() if len(station_data) > 9 else '',
                'Ns': station_data[10].strip() if len(station_data) > 10 else '',
                'Ew': station_data[11].strip() if len(station_data) > 11 else '',
                'Z': station_data[12].strip() if len(station_data) > 12 else '',
                'K': station_data[13].strip() if len(station_data) > 13 else '',
                'Mpv': station_data[14].strip() if len(station_data) > 14 else '',
                'MLH': station_data[15].strip() if len(station_data) > 15 else '',
                'Comment': station_data[16].strip() if len(station_data) > 16 else ''
            }
            current_epicenter['Stations'].append(station_info)

# თუ ბოლო მონაცემი დარჩა, დაამატეთ
if current_epicenter:
    epicenters.append(current_epicenter)

# ფორმატირებული მონაცემების შენახვა ახალ ფაილში
output_file = 'formatted_199207.txt'

with open(output_file, 'w') as file:
    for epicenter in epicenters:
        # დაწერეთ თარიღი
        file.write(f"Date: {epicenter['Date']}\n")
        
        # დაწერეთ O: სტრიქონი (Summary)
        file.write(f"Summary:\n")
        if epicenter['Summary']:
            file.write(f"    {epicenter['Summary']}\n")
        else:
            file.write(f"    O: არაა ინფორმაცია\n")
        
        # დაწერეთ F და L მონაცემები
        file.write(f"Location:\n")
        file.write(f"    {epicenter['Location']}\n")
        
        # დაწერეთ kl დეტალები
        file.write(f"Details:\n")
        file.write(f"    {epicenter['Details']}\n")
        
        # დაწერეთ ყველა სადგურის მონაცემები
        if epicenter['Stations']:
            file.write(f"Stations:\n")
            for station in epicenter['Stations']:
                file.write(f"    Station: {station['Station']}\n")
                file.write(f"        P_Fa: {station['P_Fa']}\n")
                file.write(f"        P_Time: {station['P_Time']}\n")
                file.write(f"        SFa: {station['SFa']}\n")
                file.write(f"        S_Time: {station['S_Time']}\n")
                file.write(f"        EpH: {station['EpH']}\n")
                file.write(f"        EpR: {station['EpR']}\n")
                file.write(f"        T_p: {station['T_p']}\n")
                file.write(f"        T_s: {station['T_s']}\n")
                file.write(f"        T_S: {station['T_S']}\n")
                file.write(f"        Ns: {station['Ns']}\n")
                file.write(f"        Ew: {station['Ew']}\n")
                file.write(f"        Z: {station['Z']}\n")
                file.write(f"        K: {station['K']}\n")
                file.write(f"        Mpv: {station['Mpv']}\n")
                file.write(f"        MLH: {station['MLH']}\n")
                file.write(f"        Comment: {station['Comment']}\n")
        
        file.write("\n")

print(f"ფორმატირებული მონაცემები შენახულია '{output_file}' ფაილში.")