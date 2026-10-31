import requests
import json
from datetime import datetime


API_URL = "https://dummyjson.com/products"


def extract_products():
    response = requests.get(API_URL)

    response.raise_for_status()

    return response.json()


def inspect_data(data):
    print("Total products:", data["total"])
    print("Products returned:", len(data["products"]))

    first_product = data["products"][0]

    print("\nFields in first product:")

    for field in first_product:
        print(field)

    print("\nComplex fields:")

    for field, value in first_product.items():

        if isinstance(value, dict):
            print(field, "-> OBJECT")

        elif isinstance(value, list):
            print(field, "-> ARRAY")


def save_raw_data(data):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"products_{timestamp}.json"

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nRaw data saved to: {file_name}")

def simulate_change(data):
    for product in data["products"]:
        if product["id"] == 13:
            print(
                f"Changing product 13 stock: "
                f"{product['stock']} -> 18"
            )
            product["stock"] = 18

            return data

    raise ValueError("Product 13 not found.")



def main():
    print("Starting data ingestion...")

    data = extract_products()

    inspect_data(data)

    data = simulate_change(data)

    save_raw_data(data)

    print("\nIngestion completed successfully.")


if __name__ == "__main__":
    main()