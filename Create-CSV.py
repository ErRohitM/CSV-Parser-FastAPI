import csv

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as csv_file:
        fieldnames = ['name', 'age']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        # Write header
        writer.writeheader()

        # Write data
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    # Example data
    data = [
        {'name': 'John', 'age': 25},
        {'name': 'Alice', 'age': 30},
        {'name': 'Bob', 'age': 22},
        {'name': 'Mary', 'age': 24},
        {'name': 'Rome', 'age': 32},
        {'name': 'Ram', 'age': 18},
    ]

    # File path to save the CSV
    file_path = "example.csv"

    # Write CSV file
    write_csv(file_path, data)

    print(f"CSV file '{file_path}' created successfully.")
