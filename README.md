# gitlab-reporter

This script is designed to fetch and display a structured summary of commits from GitLab projects using the GitLab API. \
The output groups commits by project, showing the author, commit message, and timestamp.

Example:
```sh
Project: group_1/project_1
  - Author: user_1
    Message: Added Priority parameter. issue: #205
    Date: 2024-11-21T15:25:22.000+01:00

  - Author: user_2
    Message: Remove unused code
    Date: 2024-11-20T18:12:40.000+01:00

Project: group_3/project_1
  - Author: user_1
    Message: Fix bug on Shop table
    Date: 2024-11-22T10:47:05.000+01:00
```

## Getting started

Run the following command to execute the script using Docker

```sh
docker run -it --rm -v $(pwd):/opt -w /opt python:3.12.5 bash -c "pip install -r requirements.txt && clear && python script.py --help"

usage: script.py [-h] -s STARTTIME -e ENDTIME -t TOKEN -g GITLAB [-u USER] [-p PROJECT] [-o OUTPUT]

Generate a GitLab commit report.

options:
  -h, --help            show this help message and exit
  -s STARTTIME, --starttime STARTTIME
                        Start date (format: YYYY-MM-DD)
  -e ENDTIME, --endtime ENDTIME
                        End date (format: YYYY-MM-DD)
  -t TOKEN, --token TOKEN
                        Personal Access Token for GitLab API
  -g GITLAB, --gitlab GITLAB
                        GitLab server URL (e.g., https://gitlab.example.com)
  -u USER, --user USER  Filter commits by a comma-separated list of users (author_name or author_email)
  -p PROJECT, --project PROJECT
                        Filter by a comma-separated list of project names
  -o OUTPUT, --output OUTPUT
                        Output file name (default: gitlab_report.txt)
```

## Example

Generate a report for a specific date and user:
```sh
docker run -it --rm -v $(pwd):/opt -w /opt python:3.12.5 bash -c "pip install -r requirements.txt && clear && python script.py -s 2024-11-22 -e 2024-11-22 -t <PERSONAL_ACCESS_TOKEN> -g https://gitlab.com -u mario.rossi@mail.com"
```

Generate a report for multiple projects and a specific user:
```sh
docker run -it --rm -v $(pwd):/opt -w /opt python:3.12.5 bash -c "pip install -r requirements.txt && clear && python script.py -s 2024-11-22 -e 2024-11-22 -t <PERSONAL_ACCESS_TOKEN> -g https://gitlab.com -p proxysql,dante8 -u mario.rossi@mail.com"
```

Generate a report for a single project and multiple users:
```sh
docker run -it --rm -v $(pwd):/opt -w /opt python:3.12.5 bash -c "pip install -r requirements.txt && clear && python script.py -s 2024-11-22 -e 2024-11-22 -t <PERSONAL_ACCESS_TOKEN> -g https://gitlab.com -u mario.rossi@mail.com,antonio.bianchi@mail.com -p bea"
```

# Contribute
Thanks to your contributions!

Here is a list of users who already contributed to this repository: \
<a href="https://github.com/vlauciani/gitlab-reporter/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=vlauciani/gitlab-reporter" />
</a>

# Author
(c) 2024 Valentino Lauciani valentino.lauciani[at]ingv.it

Istituto Nazionale di Geofisica e Vulcanologia, Italia
