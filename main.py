import requests
from bs4 import BeautifulSoup
import json

def FindAlternateGroups(store_domain):
    # Make a request to the product data URL
    url = f"{store_domain}/collections/all/products.json?page=1"
    response = requests.get(url)
    data = response.json()

    # Create a dictionary to store product alternates
    alternates = {}

    # Iterate over each product in the data
    for product in data['products']:
        
        # Get the product link and its variant options
        product_link = f"{store_domain}/products/{product['handle']}"
        
        # Create a unique key for the alternate group using vendor, product_type and tags associated with the product
        if len(product['tags'])!=0:
            key=f"{product['product_type']}: {product['tags'][0]}: {product['vendor']} "
        else:
            key=f"{product['product_type']}: : {product['vendor']} "

        print(key)
        
        # Add the product link to the corresponding alternate group
        if key in alternates:
            alternates[key].append(product_link)
        else:
            alternates[key] = [product_link]

    # Convert the alternates dictionary to JSON format
    result = []
    for key, value in alternates.items():
        result.append({"product alternates": value})

    return json.dumps(result, indent=4)

# Test the function with the provided store domain
store_domain = "https://boysnextdoor-apparel.co"
alternate_groups = FindAlternateGroups(store_domain)
with open("output.json",'w') as f:
    f.write(alternate_groups)

