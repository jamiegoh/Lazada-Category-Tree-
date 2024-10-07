import csv
import json
from collections import defaultdict

csv.field_size_limit(100000000)

def parse_attributes(attributes_json):
    attributes = json.loads(attributes_json)
    compulsory_attrs = set()
    if isinstance(attributes, dict) and 'module' in attributes:
        for module in attributes['module']:
            for attribute in module.get('attributes', []):
                if attribute.get('is_mandatory') == 1:
                    compulsory_attrs.add(attribute['name'])
    return compulsory_attrs

def analyze_csv(file_path):
    all_attributes = defaultdict(int)
    category_count = 0
    
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category_count += 1
            attributes_json = row['Attributes']
            compulsory_attrs = parse_attributes(attributes_json)
            for attr in compulsory_attrs:
                all_attributes[attr] += 1
    
    compulsory_across_all = [attr for attr, count in all_attributes.items() if count == category_count]
    return compulsory_across_all, category_count

def main():
    csv_file_path = 'lazada_categories_attributes.csv'
    compulsory_attributes, total_categories = analyze_csv(csv_file_path)
    
    print(f"Analyzed {total_categories} categories.")
    print("Compulsory attributes across all categories:")
    for attr in compulsory_attributes:
        print(f"- {attr}")
    
    if not compulsory_attributes:
        print("No attributes are compulsory across all categories.")

if __name__ == "__main__":
    main()