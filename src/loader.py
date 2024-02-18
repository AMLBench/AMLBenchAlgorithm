import os
import subprocess

import pandas

SEED = 1
RABOBANK_TRANSACTIONS_FILE = './data/rabobank_transactions.csv'
CASES_TRANSACTIONS_FILE = './data/cases_transactions.csv'


def parse_raw_rabo_data():
    transactions = pandas.read_csv(RABOBANK_TRANSACTIONS_FILE, sep=';',
                                   usecols=['start_id', 'total', 'count', 'end_id', 'year_from', 'year_to'])
    
    transactions = transactions.groupby(['start_id', 'end_id']).agg(
        {'total': 'sum', 'count': 'sum', 'year_from': 'min', 'year_to': 'max'}).reset_index()

    senders = transactions['start_id'].unique()
    receivers = transactions['end_id'].unique()
    accounts = pandas.DataFrame({'account_id': list(set(senders) | set(receivers))})
    return accounts, transactions


def parse_raw_cases_data():
    transactions = pandas.read_csv(CASES_TRANSACTIONS_FILE,
                                   usecols=['origin_id', 'target_id', 'amount', 'transaction_count', 'case_id'],
                                   dtype={'case_id': str})
    senders = transactions['origin_id'].unique()
    receivers = transactions['target_id'].unique()
    accounts = pandas.DataFrame({'account_id': list(set(senders) | set(receivers))})
    return accounts, transactions

def concat_data(rabo_accounts, cases_accounts, rabo_transactions, cases_transactions):
    rabo_accounts.insert(len(rabo_accounts.columns), 'is_ml', False)
    rabo_transactions.insert(len(rabo_transactions.columns), 'is_ml', False)
    cases_accounts.insert(len(cases_accounts.columns), 'is_ml', True)
    cases_transactions.insert(len(cases_transactions.columns), 'is_ml', True)

    rabo_transactions = rabo_transactions.rename(columns={'start_id': 'origin_id', 'total': 'amount', 'count': 'transaction_count', 'end_id': 'target_id'})
    rabo_transactions = rabo_transactions.drop(columns=['year_to', 'year_from'])

    new_ids = rabo_accounts['account_id'].sample(len(cases_accounts), random_state=SEED)
    old_ids = cases_accounts['account_id']

    for old_id, new_id in zip(old_ids, new_ids):
        cases_transactions[['origin_id', 'target_id']] = cases_transactions[['origin_id', 'target_id']].replace(
            to_replace=old_id, value=new_id)

    transactions = pandas.concat([rabo_transactions, cases_transactions], ignore_index=True)
    transactions['amount'] = transactions['amount'].astype(int)

    return transactions

def main():
    rabo_accounts, rabo_transactions = parse_raw_rabo_data()
    cases_accounts, cases_transactions = parse_raw_cases_data()
    transactions = concat_data(rabo_accounts, cases_accounts, rabo_transactions, cases_transactions)

    transactions.to_csv('amlbench_dataset.csv', index=None)

if __name__ == '__main__':
    main()
