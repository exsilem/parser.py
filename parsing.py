import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs


def parsing(email, password):
    useragent = UserAgent()

    headers = {
        "user-agent": useragent.random
    }

    data = {
        "LoginForm[username]": email,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0"
    }

    response = requests.post("https://kcodeclass.s20.online/login?backUrl=https%3A%2F%2Fkcodeclass.s20.online%2F",
                             headers=headers, data=data)

    days = ["Понедельник,", "Вторник,", "Среда,", "Четверг,", "Пятница,", "Суббота,", "Воскресенье,"]

    buf = bs(response.text, 'lxml')
    text = buf.find(class_="table-responsive").text
    text = text.replace("\n", "").split()
    title = ' '.join(text[:5])
    title += ":"
    text = text[5:]

    for i in range(len(text)):
        if text[i] in days:
            index = days.index(text[i])
            i += 1
            while text[i] not in days and i < len(text)-1:
                days[index] = days[index] + " " + text[i]
                i += 1

    days = [i.replace(',', ':') for i in days]
    days = '\n'.join(days)
    return days


def test_request(email, password):
    useragent = UserAgent()

    headers = {
        "user-agent": useragent.random
    }

    data = {
        "LoginForm[username]": email,
        "LoginForm[password]": password,
        "LoginForm[rememberMe]": "0"
    }

    response = requests.post("https://kcodeclass.s20.online/login?backUrl=https%3A%2F%2Fkcodeclass.s20.online%2F",
                             headers=headers, data=data)
    buf = bs(response.text, 'lxml')
    text = buf.find(class_="table-responsive")
    if text is None:
        return False
    else:
        return True


