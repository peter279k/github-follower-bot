import os
import requests
from requests.auth import HTTPBasicAuth


def fetch_followers(github_user, page):
    """Fetch a list of followers for a given GitHub user and page."""
    url = f"https://api.github.com/users/{github_user}/followers?page={page}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def follow_user(github_user, personal_token, user_to_follow):
    """Send a follow request to a specific user."""
    url = f"https://api.github.com/user/following/{user_to_follow}"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
        )
    }
    response = requests.put(
        url, auth=HTTPBasicAuth(github_user, personal_token), headers=headers
    )
    return response.status_code


def load_existing_followers(file_path):
    """Load the list of already followed users from a file."""
    if not os.path.exists(file_path):
        return set()
    with open(file_path, "r") as file:
        return set(file.read().strip().splitlines())


def save_new_follower(file_path, username):
    """Append a newly followed user to the file."""
    with open(file_path, "a") as file:
        file.write(f"{username}\n")


def save_follower_count(file_path, count):
    """Save the total number of followers fetched."""
    with open(file_path, "w") as file:
        file.write(f"{count}\n")


def main():
    print("Hi! I am GitHub follower bot.")
    print("Letting you follow your all followers!")
    print("Starting to fetch your follower list...\n")

    github_user = os.getenv("github_user")
    personal_github_token = os.getenv("personal_github_token")

    if not github_user or not personal_github_token:
        print("Error: Please set the 'github_user' and 'personal_github_token' environment variables.")
        return

    followers_file = "./followers.txt"
    follower_counter_file = "./follower_counter.txt"

    existing_followers = load_existing_followers(followers_file)
    follower_counter = 0
    page = 1

    while True:
        followers = fetch_followers(github_user, page)
        if not followers:
            break

        follower_counter += len(followers)
        for follower in followers:
            username = follower["login"]
            if username in existing_followers:
                continue

            status_code = follow_user(github_user, personal_github_token, username)
            if status_code == 204:
                print(f"User: {username} has been followed!")
                save_new_follower(followers_file, username)
            else:
                print(f"Failed to follow {username}. Status code: {status_code}")

        page += 1

    save_follower_count(follower_counter_file, follower_counter)
    print("\nFollowing users from your follower list is done!")


if __name__ == "__main__":
    main()
