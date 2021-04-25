import csv
import os

from analytics_component.models import Order, OrderLine, Product, Promotion, ProductPromotion, VendorCommissions


def import_csvs(data_folder_path):
    """Function to import the required data to sqlite, from csv format"""

    # Create list of data folder contents
    data_folder_contents = os.listdir(data_folder_path)

    # Loop through filenames in data folder, and import data
    for filename in data_folder_contents:

        # Handle '/' or no '/' in folder path
        if data_folder_path[-1] == '/':
            file_path = data_folder_path + filename
        else:
            file_path = data_folder_path + '/' + filename

        # Open each csv in turn, and import data as dictated by filename
        with open(file_path) as csv_file:

            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader) # Skip headers

            if filename == 'orders.csv': # Import orders
                print("Importing data from orders.csv")

                for row in csv_reader:
                    create_order = Order(
                        id=row[0],
                        created_at=row[1],
                        vendor_id=row[2],
                        customer_id=row[3]
                    )
                    create_order.save()

            elif filename == 'order_lines.csv': # Import order lines
                print("Importing data from order_lines.csv")

                for row in csv_reader:
                    create_order_line = OrderLine(
                        order_id=row[0],
                        product_id=row[1],
                        product_description=row[2],
                        product_price=row[3],
                        product_vat_rate=row[4],
                        discount_rate=row[5],
                        quantity=row[6],
                        full_price_amount=row[7],
                        discounted_amount=row[8],
                        vat_amount=row[9],
                        total_amount=row[10]
                    )
                    create_order_line.save()

            elif filename == 'products.csv': # Import products
                print("Importing data from products.csv")

                for row in csv_reader:
                    create_product = Product(
                        id=row[0],
                        description=row[1]
                    )
                    create_product.save()
            elif filename == 'promotions.csv': # Import promotions
                print("Importing data from promotions.csv")

                for row in csv_reader:
                    create_promotion = Promotion(
                        id=row[0],
                        description=row[1]
                    )
                    create_promotion.save()

            elif filename == 'product_promotions.csv': # Import product promotions
                print("Importing data from product_promotions.csv")

                for row in csv_reader:
                    create_product_promotion = ProductPromotion(
                        date=row[0],
                        product_id=row[1],
                        promotion_id=row[2]
                    )
                    create_product_promotion.save()

            elif filename == 'commissions.csv': # Import vendor commissions
                print("Importing data from commissions.csv")

                for row in csv_reader:
                    create_commission = VendorCommissions(
                        date=row[0],
                        vendor_id=row[1],
                        rate=row[2]
                    )
                    create_commission.save()
