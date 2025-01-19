import stripe
import csv
from datetime import datetime
import os
from dotenv import load_dotenv

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

def write_invoices_to_file(invoices, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Invoice ID', 'Created', 'Due Date', 'Paid At', 'Amount Paid', 'Currency', 'Payment Status'])

        for invoice in paid_invoices:
            writer.writerow([
                invoice.id,
                datetime.fromtimestamp(invoice.created).isoformat(),
                datetime.fromtimestamp(invoice.due_date).isoformat() if invoice.due_date else '',
                datetime.fromtimestamp(invoice.status_transitions.paid_at).isoformat() if invoice.status_transitions.paid_at else '',
                invoice.amount_paid / 100,
                invoice.currency,
                invoice.status
            ])

## Initialization

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

output_file = os.path.join(os.path.dirname(__file__), 'out', 'invoices_2024_Q4.csv')

## Main script

paid_invoices = fetch_paid_invoices()

write_invoices_to_file(paid_invoices, output_file)

print("Export completed.")
