import json
import csv
import os


#def find_latest_bronze_file():
#    files = [
#        file for file in os.listdir(".")
#        if file.startswith("products_") and file.endswith(".json")
#    ]
#
#    if not files:
#        raise FileNotFoundError("No Bronze JSON files found.")
#
 #   return max(files)


def find_latest_bronze_file():
    ingestion_folder = "../ingestionAWS"

    files = [
        file for file in os.listdir(ingestion_folder)
        if file.startswith("products_") and file.endswith(".json")
    ]

    if not files:
        raise FileNotFoundError("No Bronze JSON files found.")

    latest_file = max(files)

    return os.path.join(ingestion_folder, latest_file)



def read_bronze_data(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def transform_products(data):
    products = data["products"]

    silver_products = []

    for product in products:
        silver_products.append({
            "id": product["id"],
            "title": product["title"],
            "category": product["category"],
            "price": product["price"],
            "discountPercentage": product["discountPercentage"],
            "rating": product["rating"],
            "stock": product["stock"],
            "brand": product.get("brand"),
            "sku": product.get("sku"),
            "availabilityStatus": product["availabilityStatus"],
            "minimumOrderQuantity": product["minimumOrderQuantity"]
        })

    return silver_products


def save_silver_data(products):
    file_name = "silver_products.csv"

    fieldnames = products[0].keys()

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(products)

    print(f"Silver data saved to: {file_name}")


def main():
    print("Starting Silver transformation...")

    bronze_file = find_latest_bronze_file()

    print(f"Reading Bronze file: {bronze_file}")

    data = read_bronze_data(bronze_file)

    silver_products = transform_products(data)

    print(f"Products transformed: {len(silver_products)}")

    save_silver_data(silver_products)

    print("Silver transformation completed successfully.")


if __name__ == "__main__":
    main()