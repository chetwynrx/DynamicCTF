import mysql.connector
import MySQLdb
import random

# List of random English names (you can replace this with your own dataset)
names = [
    "John Smith",
    "Jane Doe",
    "Michael Johnson",
    "Emily Williams",
    "Christopher Brown",
    "Amanda Jones",
    "David Garcia",
    "Sarah Martinez",
    "James Miller",
    "Jessica Davis",
    "Robert Rodriguez",
    "Jennifer Hernandez",
    "Daniel Lopez",
    "Ashley Gonzalez",
    "William Wilson",
    "Mary Anderson",
    "Matthew Taylor",
    "Elizabeth Thomas",
    "Joseph Lee",
    "Patricia Moore"
]

# Connect to MySQL database
conn = MySQLdb.connect(user='root', password='password', host='127.0.0.1:3306', database='usersdb')

cursor = conn.cursor()

# Create the tables table
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    userid INT PRIMARY KEY,
                    username VARCHAR(50),
                    password VARCHAR(50),
                    firstname VARCHAR(50),
                    lastname VARCHAR(50),
                    email VARCHAR(100)
                )''')

# Function to generate random users
def generate_users(num_users):
    users = []
    for i in range(num_users):
        userid = i + 1
        username = f'user{userid}'
        password = f'password{userid}'
        name = random.choice(names).split()
        firstname = name[0]
        lastname = name[1]
        email = f'user{userid}@example.com'
        users.append((userid, username, password, firstname, lastname, email))
    return users

# Generate 100 random users
random_users = generate_users(100)

# Insert users into the tables table
cursor.executemany('''INSERT INTO users (userid, username, password, firstname, lastname, email)
                      VALUES (%s, %s, %s, %s, %s, %s)''', random_users)

# Commit changes and close the connection
conn.commit()
conn.close()
