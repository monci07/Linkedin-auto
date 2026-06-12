from github import Github

class github_fetch:
    repo = None
    last_sha = None
    
    def __init__(self, repo: str):
        try:
            g = Github("")
            self.repo = g.get_repo(repo)
            commits = self.repo.get_commits()
            self.last_sha = commits[0].sha[:7]
            print('github info stored')
        except Exception as e:
            print(f"Error:\n{e}")

    def get_last_commit(self):
        commits = self.repo.get_commits()
        last_commit = commits[0]
        if last_commit.sha[:7] != self.last_sha:
            print('There is a new commit')
        else:
            print("There hasn't been a new commit")

        # for commit in commits[:10]:
        #     print(f"SHA:     {commit.sha[:7]}")
        #     print(f"Autor:   {commit.commit.author.name}")
        #     print(f"Fecha:   {commit.commit.author.date}")
        #     print(f"Mensaje: {commit.commit.message[:80]}")
        #     print("---")