import csv
import sqlite3
import os

#shape-specific number
die_max = 4

print("Quick reminder to make sure you have made all necessary corrections to flagged items.")
input("Press Enter to continue.")

#create labels for the csv
labels = []
for i in range(0, die_max):
    labels.append("roll_" + str(i+1))

#initialize count for all possible values
count = []
for i in range(0, die_max):
    count.append(0)

if not os.path.exists('dice.db'):
    input("dice.db does not exist.  Exiting.")
    sys.exit()
conn = sqlite3.connect('dice.db')
cursor = conn.cursor()
cursor.execute('select label, path from rolls')
raw = cursor.fetchall()
conn.commit()
conn.close()
#count occurrences of all values
for value in raw:
    if int(value[0]) <= die_max and int(value[0]) > 0:
        count[int(value[0])-1] += 1
    else:
        print(f"Weird value: {value[0]}")

data = [labels, count]

try:
    with open('roll_tally.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data)  # Write all rows
    print(f"Data successfully saved to roll_tally.csv.")
except Exception as e:
    print(f"An error occurred: {e}")

total = 0
for value in count:
    total += value
print(f'{total} rolls counted')

for i in range(0, die_max):
    print(f"Roll {i+1}: " + str(count[i]))
