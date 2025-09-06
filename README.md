# Aadhaar Card OCR Data Extraction

A Python application that extracts patient information from Aadhaar card images using Optical Character Recognition (OCR) and exports the data to CSV format.

## Features

- **Automated OCR Processing**: Extracts text from Aadhaar card images using Tesseract OCR
- **Smart Data Parsing**: Intelligently identifies and extracts key information:
  - Name
  - Gender (M/F)
  - Date of Birth
  - Aadhaar Number (UID)
  - Complete Address (Street, City, State)
- **CSV Export**: Saves extracted data to a structured CSV file for easy data management
- **Error Handling**: Robust error handling for missing files and OCR failures

## Prerequisites

### Software Requirements
- Python 3.7 or higher
- Tesseract OCR engine

### Installing Tesseract OCR

**Windows:**
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install to the default location: `C:\Program Files\Tesseract-OCR\`
3. The application is configured to use this default path

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd patient_registration
```

2. Install Python dependencies:
```bash
pip install opencv-python pytesseract
```

## Usage

1. Place your Aadhaar card image in the project directory with the filename `sample_aadhaar_photo.jpg` (or modify the filename in main.py)

2. Run the application:
```bash
python main.py
```

3. The extracted information will be displayed in the console and automatically saved to `sample_patient_data.csv`

### Example Output

```
Name: Mohit Sharma
Gender: M
DOB: 1990-09-04
UID: 123456789012
Address: B-123, Sector 5, Andheri East, Mumbai, Maharashtra

Data saved to sample_patient_data.csv
```

## CSV Output Format

The application generates a CSV file with the following columns:
- **Name**: Full name of the cardholder
- **Gender**: M (Male) or F (Female)
- **DOB**: Date of birth in YYYY-MM-DD format
- **UID**: 12-digit Aadhaar number
- **Address**: Complete address including street, city, and state

## Technical Details

### Image Preprocessing
- Converts images to grayscale for better OCR accuracy
- Upscales images by 2x for improved text recognition
- Optional thresholding for challenging images

### Data Extraction Logic
- **Name Extraction**: Filters out header text and identifies actual names using pattern matching
- **Gender Detection**: Recognizes both "Gender: M/F" format and full word patterns
- **Date Parsing**: Handles multiple date formats (DD/MM/YYYY, DD-MM-YYYY)
- **Address Parsing**: Extracts structured address information between gender and UID sections
- **UID Extraction**: Identifies 12-digit Aadhaar numbers with or without spacing

### Supported Address Formats
The application recognizes Indian address patterns including:
- Street addresses (e.g., B-123, Sector 5)
- Areas and localities (e.g., Andheri East)
- Cities (e.g., Mumbai)
- States (e.g., Maharashtra)
- PIN codes (6-digit postal codes)

## File Structure

```
patient_registration/
├── main.py                    # Main application script
├── sample_aadhaar_photo.jpg   # Sample Aadhaar card image (for demonstration)
├── sample_patient_data.csv    # Sample CSV output (for demonstration)
├── README.md                  # This documentation
├── .gitignore                 # Git ignore file
└── requirements.txt           # Python dependencies
```

## Sample Data

The repository includes sample files for demonstration:
- `sample_aadhaar_photo.jpg` - Sample Aadhaar card image
- `sample_patient_data.csv` - Sample extracted data in CSV format

These files are safe to include in version control as they contain only demonstration data.

## Error Handling

- **Missing Image**: Displays clear error message if input image is not found
- **OCR Failures**: Gracefully handles OCR processing errors
- **Invalid Data**: Provides fallback mechanisms for data extraction
- **File Permissions**: Handles CSV file access errors

## Limitations

- Requires clear, high-quality Aadhaar card images
- Works best with standard Aadhaar card layouts
- Tesseract OCR accuracy depends on image quality
- Currently optimized for English text extraction

## Branch Strategy

This repository uses the following branch structure:

- **`base`** - Frozen reference branch containing the initial stable implementation
  - Contains fully working OCR system with sample data
  - Use this branch as a reference point or starting point for new features
  - **Do not modify this branch** - it serves as the baseline
  
- **`master`** - Active development branch
  - All new features and improvements are developed here
  - May contain work-in-progress or experimental features

## Contributing

1. Fork the repository
2. Create a feature branch from `master` (`git checkout -b feature/new-feature`)
3. Make your changes and test thoroughly
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/new-feature`)
6. Create a Pull Request targeting the `master` branch

To start from the baseline implementation:
```bash
git checkout base
git checkout -b feature/your-feature-name
```

## License

This project is intended for educational and legitimate administrative purposes only. Users must comply with applicable privacy laws and regulations when processing personal identification documents.

## Security Note

This application processes sensitive personal information. Ensure compliance with:
- Data protection regulations (GDPR, etc.)
- Privacy laws in your jurisdiction
- Secure handling of personal identification documents
- Proper data storage and disposal practices

---

**Note**: This tool is designed for legitimate document processing purposes. Users are responsible for ensuring compliance with all applicable laws and regulations regarding the processing of personal identification documents.