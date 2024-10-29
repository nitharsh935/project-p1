import requests
from os import environ
import csv
from time import sleep
from sys import argv

headers = {"Authorization": f"token {environ['GITHUB_TOKEN']}"}

def get_users_by_city_and_followers(city, min_followers, max_results):
    users = []
    page = 1

    while len(users) < max_results:
        url = f"https://api.github.com/search/users?q=location:{city}+followers:>{min_followers}&per_page=20&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            new_users = response.json().get('items', [])
            users.extend(new_users)
            if len(new_users) == 0 or len(users) >= max_results:
                break
            page += 1
        else:
            print(f"Error: {response.status_code}")
            break
    
    return users[:max_results]


def clean_company_name(company_name):
    if company_name:
        company_name = company_name.strip().lstrip('@').upper()
    return company_name

def get_user_details(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        
        # Format and clean data as per requirements
        user_details = {
            "login": user_data.get("login"),
            "name": user_data.get("name"),
            "company": clean_company_name(user_data.get("company")),
            "location": user_data.get("location"),
            "email": user_data.get("email"),
            "hireable": user_data.get("hireable"),
            "bio": user_data.get("bio"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "created_at": user_data.get("created_at")
        }
        return user_details
    else:
        print(f"Error fetching details for user {username}: {response.status_code}")
        return {}
    
def read_csv(input_name):
    results = []
    with open(input_name) as csvfile_reader:
        reader = csv.reader(csvfile_reader) 
        for row in reader:
            results.append(row)
    return results

def write_csv(output_name,rows):
    with open(output_name,"w") as csvfile_writer:
        wtr = csv.writer(csvfile_writer)
        wtr.writerows (rows)
    print(f"{len(rows)} rows written to {output_name}")

def get_user_repos(username, max_repos_per_user):
    url = f"https://api.github.com/users/{username}/repos?sort=pushed&per_page=20"
    all_repos = []
    page = 1

    while len(all_repos) < max_repos_per_user:
        response = requests.get(f"{url}&page={page}", headers=headers)
    
        if response.status_code == 403:
            print("Rate limit reached. Waiting for 30 seconds...")
            sleep(30)
            continue

        if response.status_code == 200:
            repos = response.json()
            if not repos:
                break
            all_repos.extend(repos)
            page += 1
        else:
            print(f"Error fetching repos for {username}: {response.status_code}")
            break

    return all_repos[:max_repos_per_user]


def get_repositories(username,max_repos_per_user):
    repos = get_user_repos(username,max_repos_per_user)
    repository_data = []
    for repo in repos:
        repository_data.append(list({
            "login": username,
            "full_name": repo.get("full_name"),
            "created_at": repo.get("created_at"),
            "stargazers_count": repo.get("stargazers_count"),
            "watchers_count": repo.get("watchers_count"),
            "language": repo.get("language"),
            "has_projects": repo.get("has_projects"),
            "has_wiki": repo.get("has_wiki"),
            "license_name": repo["license"]["key"] if repo.get("license") else None
        }.values()))
    return repository_data


def fetch_and_write_users_to_csv(city, min_followers,max_results):
    users = get_users_by_city_and_followers(city, min_followers,max_results)
    print(f"Number of users from API from city '{city}' and min followers '{min_followers}' is '{len(users)}'")
    user_details_list=[]
    for user in users:
        username = user["login"]
        user_details = get_user_details(username)
        if user_details:
            user_details_list.append(list(user_details.values()))
    write_csv("users.csv",user_details_list)


def get_repo_and_write_to_file(max_repos_per_user):
    repo_details=[]
    for user_detail in read_csv("users.csv"):
        user_name=user_detail[0]
        repo_details.extend(get_repositories(user_name,max_repos_per_user))
    write_csv("repositories.csv",repo_details)

if __name__=="__main__":
    country_name="San Francisco"
    min_followers=20
    max_user_results=20
    max_repos_per_user=20
    fetch_and_write_users_to_csv(country_name,min_followers,max_user_results)
    get_repo_and_write_to_file(max_repos_per_user)

