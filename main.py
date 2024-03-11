import configparser
import json
from datetime import datetime

from github import Github


def confirm_action(message: str):
    while True:
        print(message)
        confirmation = input("Are you sure you want to proceed? (Y/N) ").strip().lower()
        if confirmation in ["y", "n"]:
            break
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")

    if confirmation == "y":
        return True
    else:
        return False


def printline(message: str):
    print(message)
    print()


config = configparser.ConfigParser()
config.read('config.ini')

access_token = config.get('github', 'token')
repo_name = config.get('github', 'repo')
pr_num_start_from_before = int(config.get('github', 'startFromBeforePRNumber'))
print(access_token)

# Authenticate with GitHub API
g = Github(access_token)

# Get the repository
repo = g.get_repo(repo_name)

if confirm_action("Going to connect to Github and fetch all the repositories review history data.") == True:
    # Fetch pull requests
    pull_requests = repo.get_pulls(state="closed")

    # Loop through pull requests and extract data
    data = []
    batch_size = 1000

    printline("Start processing Pull Requests (PRs) found ...")
    for pr in pull_requests:
        try:
            if (pr_num_start_from_before > 0 and pr.number > pr_num_start_from_before):
                printline(f"Skipping PR #{pr.number}")
                continue
            printline(f"Processing PR #{pr.number}")
            # Extract code diffs
            files = pr.get_files()
            printline(f"Process files for PR #{pr.number} ...")
            for file in files:
                review_data = {
                    "review_id": f"{pr.number}_{file.filename}",
                    "pull_request_id": pr.number,
                    "file_path": file.filename,
                    "diff": file.patch,
                    "comments": [],
                    "review_state": None,
                    "reviewer": None,
                    "review_timestamp": None
                }

                # Extract review comments
                review_comments = pr.get_review_comments()
                printline(f"Process review comments for PR #{pr.number} ...")
                for comment in review_comments:
                    if comment.path == file.filename:
                        comment_data = {
                            "comment_id": comment.id,
                            "author": comment.user.login,
                            "comment_body": comment.body,
                            "timestamp": str(comment.created_at),
                            "line_number": comment.position,
                            "line_code": None,
                            "conversation": []
                        }

                        # Extract conversation
                        conversation_comments = [c for c in review_comments if
                                                 c.position == comment.position and c.path == file.filename and c.id != comment.id]
                        printline(f"Process conversation comments for PR #{pr.number} ...")
                        for response in conversation_comments:
                            response_data = {
                                "comment_id": response.id,
                                "author": response.user.login,
                                "comment_body": response.body,
                                "timestamp": str(response.created_at)
                            }
                            comment_data["conversation"].append(response_data)

                        review_data["comments"].append(comment_data)

                # Extract issue comments
                issue_comments = pr.get_issue_comments()
                printline(f"Process issue comments for PR #{pr.number} ...")
                for comment in issue_comments:
                    comment_data = {
                        "comment_id": comment.id,
                        "author": comment.user.login,
                        "comment_body": comment.body,
                        "timestamp": str(comment.created_at),
                        "line_number": None,
                        "line_code": None,
                        "conversation": []
                    }
                    review_data["comments"].append(comment_data)

                # Extract reviews
                reviews = pr.get_reviews()
                printline(f"Process reviews for PR #{pr.number} ...")
                for review in reviews:
                    if review.commit_id == file.sha:
                        review_data["review_state"] = review.state
                        review_data["reviewer"] = review.user.login
                        review_data["review_timestamp"] = str(review.submitted_at)

                data.append(review_data)

                # Write data to JSONL file if data so far is greater than 1000 lines and clear the data
                if len(data) >= batch_size:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    filename = f"data_{timestamp}.jsonl"
                    with open(filename, "a", encoding="utf-8") as f:
                        for item in data:
                            f.write(json.dumps(item) + "\n")
                    print(f"File written to {filename} with 1000 or more lines and cleared data")
                    data = []

        except Exception as e:
            error_message = f"Error processing pull request #{pr.number}: {str(e)}"
            print(error_message)
            with open("error.log", "a", encoding="utf-8") as error_log:
                error_log.write(f"{datetime.now()} - {error_message}\n")
            continue
