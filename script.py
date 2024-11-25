import requests
import argparse
import datetime
import logging

# Configure logging level
LOG_LEVEL = logging.DEBUG  # Change this to logging.INFO or logging.ERROR as needed

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=LOG_LEVEL
)

def parse_list_argument(arg):
    """
    Parse a comma-separated argument into a list.
    """
    return [item.strip() for item in arg.split(",")] if arg else []

def get_projects(gitlab_url, headers):
    """
    Fetch the list of accessible projects.
    """
    logging.debug("Fetching projects...")
    projects = []
    page = 1
    while True:
        url = f"{gitlab_url}/api/v4/projects?per_page=100&page={page}"
        logging.debug(f"Requesting projects from: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Error fetching projects: {response.text}")
            break
        data = response.json()
        if not data:
            logging.debug("No more projects found.")
            break
        projects.extend(data)
        logging.debug(f"Fetched {len(data)} projects.")
        page += 1
    return projects

def get_commits(gitlab_url, headers, project_id, start_date, end_date, users=None):
    """
    Fetch commits for a project within a specific date range.
    If users are specified, filter commits by author_email or author_name.
    """
    logging.debug(f"Fetching commits for project ID {project_id}...")
    commits = []
    page = 1
    while True:
        url = (
            f"{gitlab_url}/api/v4/projects/{project_id}/repository/commits"
            f"?since={start_date}&until={end_date}&per_page=100&page={page}"
        )
        logging.debug(f"Requesting commits from: {url}")
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Error fetching commits for project {project_id}: {response.text}")
            break
        data = response.json()
        if not data:
            logging.debug("No more commits found.")
            break
        # Filter commits by users if specified
        if users:
            data = [
                commit for commit in data
                if commit.get("author_name") in users or commit.get("author_email") in users
            ]
        commits.extend(data)
        logging.debug(f"Fetched {len(data)} commits.")
        page += 1
    return commits

def generate_report(gitlab_url, headers, start_date, end_date, users=None, project_names=None):
    """
    Generate a report of commits grouped by project.
    """
    logging.info("Generating report...")
    projects = get_projects(gitlab_url, headers)
    report = {}

    total_projects = len(projects)
    for index, project in enumerate(projects, start=1):
        # Skip projects if a specific project name list is provided and does not match
        if project_names and project["name"].lower() not in [name.lower() for name in project_names]:
            logging.debug(f"{index}/{total_projects} - Skipping project {project['name']} (does not match filter).")
            continue

        project_name_actual = project["name"]
        project_id = project["id"]
        logging.info(f"{index}/{total_projects} - Fetching commits for project: {project_name_actual}")
        commits = get_commits(gitlab_url, headers, project_id, start_date, end_date, users=users)
        if commits:
            report[project_name_actual] = [
                {"author": commit["author_name"], "message": commit["message"], "date": commit["created_at"]}
                for commit in commits
            ]
        else:
            logging.debug(f"No commits found for project: {project_name_actual}")
    return report

def save_report_to_file(report, filename="gitlab_report.txt"):
    """
    Save the report to a file with the specified formatting, ensuring no extra newlines in 'message'.
    """
    logging.info(f"Saving report to {filename}...")
    with open(filename, "w") as file:
        for project, commits in report.items():
            file.write(f"Project: {project}\n")
            for commit in commits:
                # Strip trailing newline from the message if present
                message = commit["message"].rstrip("\n")
                file.write(
                    f"  - Author: {commit['author']}\n"
                    f"    Message: {message}\n"
                    f"    Date: {commit['date']}\n\n"  # Add a blank line after Date
                )
            file.write("\n")  # Add an extra newline after each project
    logging.info(f"Report successfully saved to {filename}")

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Generate a GitLab commit report.")
    parser.add_argument("-s", "--starttime", required=True, help="Start date (format: YYYY-MM-DD)")
    parser.add_argument("-e", "--endtime", required=True, help="End date (format: YYYY-MM-DD)")
    parser.add_argument("-t", "--token", required=True, help="Personal Access Token for GitLab API")
    parser.add_argument("-g", "--gitlab", required=True, help="GitLab server URL (e.g., https://gitlab.example.com)")
    parser.add_argument("-u", "--user", help="Filter commits by a comma-separated list of users (author_name or author_email)")
    parser.add_argument("-p", "--project", help="Filter by a comma-separated list of project names")
    parser.add_argument("-o", "--output", default="gitlab_report.txt", help="Output file name (default: gitlab_report.txt)")

    args = parser.parse_args()

    # Parse comma-separated lists for users and projects
    users = parse_list_argument(args.user)
    project_names = parse_list_argument(args.project)

    # Set up headers for API requests
    headers = {"PRIVATE-TOKEN": args.token}

    # Format and validate dates
    try:
        start_date = f"{args.starttime}T00:00:00Z"
        end_date = f"{args.endtime}T23:59:59Z"
        datetime.datetime.strptime(args.starttime, "%Y-%m-%d")
        datetime.datetime.strptime(args.endtime, "%Y-%m-%d")
    except ValueError:
        logging.error("Dates must be in the format YYYY-MM-DD.")
        return

    # Generate the report
    logging.info("Starting the report generation process...")
    report = generate_report(args.gitlab, headers, start_date, end_date, users=users, project_names=project_names)

    # Save the report to a file
    save_report_to_file(report, filename=args.output)

if __name__ == "__main__":
    main()

