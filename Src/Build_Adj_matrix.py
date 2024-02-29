import csv
from collections import defaultdict
import buildNet


network = buildNet.internationalRouting()
placeholder = defaultdict(list)

def initialize_variable(name, value):
    # Use globals() to set the variable in the global scope
    globals()[name] = value


with open('Database/neighbours.csv', 'r', newline='', encoding='utf-8') as file1:
    reader = csv.reader(file1)
    next(reader)  # Skip header row
    for row in reader:
        country = row[0]
        for key, values in network.items():
            try:
                x = values[0]
                for key2, values2 in x.items():
                    city = key2
                    placeholder[city].append(values2)
            except:
                pass
with open('Database/AdjMatrix.csv', 'w', newline='', encoding='utf-8') as Adjacency_Matrix:
        writer = csv.writer(Adjacency_Matrix)
        writer.writerow(['City', 'Connection 1', 'Distance 1', 'Connection 2', 'Distance 2', 'Connection 3', 'Distance 3', 'Connection 4', 'Distance 4', 'Connection 5', 'Distance 5', 'Connection 6', 'Distance 6'])
        for key, values in placeholder.items():
                city = key
                for i in range(0, 6):
                    try:
                        x = str('Connection ') + str(i)
                        y = str('Distance ') + str(i)
                        initialize_variable(x, values[1])
                        initialize_variable(y, values[0])
                    except:
                         pass
                     
with open('Database/AdjMatrix.csv', 'w', newline='', encoding='utf-8') as Adjacency_Matrix:
    writer = csv.writer(Adjacency_Matrix)
    writer.writerow(['City', 'Connection 1', 'Distance 1', 'Connection 2', 'Distance 2', 'Connection 3', 'Distance 3', 'Connection 4', 'Distance 4', 'Connection 5', 'Distance 5', 'Connection 6', 'Distance 6'])
    
    
    for i in range(0, len(placeholder.items())):
        for city, values in placeholder.items():
            row_data = [city]  # Initialize row data with city name
            for j in range(6):
                if j < (len(values[i])):
                    connection = values[i][j][1]  # Extract city name from values
                    distance = values[i][j][0]     # Extract distance from values
                    row_data.extend([connection, distance])  # Add connection and distance to row data
                else:
                    row_data.extend([None, None])  # If index exceeds the length of values, add None
            writer.writerow(row_data)