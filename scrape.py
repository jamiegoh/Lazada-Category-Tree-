import lazop
import json
import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



def get_category_tree(client):
    request = lazop.LazopRequest('/category/tree/get', 'GET')
    request.add_api_param('language_code', 'en_US')
    response = client.execute(request)
    return response.body  # Return the response body directly

def get_category_attributes(client, category_id):
    request = lazop.LazopRequest('/category/attributes/get', 'GET')
    request.add_api_param('language_code', 'en_US')
    request.add_api_param('primary_category_id', category_id)
    response = client.execute(request)
    return response.body 

def traverse_categories(categories, client, csv_writer):
    for category in categories:
        if category.get('leaf', False):
            attributes = get_category_attributes(client, category['category_id'])
            csv_writer.writerow([category['name'], category['category_id'], json.dumps(attributes)])
            logger.info(f"Processed category: {category['name']} (ID: {category['category_id']})")
        
        if 'children' in category:
            traverse_categories(category['children'], client, csv_writer)

def main():
    # Lazada API credentials
    url = "https://api.lazada.com.my/rest"
    app_key = ''  # Replace with your actual app key
    app_secret = ''  # Replace with your actual app secret
    
    client = lazop.LazopClient(url, app_key, app_secret)

    category_tree = get_category_tree(client)
    
    with open('lazada_categories_attributes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Category Name', 'Category ID', 'Attributes'])
        
        if isinstance(category_tree, dict) and 'data' in category_tree:
            traverse_categories(category_tree['data'], client, csv_writer)
        else:
            logger.error("Failed to retrieve category tree or unexpected response format.")
            logger.error(f"Response: {category_tree}")
            csv_writer.writerow(['Error', 'Failed to retrieve category tree', json.dumps(category_tree)])

if __name__ == "__main__":
    main()