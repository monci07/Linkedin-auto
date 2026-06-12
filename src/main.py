from github_fetch import github_fetch
import threading

def threding_git(git, stop_event):
    i = 0
    while not stop_event.is_set():
        git.get_last_commit()
        i += 1
        if i == 100: stop_event.set()

if __name__ == '__main__':
    git = github_fetch('monci07/Linkdin-auto')
    
    stop_event = threading.Event()
    
    thread = threading.Thread(target=threding_git, args=(git,stop_event))
    thread.start()
    thread.join()