from groupme import *

if __name__ == "__main__":
    group_ids = get_group_ids()

    group_id = group_ids[0]

    messages = get_messages(group_id)

    print(messages)

