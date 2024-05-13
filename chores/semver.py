from git import Repo

repo = Repo('.')


def write_semver():
    with open('VERSION.txt', 'w') as f:
        f.write(get_semver())


def get_semver():
    version = "0.0.0"
    commits = reversed(list(repo.iter_commits()))
    for c in commits:
        version_splitted = version.split(".")
        msg = c.message.lower()
        if msg.startswith("breaking:"):
            version = f"{int(version_splitted[0]) + 1}.0.0"
        elif msg.startswith("feat:"):
            version = f"{version_splitted[0]}.{int(version_splitted[1]) + 1}.{version_splitted[2]}"
        elif msg.startswith("fix:") or msg.startswith("perf:"):
            version = f"{version_splitted[0]}.{version_splitted[1]}.{int(version_splitted[2]) + 1}"
    return version


if __name__ == '__main__':
    write_semver()
