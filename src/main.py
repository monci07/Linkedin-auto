from github_fetch import github_fetch
from claude_call import claude_call

import threading
import requests
import json

last_commit = None

def get_keys():
    with open('keys.json', 'r') as f:
        data = json.load(f)
        return data


def threding_git(git, stop_event):
    global last_commit
    while not stop_event.is_set():
        new_commit, last_commit = git.get_last_commit()
        if not new_commit: stop_event.set()

if __name__ == '__main__':
    keys = get_keys()
    project = 'monci07/Linkdin-auto'
    git = github_fetch(keys['Github'],project)
    claude = claude_call(keys['Claude'])
    message = "\
You are me — a data science student actively job hunting. \
I just pushed a commit to my project about A program that automates the publication of updates on LinkedIn. \
Commit message: {git_message}. \
Project link: https://github.com/{project} \
Write a short LinkedIn post (3-5 lines max) about this update. \
Tone: genuine, mildly enthusiastic, professional but human. \
Avoid generic phrases like 'excited to share', 'thrilled to announce', or 'on my journey'. \
Avoid using emojis, unless it marks the end of the project. \
Integrate the project link naturally. No hashtag spam — max 2 relevant ones. \
Don't give to much information about the project, keep it vague. \
Return only the post text, no introduction, no '---', no extra commentary."

    query = """
mutation {
  createPost(input: {
    text: "{Response}"
    channelId: "{ID}"
    schedulingType: automatic
    mode: addToQueue
  }) {
    ... on PostActionSuccess {
      post {
        id
        text
        status
      }
    }
    ... on MutationError {
      message
    }
  }
}
"""

    while True:
        stop_event = threading.Event()

        thread = threading.Thread(target=threding_git, args=(git,stop_event))
        thread.start()
        thread.join()
        
        response_claude = claude.call(message.format(git_message=last_commit.commit.message.split('\n\n')[1], project = project)).replace('"', '\\"')
        

        response = requests.post(
            "https://api.buffer.com",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {keys['Buffer']}",
            },
            json={
                "query": query.replace('{Response}',response_claude).replace('{ID}', keys['ChannelID(linkedin)'])
            },
        )

        data = response.json()
        print(data)