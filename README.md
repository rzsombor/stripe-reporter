# Stripe Reporter

This script generates a report of Stripe invoices for a specific year and quarter. The report is saved as a CSV file.

## Prerequisites

- Python 3.x
- pip (Python package installer)
- A Stripe account with API keys

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/stripe-reporter.git
    cd stripe-reporter
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory of the project and add your Stripe secret key:
    ```env
    STRIPE_API_KEY=your_stripe_secret_key
    ```

## Usage

Run the script with the desired year and quarter as arguments:

```sh
python main.py --year <year> --quarter <Q1|Q2|Q3|Q4>
```

For example, to generate a report for the first quarter of 2023:

```sh
python main.py --year 2023 --quarter Q1
```

The script will fetch the invoices from Stripe and save them to a CSV file in the `out` directory.

## Output

The output CSV file will have the following columns:
- Invoice ID
- Created
- Due Date
- Paid At
- Amount Paid
- Currency
- Payment Status

## License

This project is licensed under the MIT License.