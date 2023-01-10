import alfred
import requests
from datetime import date, timedelta
from keys import api_key, api_url


def get(day_offset):
    day = date.today() + timedelta(days=make_date(day_offset))
    response = requests.get(api_url, headers={"apiKey": api_key})

    if response.status_code != 200:
        return day, [], []
    
    return day, response.json()['data'], []


def make_date(day_offset: str):
    try:
        return float(day_offset)
    except ValueError:
        return 0.0


def no_items():
    print(
        alfred.render([
            alfred.Item(
                title="🔴 No Items...", 
                subtitle='', 
                arg=''
            )
        ])
    )


def food_item(food):
    title = food["GastDesc_de"]
    price = food["ProductPrice"].replace(".", ",") + ' €'
    menu = food["MenuName"]
    return alfred.Item(
        title=f'{title}',
        subtitle=f'{price} · {menu}',
        arg=''
    )


def papa(argv):
    day_offset = argv[1] if len(argv) > 1 else ''
    day, data, items = get(day_offset)

    if len(data) == 0:
        no_items()
        return

    for food in data:
        if food['outlet'] == 'papa' \
                and food['date'] == f'{day}' \
                and not food['MenuName'] == 'SALATBAR_' \
                and 'GERNE MIT' not in food['MenuName'] \
                and not food['MenuName'] == 'OBST_' \
                and not food['MenuName'] == 'DESSERTS_' \
                and not food['MenuName'] == 'GEMUESETELLER_':
            items.append(food_item(food))

    check_and_print(items)


def canteen(argv):
    day_offset = argv[1] if len(argv) > 1 else ''
    day, data, items = get(day_offset)

    if len(data) == 0:
        no_items()
        return

    for food in data:
        if food['outlet'] == 'canteen' \
                and food['date'] == f'{day}':
            items.append(food_item(food))

    check_and_print(items)

def check_and_print(items):
    if len(items) == 0:
        no_items()
    else:
        print(alfred.render(items))


if __name__ == '__main__':
    canteen()
