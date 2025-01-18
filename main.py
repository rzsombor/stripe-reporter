import stripe
import csv
from datetime import datetime
import os
from dotenv import load_dotenv

# Set your secret key. Remember to replace 'your_secret_key' with your actual Stripe secret key.
# Load environment variables from a .env file if it exists
load_dotenv()

# Set your secret key from the environment variable
stripe.api_key = os.getenv('STRIPE_API_KEY')

# Define the start and end dates for Q4 2024
start_date = datetime(2024, 10, 1)
end_date = datetime(2024, 12, 31, 23, 59, 59)

# Convert dates to Unix timestamps
start_timestamp = int(start_date.timestamp())
end_timestamp = int(end_date.timestamp())

# Function to fetch all paid invoices in Q4 2024
def fetch_paid_invoices():
    invoices = []
    has_more = True
    starting_after = None

    while has_more:
        response = stripe.Invoice.list(
            status='paid',
            created={
                'gte': start_timestamp,
                'lte': end_timestamp
            },
            limit=100,
            starting_after=starting_after
        )
        invoices.extend(response.data)
        has_more = response.has_more
        if has_more:
            starting_after = response.data[-1].id

    return invoices

# Fetch the invoices
paid_invoices = fetch_paid_invoices()

# Write the invoices to a CSV file
output_dir = os.path.join(os.path.dirname(__file__), 'out')
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, 'paid_invoices_2024_Q4.csv')

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Invoice ID', 'Customer ID', 'Amount Paid', 'Currency', 'Created'])

    for invoice in paid_invoices:
        writer.writerow([
            invoice.id,
            invoice.customer,
            invoice.amount_paid,
            invoice.currency,
            datetime.fromtimestamp(invoice.created).isoformat()
        ])

print("Export completed. Check the 'paid_invoices_2024_Q4.csv' file.")