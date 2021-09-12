# CTFd API endpoint
host = "https://ctfd.io"

# CTFd API token
api_token = ""

# How frequently to check for new solves
poll_period = 10

# Discord webhook url
webhook_url = ""

# Available template variables are:
# User Name (if individual mode) / Team Name (if team mode): {user_name}
# Challenge Name: {chal_name}
first_blood_announce_string = "First Blood for challenge **{chal_name}** goes to **{user_name}**! :knife: :drop_of_blood:"

# To be used with announce_all_solves
solve_announce_string = "**{user_name}** just solved **{chal_name}**!"

# Whether or not to announce all solves as well as first bloods
announce_all_solves = True
