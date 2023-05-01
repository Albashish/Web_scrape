import requests
from bs4 import BeautifulSoup
import json

def FindAlternateGroups(store_domain):
    page = 1
    products = []
    while page==1:
        url = f"{store_domain}/collections/all/products.json?page={page}"
        response = requests.get(url)
        data = response.json()
        if len(data['products']) == 0:
            break
        products += data['products']
        page += 1

    # Create a dictionary of body_html content with simplified text content
    html_dict = {}
    for product in data['products']:
        soup = BeautifulSoup(product['body_html'], 'html.parser')
        text = soup.get_text().strip()
        #print(html_dict.get(text, []) + [product['handle']])
        html_dict[text] = html_dict.get(text, []) + [product['handle']]

    # Find alternate groups
    alternate_groups = []
    for handles in html_dict.values():
        if len(handles) > 1:
            alternate_groups.append({"product alternates": [f"https://{store_domain}/products/{handle}" for handle in handles]})
    

    return json.dumps(alternate_groups, indent=4)



store_domain = "https://boysnextdoor-apparel.co"
alternates = FindAlternateGroups(store_domain)
print(alternates)
with open("output.json",'w') as f:
    f.write(alternates)

