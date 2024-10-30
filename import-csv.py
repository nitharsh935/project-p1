import csv
import datetime
import random
import string

# Function to generate random user data
def generate_user_data():
    login = ''.join(random.choices(string.ascii_lowercase, k=8))
    name = ' '.join(random.choices(string.ascii_capitalize, k=2))
    company = random.choice(['GITHUB', 'SHOPIFY', 'MICROSOFT', 'AMAZON', 'GOOGLE'])
    location = 'Toronto'
    email = f"{login}@example.com"
    hireable = random.choice([True, False])
    bio = ' '.join(random.choices(string.ascii_letters, k=random.randint(50, 150)))
    public_repos = random.randint(25, 150)
    followers = random.randint(500, 10000)
    following = random.randint(50, 500)
    created_at = datetime.datetime(
        random.randint(2006, 2023),
        random.randint(1, 12),
        random.randint(1, 28),
        random.randint(0, 23),
        random.randint(0, 59),
        random.randint(0, 59)
    ).isoformat()
    return [login, name, company, location, email, hireable, bio, public_repos, followers, following, created_at]

# Generate and write to CSV file
with open('users.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['login', 'name', 'company', 'location', 'email', 'hireable', 'bio', 'public_repos', 'followers', 'following', 'created_at'])
    for _ in range(638):
        writer.writerow(generate_user_data())
