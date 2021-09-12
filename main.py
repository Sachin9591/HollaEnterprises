import pandas as pd
import requests
import time

url = 'https://github.com/Sachin9591/HollaEnterprises/blob/main/qna_chitchat_professional_english.csv'
token = "1928970983:AAGjjDBE02HG5CWSiyYAGa64ito_l2u1emU"
df = pd.read_csv(url, key='\t')


def get_update_from_bot(update_id):
    global token
    base_url = 'https://api.telegram.org/bot{}/getUpdates?offset={}'.format(token, update_id)
    resp = requests.get(base_url)
    data = resp.json()
    return data


def auto_answer(message):
    answer = df.loc[df['Question'].str.upper() == message]
    if not answer.empty:
        answer = answer.iloc[0]['Answer']
        return answer
    else:
        return "Sorry, I couldn't understand you!. I'm still learning and try to get better in answering."


def reply_msg(item, answer):
    global token
    try:
        chat_id = item["message"]["chat"]["id"]
        user_id = item["message"]["from"]["id"]
        user_name = item["message"]["from"].get("username", user_id)
        welcome_msg = '''{}'''.format(answer)
        to_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML'\
            .format(token, chat_id, welcome_msg)
        resp = requests.get(to_url)
    except Exception as e:
        print(e)


def main():
    data = get_update_from_bot(0)
    while True:
        for item in data["result"]:
            update_id = item["update_id"]
            # chat_id = item["message"]["chat"]["id"]
            # user_id = item["message"]["from"]["id"]
            # user_name = item["message"]["from"]["username"]
            message = item["message"]["text"]
            answer = auto_answer(message.upper())
            reply_msg(item, answer)
        time.sleep(1)
        data = get_update_from_bot(update_id + 1)
        print(data)


if __name__ == '__main__':
    main()
