import json
from amazon import scrape_amazon
from flipkart import scrape_flipkart
if __name__ == "__main__":
    search_query = input("Enter product name to search: ")
    amazon_results = scrape_amazon(search_query)
    flipkart_results = scrape_flipkart(search_query)

    # print(meesho_results)

    results = amazon_results + flipkart_results
    print(len(results))
    # print(flipkart_results)
    if results:
        with open("products.json", "w") as f:
            json.dump(results, f, indent=4)
        print("Products saved to 'products.json'.")
    else:
        print("No products found or Amazon blocked the request.")
