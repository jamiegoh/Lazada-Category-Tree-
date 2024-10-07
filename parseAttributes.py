import csv
import json
from collections import defaultdict


csv.field_size_limit(100000000)

def parse_attributes(attributes_json):
    attributes = json.loads(attributes_json)
    all_attrs = set()
    compulsory_attrs = set()
    if 'data' in attributes:
        for attr in attributes['data']:
            all_attrs.add(attr['name'])
            if attr.get('is_mandatory') == 1:
                compulsory_attrs.add(attr['name'])
    return all_attrs, compulsory_attrs

def analyze_csv(file_path):
    categories = []
    all_attributes = set()
    
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            category_name = row['Category Name']
            category_id = row['Category ID']
            attributes_json = row['Attributes']
            all_attrs, compulsory_attrs = parse_attributes(attributes_json)
            
            categories.append({
                'name': category_name,
                'id': category_id,
                'all_attrs': all_attrs,
                'compulsory_attrs': compulsory_attrs
            })
            
            all_attributes.update(all_attrs)
    
    return categories, all_attributes

def write_csv(file_name, headers, rows):
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

def main():
    input_csv = 'lazada_categories_attributes.csv'
    categories, all_attributes = analyze_csv(input_csv)
    
    #Categories where 'name' is compulsory
    name_compulsory = [{'Category Name': cat['name'], 'Category ID': cat['id']} 
                       for cat in categories if 'name' in cat['compulsory_attrs']]
    write_csv('1_name_compulsory.csv', ['Category Name', 'Category ID'], name_compulsory)
    
    #Categories where 'name' is not compulsory but still an attribute
    name_optional = [{'Category Name': cat['name'], 'Category ID': cat['id']} 
                     for cat in categories if 'name' in cat['all_attrs'] and 'name' not in cat['compulsory_attrs']]
    write_csv('2_name_optional.csv', ['Category Name', 'Category ID'], name_optional)
    
    #Categories where 'description' is compulsory
    desc_compulsory = [{'Category Name': cat['name'], 'Category ID': cat['id']} 
                       for cat in categories if 'description' in cat['compulsory_attrs']]
    write_csv('3_description_compulsory.csv', ['Category Name', 'Category ID'], desc_compulsory)
    
    #Categories where 'description' is not compulsory but still an attribute
    desc_optional = [{'Category Name': cat['name'], 'Category ID': cat['id']} 
                     for cat in categories if 'description' in cat['all_attrs'] and 'description' not in cat['compulsory_attrs']]
    write_csv('4_description_optional.csv', ['Category Name', 'Category ID'], desc_optional)
    
    #All common attributes
    common_attrs = [attr for attr in all_attributes 
                    if all(attr in cat['all_attrs'] for cat in categories)]
    write_csv('5_common_attributes.csv', ['Attribute Name'], [{'Attribute Name': attr} for attr in common_attrs])
    
    print("CSV files have been generated successfully.")

if __name__ == "__main__":
    main()