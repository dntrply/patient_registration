import cv2
import pytesseract
import re
import datetime
import csv


def main():
    # 1. Load and preprocess image
    img = cv2.imread("aadhaar_photo.jpg")
    if img is None:
        print("Error: Could not load image 'aadhaar_photo.jpg'. Please check if the file exists.")
        return
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)              # convert to grayscale
    img = cv2.resize(img, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_CUBIC)  # upscale image
    # (Optional: apply thresholding)
    # img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)[1]

    # 2. OCR extraction
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # path to tesseract binary (if needed)
    text = pytesseract.image_to_string(img, lang='eng')

    # 3. Initialize fields
    name = ""; gender = ""; dob = ""; uid = ""; address = ""

    # 4. Parse Name - skip header lines and find actual name
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    name_found = False
    
    for line in lines:
        line_lower = line.lower()
        # Skip header/official text lines
        if any(keyword in line_lower for keyword in ['uidai', 'government', 'unique', 'identification', 'authority', 'india', 'भारत']):
            continue
        # Skip lines that look like IDs, dates, or addresses
        if re.search(r'\d{4}\s?\d{4}\s?\d{4}', line) or re.search(r'\d{2}[\/-]\d{2}[\/-]\d{4}', line):
            continue
        # Skip very short lines (likely not names)
        if len(line.strip()) < 3:
            continue
        
        # Clean and validate potential name
        cleaned_name = re.sub(r'[^A-Za-z ]', '', line).strip()
        # Remove common prefixes like "Name", "नाम", etc.
        cleaned_name = re.sub(r'^(Name|नाम)\s+', '', cleaned_name, flags=re.IGNORECASE).strip()
        if len(cleaned_name.split()) >= 2 and len(cleaned_name) > 5:  # At least 2 words, reasonable length
            name = cleaned_name
            name_found = True
            break
    
    # Fallback: if no name found using above logic, try simpler approach
    if not name_found and lines:
        # Skip obvious header lines and take first reasonable line
        for line in lines:
            if len(line) > 10 and not any(keyword in line.lower() for keyword in ['unique', 'authority', 'government']):
                name = re.sub(r'[^A-Za-z ]', '', line).strip()
                break

    # 5. Parse Gender
    # Look for "Gender: M/F" pattern first
    gender_match = re.search(r'Gender:\s*([MF])', text, re.IGNORECASE)
    if gender_match:
        gender = gender_match.group(1).upper()
    elif "female" in text.lower():
        gender = "F"
    elif "male" in text.lower():
        gender = "M"

    # 6. Parse DOB or Year of Birth
    dob_match = re.search(r'(\d{2}[\/-]\d{2}[\/-]\d{4})', text)
    if dob_match:
        dob_str = dob_match.group(1)
        # Convert to YYYY-MM-DD format
        try:
            dob_dt = datetime.datetime.strptime(dob_str.replace('/', '-'), "%d-%m-%Y")
            dob = dob_dt.strftime("%Y-%m-%d")
        except:
            dob = ""  # leave empty if parse fails
    else:
        # Try Year of Birth
        yob_match = re.search(r'\b(19\d{2}|20\d{2})\b', text)
        if yob_match:
            year = yob_match.group(1)
            dob = f"{year}-01-01"  # default to Jan 1 of that year (if only year is known)

    # 7. Parse Aadhaar Number
    uid_match = re.search(r'\d{4}\s?\d{4}\s?\d{4}', text)
    if uid_match:
        uid = uid_match.group(0).replace(' ', '')

    # 8. Parse Address - extract from OCR text between Gender and UID
    address_text = ""
    
    # Find address section between Gender and UID in the OCR text
    gender_pos = text.find("Gender:")
    uid_match = re.search(r'\d{4}\s?\d{4}\s?\d{4}', text)
    
    if gender_pos != -1 and uid_match:
        # Extract text between gender line and UID
        gender_end = text.find('\n', gender_pos)
        uid_start = uid_match.start()
        
        if gender_end != -1 and uid_start > gender_end:
            address_section = text[gender_end:uid_start].strip()
            
            # Clean up the address section
            address_lines = [line.strip() for line in address_section.split('\n') if line.strip()]
            
            # Remove empty lines and filter out noise
            clean_address_lines = []
            for line in address_lines:
                # Skip lines that are too short or contain mostly special characters
                if len(line) > 3 and not re.match(r'^[^\w\s]*$', line):
                    clean_address_lines.append(line)
            
            # Join and clean up address formatting
            address = ", ".join(clean_address_lines)
            # Remove double commas and extra spaces
            address = re.sub(r',\s*,', ',', address)
            address = re.sub(r'\s+', ' ', address).strip()
    
    # Alternative: Look for Indian state names and pin codes as address indicators
    if not address:
        indian_states = ['maharashtra', 'delhi', 'mumbai', 'karnataka', 'tamil nadu', 'gujarat', 
                        'rajasthan', 'punjab', 'haryana', 'uttar pradesh', 'west bengal', 'kerala']
        
        # Find lines containing state names or pin codes (6 digits)
        for line in lines:
            line_lower = line.lower()
            # Check if line contains a state name or 6-digit pin code
            if (any(state in line_lower for state in indian_states) or 
                re.search(r'\b\d{6}\b', line)):
                # This might be part of address, collect surrounding lines
                line_index = lines.index(line)
                # Take a few lines around this line as potential address
                start_idx = max(0, line_index - 2)
                end_idx = min(len(lines), line_index + 2)
                addr_candidates = lines[start_idx:end_idx]
                
                # Filter out header lines and UID lines
                filtered_addr = []
                for addr_line in addr_candidates:
                    if not any(keyword in addr_line.lower() for keyword in 
                              ['unique', 'authority', 'government', 'aadhaar']) and \
                       not re.search(r'\d{4}\s?\d{4}\s?\d{4}', addr_line):
                        filtered_addr.append(addr_line)
                
                if filtered_addr:
                    address = ", ".join(filtered_addr)
                    # Clean up formatting
                    address = re.sub(r',\s*,', ',', address)
                    address = re.sub(r'\s+', ' ', address).strip()
                    break

    # At this point, we have extracted: name, gender, dob, uid, address.
    print(f"Name: {name}")
    print(f"Gender: {gender}")
    print(f"DOB: {dob}")
    print(f"UID: {uid}")
    print(f"Address: {address}")
    
    # Generate CSV file with the extracted data
    csv_filename = "patient_data.csv"
    
    # Check if CSV file exists to determine if we need to write header
    file_exists = False
    try:
        with open(csv_filename, 'r') as f:
            file_exists = True
    except FileNotFoundError:
        file_exists = False
    
    # Write data to CSV
    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Gender', 'DOB', 'UID', 'Address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header only if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write the extracted data
        writer.writerow({
            'Name': name,
            'Gender': gender,
            'DOB': dob,
            'UID': uid,
            'Address': address
        })
    
    print(f"\nData saved to {csv_filename}")



if __name__ == "__main__":
    main()