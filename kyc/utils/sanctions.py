import csv
from rapidfuzz import fuzz

def check_sanctions(name, csv_path='kyc/utils/sdn.csv'):
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 2:
                    continue
                sanctioned_name = row[1]
                if fuzz.partial_ratio(name.lower(), sanctioned_name.lower()) > 85:
                    return True, sanctioned_name
        return False, None
    except Exception as e:
        return False, f"Sanctions check error: {str(e)}"
