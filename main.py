import argparse
import calendar
import csv
from datetime import datetime
import os
import stripe
from dotenv import load_dotenv


## Functions

def fetch_invoices(start_time, end_time):
    invoices = []
    has_more = True
    starting_after = None

    while has_more:
        response = stripe.Invoice.list(
            created={
                'gte': start_time,
                'lte': end_time
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

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Invoice ID', 'Created', 'Due Date', 'Paid At', 'Amount Paid', 'Amount Due', 'Currency', 'Payment Status'])

        for invoice in invoices:
            writer.writerow([
                invoice.id,
                datetime.fromtimestamp(invoice.created).isoformat(),
                datetime.fromtimestamp(invoice.due_date).isoformat() if invoice.due_date else '',
                datetime.fromtimestamp(invoice.status_transitions.paid_at).isoformat() if invoice.status_transitions.paid_at else '',
                invoice.amount_paid / 100,
                invoice.amount_due / 100,
                invoice.currency,
                invoice.status
            ])

def parse_quarter_arguments():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Generate Stripe invoice report for a specific year and quarter.')
    parser.add_argument('--year', type=int, required=True, help='The year for the report')
    parser.add_argument('--quarter', type=str, required=True, choices=['Q1', 'Q2', 'Q3', 'Q4'], help='The quarter for the report')
    args = parser.parse_args()

    # Determine the start and end dates based on the year and quarter
    year = args.year
    quarter = args.quarter

    return year, quarter

def quarter_to_date(year, quarter):
    if quarter == 'Q1':
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 3, calendar.monthrange(year, 3)[1], 23, 59, 59)
    elif quarter == 'Q2':
        start_date = datetime(year, 4, 1)
        end_date = datetime(year, 6, calendar.monthrange(year, 6)[1], 23, 59, 59)
    elif quarter == 'Q3':
        start_date = datetime(year, 7, 1)
        end_date = datetime(year, 9, calendar.monthrange(year, 9)[1], 23, 59, 59)
    elif quarter == 'Q4':
        start_date = datetime(year, 10, 1)
        end_date = datetime(year, 12, calendar.monthrange(year, 12)[1], 23, 59, 59)

    return start_date, end_date


## Initialization

# Load environment variables from a .env file if it exists
load_dotenv()

# Set your secret key from the environment variable
stripe.api_key = os.getenv('STRIPE_API_KEY')


## Main script

year, quarter = parse_quarter_arguments()

output_file_path = os.path.join(os.path.dirname(__file__), 'out', f'invoices_{year}_{quarter}.csv')

start_date, end_date = quarter_to_date(year, quarter)

print(f'Fetching invoices created between {start_date} and {end_date}...')
invoices = fetch_invoices(int(start_date.timestamp()), int(end_date.timestamp()))

print(f'Got {len(invoices)} invoices, writing to file...')
write_invoices_to_file(invoices, output_file_path)

print('Export completed.')
