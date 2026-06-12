from github_fetch import github_fetch
import threading

last_commit = None

def threding_git(git, stop_event):
    while not stop_event.is_set():
        new_commit, last_commit = git.get_last_commit()
        if not new_commit: stop_event.set()

if __name__ == '__main__':
    git = github_fetch('monci07/Linkdin-auto')
    
    stop_event = threading.Event()
    
    thread = threading.Thread(target=threding_git, args=(git,stop_event))
    thread.start()
    thread.join()
    
    while last_commit is None: pass
    
    print(f"SHA:     {last_commit.sha[:7]}")
    print(f"Autor:   {last_commit.commit.author.name}")
    print(f"Fecha:   {last_commit.commit.author.date}")
    print(f"Mensaje: {last_commit.commit.message[:80]}")
    print("---")
