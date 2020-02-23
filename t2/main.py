import json
import ssl
import urllib.error
import urllib.request

import twurl


def read_data(acct: str) -> dict:
    """Reads json file using API."""
    twitter_url = 'https://api.twitter.com/1.1/friends/list.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = twurl.augment(twitter_url, {'screen_name': acct, 'count': '42'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)

    return js


def get_info(data):
    stack = [data]
    directories = []

    def help_screen():
        print("\nCommands:")
        print("  help".ljust(21, ' '), "Show this screen.")
        print("  <directory_name>".ljust(21, ' '),
              "Move from a current working directory into another.")
        print("  ..".ljust(21, ' '), "Go up one directory.")
        print("  exit".ljust(21, ' '), "Exit module.\n")

    help_screen()
    while True:
        if isinstance(data, dict):
            print('    '.join(data.keys()))
        elif isinstance(data, list):
            print(f"You've reached a list. Enter an index in range from 0 to "
                  f"{len(data) - 1} to move from a current working directory "
                  f"into another.")
            print(data)
        else:
            print(data)
            print("You've reached the end of the path. Enter .. command to go "
                  "up one directory.")

        user_input = input('/'.join(directories) + '>')
        print('')

        if user_input == 'help':
            help_screen()
            continue
        elif user_input == '..':
            try:
                data = stack[-2]
                stack.pop()
                directories.pop()
                continue
            except IndexError:
                continue
        elif user_input == 'exit':
            break

        try:
            if isinstance(data, dict):
                data = data[user_input]
                stack.append(data)
                directories.append(user_input)
            elif isinstance(data, list):
                data = data[int(user_input)]
                stack.append(data)
                directories.append(user_input)
            else:
                print(user_input, "command or directory not found.")
        except (ValueError, IndexError):
            print(user_input, "command or directory not found.")


if __name__ == '__main__':
    try:
        ACCT = input('Enter a Twitter account: ')
        DATA = read_data(ACCT)
        get_info(DATA)
    except:
        print("Enter a valid Twitter account.")
