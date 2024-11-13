import re

# განვსაზღვრავთ რეგულარულ გამონაკლისებს
date_pattern = re.compile(r'(\d{2}\.\d{2}\.\d{2})|\b(\d{2} \d{2} \d{2})\b')  # ამოწმებს თარიღს ორ ფორმატში (მაგ. 01 07 92 ან 01.07.92)
summary_pattern = re.compile(r'O:(\d{2} \d{2} \d{2}\.\d) (.+)')  # მოძებნის "O:" ხაზებს, სადაც ნაჩვენებია დრო და რეგიონი
location_pattern = re.compile(r'F=(\d{2} \d{2}=\d{2}\.\d{2}N)\s+L=(\d{2} \d{2}=\d{2}\.\d{2}E)')  # მოძებნის გეოგრაფიულ მონაცემებს (F და L)
details_pattern = re.compile(r'kl\s+(\w)\s+h=(\d+-\d+)\s+K=(\d+\.\d+)\s+Mpv=(\d+\.\d+)')  # "kl" ხაზები, სადაც მოცემულია სიდიდეები
station_pattern = re.compile(r'(?:,)?\s*(\d{2}\.\d{2}\.\d{2})?\s*,\s*([A-Z]{2,})\s*,\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*)')  # სადგურის მონაცემები

# parser ფაილის სახელი
file_path = '199207_changed'

# initializing სიები მონაცემების შესანახად
epicenters = []
current_epicenter = None
last_header_date = None

# ვკითხულობთ ფაილის ხაზებს
with open(file_path, 'r') as file:
    lines = file.readlines()

# ვამუშავებთ თითოეულ ხაზს
for line in lines:
    line = line.strip()  # ათავისუფლებს ზედმეტ ადგილებს

    # თუ ხაზი ცარიელია, იწყება ახალი ეპიცენტრი
    if not line:
        if current_epicenter:
            epicenters.append(current_epicenter)  # თუ არსებობს წინამორბედი ეპიცენტრი, დაამატე სიაში
        current_epicenter = None  # ნულდება არსებული ეპიცენტრი
        continue

    # თუ არ არსებობს მიმდინარე ეპიცენტრი, შექმენი ახალი
    if not current_epicenter:
        current_epicenter = {
            'Header_Date': '',    # თარიღი (მთავარი)
            'Epicenter_Date': '', # ეპიცენტრის თარიღი
            'Time': '',           # დრო
            'Region': '',         # რეგიონი
            'Location': '',       # ადგილმდებარეობა
            'Magnitude': '',      # მაგნიტუდა
            'Details': '',        # დეტალები
            'Summary': '',        # რეზიუმე
            'Stations': []        # სადგურები
        }

    # მოძებნე მთავარი თარიღი (Header_Date) და Epicenter_Date
    date_match = date_pattern.search(line)
    if date_match:
        date_value = date_match.group(1) or date_match.group(2)  # აიღებს თარიღს ორივე ფორმატიდან
        if not last_header_date or date_value != last_header_date:  # თუ ეს თარიღი განსხვავდება უკანასკნელისგან
            last_header_date = date_value
            current_epicenter['Header_Date'] = date_value
        if not current_epicenter['Epicenter_Date']:  # თუ Epicenter_Date არ არის დაგეგმილი, გამოიყენე მთავარი თარიღი
            current_epicenter['Epicenter_Date'] = date_value

    # მოძებნა სადაც მოცემულია დრო და რეგიონი
    summary_match = summary_pattern.search(line)
    if summary_match:
        current_epicenter['Summary'] = f"O: {summary_match.group(1)} {summary_match.group(2)}"
        if not current_epicenter['Epicenter_Date']:  # თუ Epicenter_Date არ არის, შეავსე რეზიუმედან
            current_epicenter['Epicenter_Date'] = summary_match.group(1)
        current_epicenter['Time'] = summary_match.group(1)  # დრო
        current_epicenter['Region'] = summary_match.group(2)  # რეგიონი

    # მოძებნე ადგილმდებარეობა (F და L ხაზები)
    location_match = location_pattern.search(line)
    if location_match:
        current_epicenter['Location'] = f"F={location_match.group(1)} L={location_match.group(2)}"

    # მოძებნა დეტალები (kl ხაზები)
    details_match = details_pattern.search(line)
    if details_match:
        current_epicenter['Details'] = f"kl {details_match.group(1)} h={details_match.group(2)} K={details_match.group(3)} Mpv={details_match.group(4)}"

    # სადგურის მონაცემების მოძებნა
    station_match = station_pattern.search(line)
    if station_match:
        station_info = {
            'D': current_epicenter['Epicenter_Date'],  # სადგურისთვის Epicenter_Date
            'St': station_match.group(2).strip(),  # სადგურის დასახელება
            'P_Fa': station_match.group(3).strip(),  # P_Fa
            'P_Time': station_match.group(4).strip(),  # P_Time
            'SFa': station_match.group(5).strip(),  # SFa
            'S_Time': station_match.group(6).strip(),  # S_Time
            'S-P': station_match.group(7).strip(),  # S-P
            'Sour_T': station_match.group(8).strip(),  # Sour_T
            'EpH': station_match.group(9).strip(),  # EpH
            'EpR': station_match.group(10).strip(),  # EpR
            'T_p': station_match.group(11).strip(),  # T_p
            'T_s': station_match.group(12).strip(),  # T_s
            'T_S': station_match.group(13).strip(),  # T_S
            'Ns1': station_match.group(14).strip(),  # Ns1
            'Ns2': station_match.group(15).strip(),  # Ns2
            'Ew1': station_match.group(16).strip(),  # Ew1
            'Ew2': station_match.group(17).strip() if len(station_match.groups()) > 17 else '',  # Ew2 (optional)
            'Z': station_match.group(18).strip() if len(station_match.groups()) > 18 else '',  # Z (optional)
            'K': station_match.group(19).strip() if len(station_match.groups()) > 19 else '',  # K (optional)
            'Mpv': station_match.group(20).strip() if len(station_match.groups()) > 20 else '',  # Mpv (optional)
            'MLH': station_match.group(21).strip() if len(station_match.groups()) > 21 else '',  # MLH (optional)
            'Comment': station_match.group(22).strip() if len(station_match.groups()) > 22 else ''  # Comment (optional)
        }
        
        # თუ D (Epicenter_Date) უკვე არის სადგურის მონაცემებში, ამოვიღოთ (არ გაიმეოროს)
        if station_info['D'] == current_epicenter['Epicenter_Date']:
            station_info.pop('D')  # D ამოიღე, რომ თავიდან ავიცილოთ გამეორება
        
        current_epicenter['Stations'].append(station_info)  # სადგური დავამატოთ ეპიცენტრის მონაცემებს

# ბოლოს დავამატოთ უკანასკნელი ეპიცენტრი, თუ იგი არ არის დამატებული
if current_epicenter:
    epicenters.append(current_epicenter)

# შევინახოთ დამუშავებული მონაცემები ფაილში
output_file = 'formatted_199207.txt'
with open(output_file, 'w') as file:
    for epicenter in epicenters:
        file.write(f"Date: {epicenter['Header_Date']}\n")
        file.write(f"Summary:\n {epicenter['Summary']}\n")
        file.write(f"Location:\n {epicenter['Location']}\n")
        file.write(f"Details:\n {epicenter['Details']}\n")
        file.write(f"Stations:\n")
        for station in epicenter['Stations']:
            file.write(f" Station: {station['St']}\n")
            for key, value in station.items():
                if key != 'St': 
                    file.write(f" {key}: {value}\n")
            file.write("\n")


print(f"Formatted data has been saved to '{output_file}'")
