from github_fetch import github_fetch
from claude_call import claude_call
import threading

last_commit = None

def threding_git(git, stop_event):
    global last_commit
    while not stop_event.is_set():
        new_commit, last_commit = git.get_last_commit()
        if not new_commit: stop_event.set()

if __name__ == '__main__':
    project = 'monci07/Linkdin-auto'
    git = github_fetch(project)
    claude = claude_call()
    message = "\
You are me — a data science student actively job hunting. \
I just pushed a commit to my project about A program that automates the publication of updates on LinkedIn. \
Commit message: {git_message}. \
Project link: https://github.com/{project}\
Write a short LinkedIn post (3-5 lines max) about this update. \
Tone: genuine, mildly enthusiastic, professional but human. \
Avoid generic phrases like 'excited to share', 'thrilled to announce', or 'on my journey'. \
Integrate the project link naturally. No hashtag spam — max 2 relevant ones."
    while True:
        stop_event = threading.Event()
        
        thread = threading.Thread(target=threding_git, args=(git,stop_event))
        thread.start()
        thread.join()
        
        
        response = claude.call(message.format(git_message=last_commit.commit.message.split('\n\n')[1], project = project))
        print(response)

