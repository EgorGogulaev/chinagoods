import json
import time
import winsound

import requests
from fake_useragent import UserAgent

from categories_links_dict import categories_dict as cd


def get_total_pages(json_data: dict, headers: dict) -> int:
    json_data.update({"page": 1, })
    first_response = requests.post(url='https://apiserver.chinagoods.com/productquery/v1/products/search',
                                   json=json_data, headers=headers)

    if first_response.status_code != 200:
        raise ConnectionError

    total_pages = first_response.json().get('total_page', None)
    if not total_pages:
        raise ValueError

    return total_pages


def get_product_cards_ids(json_data: dict, headers: dict, start_flag: bool=False):
    dict_with_products_ids = {}
    exceptions = []

    try:
        if start_flag:
            start_category = int(input("CAT:"))
            start_sub_category = int(input("SUB_CAT:"))
        else:
            start_category = 0
            start_sub_category = 0

        for idx_category, category in enumerate(list(cd)[start_category:]):
            dict_with_products_ids[category] = {}
            for idx_sub_category, sub_category in enumerate(list(cd[category])[start_sub_category if start_flag else 0:]):
                try:
                    start_flag = False
                    dict_with_products_ids[category][sub_category] = []

                    parent_product_type_id = int(
                        cd[category][sub_category].split("parent_product_type_id")[-1].split('&')[0].replace('=', '')
                    )
                    print(parent_product_type_id)
                    product_type_id = int(
                        cd[category][sub_category].split("product_type_id")[-1].split('&')[0].replace('=', '')
                    )
                    print(product_type_id)

                    json_data['parent_product_type_id'] = parent_product_type_id
                    json_data['product_type_id'] = product_type_id

                    total_pages = get_total_pages(json_data=json_data, headers=headers)


                    for page_num in range(1, total_pages + 1):
                        headers['User-Agent'] = UserAgent().random
                        json_data["page"] = page_num
                        response_page = requests.post(url='https://apiserver.chinagoods.com/productquery/v1/products/search',
                                                      json=json_data, headers=headers)
                        if response_page.status_code != 200:
                            raise ConnectionError(f"{category} - {sub_category} - {page_num}")

                        json_with_ids = response_page.json()

                        for product_information in json_with_ids['data']:
                            dict_with_products_ids[category][sub_category].append(product_information['id'])
                    print(f"{category} #{idx_category} | {sub_category} #{idx_sub_category}")
                except Exception as ex:
                    print(ex)
                    exceptions.append(f"{category} #{idx_category} | {sub_category} #{idx_sub_category}")
                    continue
    except Exception as ex:
        print(ex)
        with open('data_with_exception_0.json', 'w', encoding='utf-8') as outfile:
            json.dump(dict_with_products_ids, outfile)
        winsound.Beep(440, 100000)


    return dict_with_products_ids, exceptions


if __name__ == '__main__':
    headers = {
        'authority': 'apiserver.chinagoods.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en',
        'content-type': 'application/json;chareset=UTF-8',
        'origin': 'https://en.chinagoods.com',
        'referer': 'https://en.chinagoods.com/',
        'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Microsoft Edge";v="116"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': UserAgent().random,
    }

    json_data = {
        "sort": 17,
        "page": 1,
        "page_size": 100,
        "platform": "pc"
    }
    data, exceptions = get_product_cards_ids(json_data=json_data, headers=headers, start_flag=True)
    with open('data_0.json', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile)
    print(exceptions)

    # 7 / 17