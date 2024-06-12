# -*- coding: utf-8 -*-
import sys
import requests
import collections
from openpyxl import Workbook
import csv

class GithubAPI:
    results = []
    raw = []
    issues_payload = {
        "per_page": 100,
        "page": 1,
        "state": "all",
    }
    
    def __init__(self, api_tokens):
        self.api_tokens = api_tokens
        self.api_token_index = 0  

    def getCommentHistory(self, url):
        comments = []
        self.issues_payload = {
            "per_page": 100,
            "page": 1,
            "state": "all",
        }
        self.raw = []
        headers = {'User-Agent': 'Mozilla/5.0'}

        while True:
            headers['Authorization'] = f'token {self.api_tokens[self.api_token_index]}'
            r = requests.get(url, params=self.issues_payload, headers=headers)

            if r.status_code == 200:
                break
            elif r.status_code == 403 and 'API rate limit exceeded' in r.text:
                
                self.api_token_index = (self.api_token_index + 1) % len(self.api_tokens)
            else:
                raise Exception(f'Failed to load page {url}. Status code: {r.status_code}')

        r = r.json()
        while (True):
            self.raw += r

            if len(r) == 100:
                self.issues_payload["page"] += 1
                headers['Authorization'] = f'token {self.api_tokens[self.api_token_index]}'
                r = requests.get(url, params=self.issues_payload, headers=headers).json()
            else:
                break

        for e in self.raw:
            print("Checking issue " + str(e["number"]))

            comment = collections.OrderedDict()
            issue["id"] = e["id"]
            issue["number"] = e["number"]
            issue["repo_url"] = e["repository_url"]
            issue["issue_url"] = e["url"]

            comments.append(comment)
        return comments

    def getIssues(self, url):
        self.issues_payload = {
            "per_page": 100,
            "page": 1,
            "state": "all",
        }

        self.raw = []
        headers = {'User-Agent': 'Mozilla/5.0'}

        while True:
            headers['Authorization'] = f'token {self.api_tokens[self.api_token_index]}'
            r = requests.get(url, params=self.issues_payload, headers=headers)

            if r.status_code == 200:
                break
            elif r.status_code == 403 and 'API rate limit exceeded' in r.text:
                # switch to next api
                self.api_token_index = (self.api_token_index + 1) % len(self.api_tokens)
            else:
                raise Exception(f'Failed to load page {url}. Status code: {r.status_code}')

        r = r.json()
        while (True):
            self.raw += r

            if len(r) == 100:
                self.issues_payload["page"] += 1
                headers['Authorization'] = f'token {self.api_tokens[self.api_token_index]}'
                r = requests.get(url, params=self.issues_payload, headers=headers).json()
            else:
                break

        for e in self.raw:
            print("Checking issue " + str(e["number"]))

            issue = collections.OrderedDict()
            issue["id"] = e["id"]
            issue["number"] = e["number"]
            issue["repo_url"] = e["repository_url"]
            issue["issue_url"] = e["url"]
            
            issue["state"] = e["state"]
            issue["html_url"] = e["html_url"]
            issue["title"] = e["title"]
          
            api_token = self.api_tokens[self.api_token_index]
            tags, comments = crawl_github_issue(issue["issue_url"], api_token)

            issue["created_at"] = e["created_at"]
            issue["updated_at"] = e["updated_at"]
            issue["closed_at"] = e["closed_at"]
            issue["tags"] = tags
            issue["comments"] = comments

            if not e["milestone"]:
                issue["milestone"] = "null"
            else:
                issue["milestone"] = e["milestone"]["title"]

            labels = []

            for label in e["labels"]:
                labelIssue = collections.OrderedDict()
                labelIssue["issue_repo_url"] = e["repository_url"]
                labelIssue["issue_id"] = e["id"]
                labelIssue["issue_number"] = e["number"]
                labelIssue["label_id"] = label["id"]
                labelIssue["label"] = label["name"]
                labels.append(labelIssue)

            issue["labels"] = labels

            self.results.append(issue)

        return self.results

if __name__ == "__main__":
    api_tokens = ['YOUR_GITHUB_API_TOKEN_1', 'YOUR_GITHUB_API_TOKEN_2']  
    apps = open('github_issues_url.csv', encoding='utf-8')
    csv_apps = csv.reader(apps)

    for row in csv_apps:
        try:
            app_source = row[0].replace("//github.com", "//api.github.com/repos")
        except:
            pass

        print("=============================")
        print(app_source)
        print("=============================")

        api = GithubAPI(api_tokens)

        print("Getting issues...")

        issues = api.getIssues(app_source)

        print("Creating issues.csv ...")

        # Create csv file
        with open("issues.csv", 'a', encoding='utf-8', newline="") as file:
            writer = csv.writer(file)

            writer.writerow(("id", "number", "issue_url", "repo_url", "events_url", "state", "html_url",
                             "milestone", "title", "created_at", "uploaded_at", "closed_at", "tags", "comments"))

            for issue in issues:
                writer.writerow((issue["id"], issue["number"], issue["issue_url"], issue["repo_url"], issue["state"],
                                 issue["html_url"], issue["milestone"], issue["title"],
                                 issue["created_at"], issue["updated_at"], issue["closed_at"], issue["tags"],
                                 issue["comments"]))

        # =======================================================================================
        print("Creating labels.csv...")

        with open("labels.csv", 'a', encoding='utf-8', newline="") as file:
            writer = csv.writer(file)

            writer.writerow(("issue_repo_url", "issue_id", "issue_number", "label_id", "label"))

            for issue in issues:
                labels = issue["labels"]
                for label in labels:
                    writer.writerow((label["issue_repo_url"], label["issue_id"], label["issue_number"],
                                     label["label_id"], label["label"]))