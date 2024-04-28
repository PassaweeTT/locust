from locust import HttpUser, task, between
import csv
import random

class ApiUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        with open("country.csv", "r") as f:
            reader = csv.DictReader(f)
            self.countries = [row["Code"] for row in reader]

    @task
    def get_top_headlines(self):
        country_code = random.choice(self.countries).lower()
        url = f"https://newsapi.org/v2/top-headlines?country={country_code}&apiKey=8a95d6fc34c845a5a6467fea09f93bcd"
        response = self.client.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            print(f"Top headlines from {country_code}")
            for article in articles[:5]:
                print(f"------------------------------------------------------------------\nTitle: {article.get('title')} \nSource: {article.get('source', {}).get('name')} \n------------------------------------------------------------------\n")
