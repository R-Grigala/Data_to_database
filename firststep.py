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
last_header_date = None  # ე.ი. შევინახავთ ბოლო ჰედერის თარიღს

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
            'Header_Date': '',  # შეცვლილი სახელი ჰედერისთვის
            'Epicenter_Date': '',  # ეპიცენტრის თარიღი
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
        date_value = date_match.group(1)
        # თუ ეს არის ახალი ჰედერის თარიღი
        if not last_header_date or date_value != last_header_date:
            last_header_date = date_value
            if not current_epicenter['Header_Date']:  # თუ ჰედერ თარიღი არ არსებობს
                current_epicenter['Header_Date'] = date_value
        # თუ ეს იგივე თარიღია, სადგურის წინ არ ჩავაწერთ
        elif date_value != current_epicenter['Epicenter_Date']:
            current_epicenter['Epicenter_Date'] = date_value

    # O: სტრიქონის მონაცემები (Summary)
    summary_match = summary_pattern.search(line)
    if summary_match:
        current_epicenter['Summary'] = f"O: {summary_match.group(2)} {summary_match.group(3)}"
        current_epicenter['Epicenter_Date'] = summary_match.group(1)  # ეპიცენტრის თარიღი
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
    # აქ კი შევამოწმებთ, რომ სადგური მინიმუმ ორი დიდი ასო შეიცავს და არა თარიღის სტრიქონში
    if line.startswith(',') and not date_pattern.match(line):  # დარწმუნდით რომ თარიღი არ იყოს
        # ამ შემთხვევაში სწორი მონაცემების მიღება
        station_data = line[1:].strip().split(',')
        
        # პირველი სიტყვა (რომელიც უნდა იყოს სადგური) იქნება პირველი მნიშვნელობა
        first_valid_word = station_data[0].strip()  # პირველი სიტყვა

        # შემოწმება, რომ სიტყვა შეიცავს მინიმუმ 2 დიდ ასოს
        if first_valid_word and sum(1 for char in first_valid_word if char.isupper()) >= 2:
            station_info = {
                'St': station_data[0].strip() if len(station_data) > 0 else '',
                'P_Fa': station_data[1].strip() if len(station_data) > 1 else '',
                'P_Time': station_data[2].strip() if len(station_data) > 2 else '',
                'SFa': station_data[3].strip() if len(station_data) > 3 else '',
                'S_Time': station_data[4].strip() if len(station_data) > 4 else '',
                'S-P': station_data[5].strip() if len(station_data) > 5 else '',
                'Sour_T': station_data[6].strip() if len(station_data) > 6 else '',
                'EpH': station_data[7].strip() if len(station_data) > 7 else '',
                'EpR': station_data[8].strip() if len(station_data) > 8 else '',
                'T_p': station_data[9].strip() if len(station_data) > 9 else '',
                'T_s': station_data[10].strip() if len(station_data) > 10 else '',
                'T_S': station_data[11].strip() if len(station_data) > 11 else '',
                'Ns1': station_data[12].strip() if len(station_data) > 12 else '',
                'Ns2': station_data[13].strip() if len(station_data) > 13 else '',
                'Ew1': station_data[14].strip() if len(station_data) > 14 else '',
                'Ew2': station_data[15].strip() if len(station_data) > 15 else '',
                'Z': station_data[16].strip() if len(station_data) > 16 else '',
                'K': station_data[17].strip() if len(station_data) > 17 else '',
                'Mpv': station_data[18].strip() if len(station_data) > 18 else '',
                'MLH': station_data[19].strip() if len(station_data) > 19 else '',
                'Comment': station_data[20].strip() if len(station_data) > 20 else ''
            }
            current_epicenter['Stations'].append(station_info)

# თუ ბოლო მონაცემი დარჩა, დაამატეთ
if current_epicenter:
    epicenters.append(current_epicenter)

# ფორმატირებული მონაცემების შენახვა ახალ ფაილში
output_file = 'formatted_199207.txt'

with open(output_file, 'w') as file:
    for epicenter in epicenters:
        # დაწერეთ ჰედერის თარიღი
        file.write(f"Date: {epicenter['Header_Date']}\n")
        
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
                file.write(f"    Station: {station['St']}\n")  # Now using 'St' for station
                for key, value in station.items():
                    if key != 'St':  # Skip the 'St' key here
                        file.write(f"        {key}: {value}\n")
        
        file.write("\n")

print(f"ფორმატირებული მონაცემები შენახულია '{output_file}'")

