import sys
import requests
import collections
import csv
from crawlcomments import crawl_github_issue  # Ensure this is correctly importing your crawl_github_issue function

class GithubAPI:
    def __init__(self, username, token):
        self.results = []
        self.raw = []
        self.issues_payload = {
            "per_page": 100,
            "page": 1,
            "state": "all",
        }
        self.auth = (username, token)

    def getCommentHistory(self, url):
        comments = []
        self.issues_payload = {
            "per_page": 100,
            "page": 1,
            "state": "all",
        }
        self.raw = []
        r = requests.get(url, params=self.issues_payload, auth=self.auth).json()

        while True:
            self.raw += r

            if len(r) == 100:
                self.issues_payload["page"] += 1
                r = requests.get(url, params=self.issues_payload, auth=self.auth).json()
            else:
                break

        for e in self.raw:
            print("Checking issue " + str(e["number"]))

            comment = collections.OrderedDict()
            comment["id"] = e["id"]
            comment["number"] = e["number"]
            comment["repo_url"] = e["repository_url"]
            comment["issue_url"] = e["url"]

            comments.append(comment)

        return comments

    def getIssues(self, url):
        api_token = "your_github_api_token"  # Replace with your GitHub API token
        self.issues_payload = {
            "per_page": 100,
            "page": 1,
            "state": "all",
        }

        self.raw = []

        r = requests.get(url, params=self.issues_payload, auth=self.auth).json()

        while True:
            self.raw += r

            if len(r) == 100:
                self.issues_payload["page"] += 1
                r = requests.get(url, params=self.issues_payload, auth=self.auth).json()
            else:
                break

        for e in self.raw:
            # Skip pull requests
            if 'pull_request' in e:
                continue

            print("Checking issue " + str(e["number"]))

            issue = collections.OrderedDict()
            issue["id"] = e["id"]
            issue["number"] = e["number"]
            issue["repo_url"] = e["repository_url"]
            issue["issue_url"] = e["url"]
            issue["state"] = e["state"]
            issue["html_url"] = e["html_url"]
            issue["title"] = e["title"]
            tags, comments, actions = crawl_github_issue("https://github.com/yoheinakajima/instagraph/issues/" + str(e["number"]), api_token)

            issue["created_at"] = e["created_at"]
            issue["updated_at"] = e["updated_at"]
            issue["closed_at"] = e["closed_at"]
            issue["tags"] = tags
            issue["actions"] = actions
            issue["comments"] = comments

            if not e["milestone"]:
                issue["milestone"] = "null"
            else:
                issue["milestone"] = e["milestone"]["title"]

            self.results.append(issue)

        return self.results

if __name__ == "__main__":
    apps = open('github_issues_url.csv', encoding='utf-8')
    csv_apps = csv.reader(apps)

    for row in csv_apps:
        try:
            app_source = row[0].replace("//github.com", "//api.github.com/repos")
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

        print("=============================")
        print(app_source)
        print("=============================")

        api = GithubAPI("your_username", "your_github_token")  # Replace with your GitHub username and token

        print("Getting issues...")
        issues = api.getIssues(app_source)

        print("Creating issues.csv...")

        with open("issues.csv", 'a', encoding='utf-8', newline="") as file:
            writer = csv.writer(file)
            writer.writerow(("id", "number", "issue_url", "repo_url", "state", "html_url",
                             "milestone", "title", "created_at", "updated_at", "closed_at", "tags", "actions", "comments"))

            for issue in issues:
                writer.writerow((issue["id"], issue["number"], issue["issue_url"], issue["repo_url"], issue["state"],
                                 issue["html_url"], issue["milestone"], issue["title"],
                                 issue["created_at"], issue["updated_at"], issue["closed_at"], issue["tags"], issue["actions"], issue["comments"]))
