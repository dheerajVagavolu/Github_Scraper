from scrape import create_log, get_name

def main():
    collected = []

    if len(repos) == 0:
        print('No repos in the List file')
        exit()

    for url in repos:
        repo_name = get_name(url)
        if repo_name in logs:
            print("Already collected")
            print(logs)
        else:
            print(repo_name)
            test = create_log(url)
            if test != 0:
                collected.append(repo_name)
        
    clean_up(collected)

def clean_up(col):
    logs = open('../data/logs', 'a')
    for name in col:
        logs.write(name+'\n')


if __name__=="__main__":
    global logs
    global repos
    try:
        repos = open('list').readlines()
    except:
        print('List file not found')
        exit()

    logs = open('../data/logs').readlines()
    logs = [log.strip() for log in logs]
    while len(repos) - len(logs) > 0:
        logs = open('../data/logs').readlines()
        logs = [log.strip() for log in logs]
        main()
