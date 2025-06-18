import sqlite3

conn = sqlite3.connect("ecofood.db")  # Connect to your database
cursor = conn.cursor()

cursor.execute("SELECT * FROM food_listing;")  # Fetch all food items
data = cursor.fetchall()

for row in data:
    print(row)  # Print all rows from the database

conn.close()
# ol {
#     list-style-type: decimal; /* Ensures numbers are used */
#     padding-left: 20px;
# }

# ol li {
#     font-weight: bold;
#     margin-bottom: 8px;
# }
