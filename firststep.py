import re

# Define regex patterns
date_pattern = re.compile(r'(\d{2}\.\d{2}\.\d{2})|\b(\d{2} \d{2} \d{2})\b')
summary_pattern = re.compile(r'O:(\d{2} \d{2} \d{2}\.\d) (.+)')
location_pattern = re.compile(r'F=(\d{2} \d{2}=\d{2}\.\d{2}N)\s+L=(\d{2} \d{2}=\d{2}\.\d{2}E)')
details_pattern = re.compile(r'kl\s+(\w)\s+h=(\d+-\d+)\s+K=(\d+\.\d+)\s+Mpv=(\d+\.\d+)')
station_pattern = re.compile(
    r',\s*([A-Z]{2,})\s*,\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),'
    r'\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*([^,]*),\s*(.*)'
)

file_path = '199207_changed'
epicenters = []
current_epicenter = None
last_header_date = None

# Read the lines of the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Helper function to safely get groups
def safe_group(match, group_num):
    try:
        return match.group(group_num).strip() if len(match.groups()) >= group_num else ''
    except IndexError:
        return ''

# Process each line
for line in lines:
    line = line.strip()

    # If the line is empty, start a new epicenter
    if not line:
        if current_epicenter:
            epicenters.append(current_epicenter)
        current_epicenter = None
        continue

    # If there is no current epicenter, create a new one
    if not current_epicenter:
        current_epicenter = {
            'Header_Date': '',
            'Epicenter_Date': '',
            'Time': '',
            'Region': '',
            'Location': '',
            'Magnitude': '',
            'Details': '',
            'Summary': '',
            'Stations': []
        }

    # Find the main date (Header_Date) and Epicenter_Date
    date_match = date_pattern.search(line)
    if date_match:
        date_value = date_match.group(1) or date_match.group(2)
        if not last_header_date or date_value != last_header_date:
            last_header_date = date_value
            current_epicenter['Header_Date'] = date_value
        if not current_epicenter['Epicenter_Date']:
            current_epicenter['Epicenter_Date'] = date_value

    # Find the summary line (O)
    summary_match = summary_pattern.search(line)
    if summary_match:
        current_epicenter['Summary'] = f"O: {summary_match.group(1)} {summary_match.group(2)}"
        if not current_epicenter['Epicenter_Date']:
            current_epicenter['Epicenter_Date'] = summary_match.group(1)
        current_epicenter['Time'] = summary_match.group(1)
        current_epicenter['Region'] = summary_match.group(2)

    # Find the location data (F and L lines)
    location_match = location_pattern.search(line)
    if location_match:
        current_epicenter['Location'] = f"F={location_match.group(1)} L={location_match.group(2)}"

    # Find the details (kl lines)
    details_match = details_pattern.search(line)
    if details_match:
        current_epicenter['Details'] = f"kl {details_match.group(1)} h={details_match.group(2)} K={details_match.group(3)} Mpv={details_match.group(4)}"

    # Find the station data
    station_match = station_pattern.search(line)
    if station_match:
        station_info = {
            'St': safe_group(station_match, 1),
            'P_Fa': safe_group(station_match, 2),
            'P_Time': safe_group(station_match, 3),
            'SFa': safe_group(station_match, 4),
            'S_Time': safe_group(station_match, 5),
            'S-P': safe_group(station_match, 6),
            'Sour_T': safe_group(station_match, 7),
            'EpH': safe_group(station_match, 8),
            'EpR': safe_group(station_match, 9),
            'T_p': safe_group(station_match, 10),
            'T_s': safe_group(station_match, 11),
            'T_S': safe_group(station_match, 12),
            'Ns1': safe_group(station_match, 13),
            'Ns2': safe_group(station_match, 14),
            'Ew1': safe_group(station_match, 15),
            'Ew2': safe_group(station_match, 16),
            'Z': safe_group(station_match, 17),
            'K': safe_group(station_match, 18),
            'Mpv': safe_group(station_match, 19),
            'MLH': safe_group(station_match, 20),
            'Comment': safe_group(station_match, 21)
        }
        current_epicenter['Stations'].append(station_info)

# Add the last epicenter if it is not added
if current_epicenter:
    epicenters.append(current_epicenter)

# Save the processed data to a file
output_file = 'formatted_199207.txt'
with open(output_file, 'w') as file:
    for epicenter in epicenters:
        file.write(f"Date: {epicenter['Header_Date']}\n")
        file.write(f"Summary:\n    {epicenter['Summary']}\n")
        file.write(f"Location:\n    {epicenter['Location']}\n")
        file.write(f"Details:\n    {epicenter['Details']}\n")
        file.write(f"Stations:\n")
        for station in epicenter['Stations']:
            file.write(f"    Station: {station['St']}\n")
            for key, value in station.items():
                file.write(f"        {key}: {value}\n")  # Print all fields, including empty values
            file.write("\n")

print(f"Formatted data has been saved to '{output_file}'")
