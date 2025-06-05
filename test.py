import csv

filename = "./assets/price_models.csv"

with open(filename, mode='r') as csvfile:
    # create a csv reader object from the file object
    csvreader = csv.DictReader(csvfile)
    # Convert to a list of dictionaries
    data = [row for row in csvreader]

nested_dict = {}
for item in data:
    model_name = item['model']
    # Remove the model key and store the rest as a nested dictionary
    model_data = {k: v for k, v in item.items() if k != 'model'}
    nested_dict[model_name] = model_data

print(nested_dict)