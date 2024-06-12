# extract comments
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_github_issue(issue_url, api_token):
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': f'token {api_token}'
    }
    
    response = requests.get(issue_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception('Failed to load page {}'.format(issue_url))
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract issue tags
    tag_elements = soup.find_all('a', class_='IssueLabel')
    tags = [tag.text.strip() for tag in tag_elements]
    
    # Extract all comments and associated images
    comment_elements = soup.find_all('td', class_='comment-body')
    comments = []
    for comment_element in comment_elements:
        comment_text = comment_element.text.strip()
        comment_images = [img['src'] for img in comment_element.find_all('img')]
        comments.append((comment_text, comment_images))
    
    # Extract actions like mentions
    timeline_events = soup.find_all('div', class_='TimelineItem-body')
    actions = set()
    for event in timeline_events:
        user_mention = event.find('a', class_='author')
        
        if user_mention:
            relative_time = event.find('relative-time')
            if relative_time:
                date = relative_time.attrs['datetime']
            else:
                date = 'Unknown date'
            action_text = event.find('pre').text.strip() if event.find('pre') else ""
            action_entry = f"{user_mention.text.strip()} mentioned this issue on {date.split('T')[0]} \n{action_text}"
            actions.add(action_entry)
    
    return tags, comments, list(actions)