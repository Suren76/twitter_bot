import argparse

# from config import PATH_TO_FILES_DIR, PATH_TO_OUTPUT_DIRECTORY
import os

from main import like_tweets

# path = PATH_TO_FILES_DIR
# path_to_output_directory = PATH_TO_OUTPUT_DIRECTORY

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mode", help="get mode to run script")
parser.add_argument("--text", help="get mode to run script")

parser.add_argument("--likes-count", help="get count of likes to do")
parser.add_argument("--threads-count", help="get count of threads to run")

parser.add_argument("-links", "--links-file", help="get path to links data file ")
parser.add_argument("-login", "--login-data", help="get path to login data file")
parser.add_argument("-proxy", "--proxy-data", help="get path to login data file")

parser.add_argument("-driver", "--path-to-chromedriver", help=f"sets the path for chromedriver, default:http://localhost:4444/wd/hub")

parser.add_argument("-t", "--timeout", help="get timeout for like")
parser.add_argument("-T", "--timeout-accounts", help="get timeout for account change")
# parser.add_argument("-MA", "--move-archives", action='store_true')
# parser.add_argument("-OIS", "--old-image-search", action='store_true')
parser.add_argument("-show", "--no-headless", action='store_false')
# parser.add_argument("-hide", "--headless", action='store_true')
parser.add_argument("--DEBUG", action='store_true')


args = parser.parse_args()

# if args.shell:
#     while True:
#         pass

print(args)

# timeout = None
# login_data = None

path_to_chromedriver = "http://localhost:4444/wd/hub"
mode = None
headless = args.no_headless
text_to_search = None
likes_count = None
threads_count = None
links_file = None
login_data = None
proxy_data = None
timeout = None
timeout_accounts = None
# path_to_chromedriver = None

if args.mode:
    mode = args.mode

if args.text:
    text_to_search = args.text

if args.likes_count:
    likes_count = int(args.likes_count)
if args.threads_count:
    threads_count = int(args.threads_count)

if args.links_file:
    links_file = args.links_file
if args.login_data:
    login_data = args.login_data
if args.proxy_data:
    proxy_data = args.proxy_data

if args.timeout:
    timeout = int(args.timeout)
if args.timeout_accounts:
    timeout_accounts = int(args.timeout_accounts)

if args.path_to_chromedriver:
    path_to_chromedriver = args.path_to_chromedriver


like_tweets(
    mode=mode,
    likes_count=likes_count,
    threads_count=threads_count,
    links_file=links_file,
    login_data=login_data,
    proxy_data=proxy_data,
    timeout=timeout,
    timeout_accounts=timeout_accounts,
    path_to_chromedriver=path_to_chromedriver,
    text_to_search=text_to_search,
    headless=headless
)

# if args.result_limits:
#     result_limits_for_image_compare = int(args.result_limits)

