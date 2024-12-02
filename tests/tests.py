import requests
import random
import time
import pandas as pd

BASE_URL = "http://127.0.0.1:5000"

HEADERS = {
    "Connection": "Close"
}

def populate_books(count):
    """
    Inserts multiple book records into the database for testing purposes.

    Args:
        count (int): The number of records to insert.
    """
    for i in range(count):
        data = {
            "title": f"Book_{i}",
            "author": f"Author_{random.randint(1, 100)}",
            "year": random.randint(1900, 2024),
            "category_id": random.randint(1, 5)  #
        }
        response = requests.post(f"{BASE_URL}/books", json=data, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error inserting data: {response.json()}")

def measure_execution_time(func, *args):
    """
    Measures the execution time of a given function.

    Args:
        func (function): The function to measure.
        *args: Arguments to pass to the function.

    Returns:
        float: The execution time in seconds.
    """
    start_time = time.time()
    func(*args)
    return time.time() - start_time

def test_select_books():
    """Performs a GET request to retrieve all book records."""
    response = requests.get(f"{BASE_URL}/books", headers=HEADERS)
    if response.status_code != 200:
        print(f"Error fetching data: {response.json()}")

def test_insert_book():
    """Performs a POST request to insert a single test book record."""
    data = {
        "title": "Test_Book",
        "author": "Test_Author",
        "year": 2024,
        "category_id": 1
    }
    response = requests.post(f"{BASE_URL}/books", json=data, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error inserting data: {response.json()}")

def test_update_book():
    """Performs a PUT request to update a specific book record."""
    data = {
        "title": "Updated_Book",
        "author": "Updated_Author",
        "year": 2024,
        "category_id": 1
    }
    response = requests.put(f"{BASE_URL}/books/1", json=data, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error updating data: {response.json()}")

def test_delete_book():
    """Performs a DELETE request to remove a specific book record."""
    response = requests.delete(f"{BASE_URL}/books/1", headers=HEADERS)
    if response.status_code != 200:
        print(f"Error deleting data: {response.json()}")

def run_tests(test_sizes):
    """
    Runs API performance tests for specified record sizes.

    Args:
        test_sizes (list): A list of record sizes to test.

    Returns:
        pd.DataFrame: A DataFrame containing performance metrics.
    """
    results = []

    for size in test_sizes:
        print(f"Testing with {size} records...")

   
        populate_time = measure_execution_time(populate_books, size)

        select_time = measure_execution_time(test_select_books)
        insert_time = measure_execution_time(test_insert_book)
        update_time = measure_execution_time(test_update_book)
        delete_time = measure_execution_time(test_delete_book)


        results.append({
            "size": size,
            "populate_time": populate_time,
            "select_time": select_time,
            "insert_time": insert_time,
            "update_time": update_time,
            "delete_time": delete_time
        })

        print(f"Completed testing for {size} records.")

    return pd.DataFrame(results)

if __name__ == "__main__":
    TEST_SIZES = [1000, 10000]
    results_df = run_tests(TEST_SIZES)


    results_file = "results.csv"
    results_df.to_csv(results_file, index=False)
    print(f"Results saved to {results_file}")