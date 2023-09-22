import asyncio
import random
import re
import winsound
import time
import json
from collections import namedtuple

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml

import aiohttp
import aiohttp_proxy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mapping_chinagoods as mc

def download_photo(link: str) -> bytes:
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
    image_response = requests.get(link, headers=headers, stream=True).content

    return image_response


def parse_data(str_html: str,) -> namedtuple:
    ProductInformation = namedtuple(typename="ProductInformation",
                                    field_names=["name", "price", "sort",
                                                 "descrition", "patterns",
                                                 "colours", "material", "meas",
                                                 "g_w", "place_of_origin",
                                                 "packing_qty", "cbm",
                                                 "n_w", "photos"])
    soup = BeautifulSoup(str_html, "lxml")
    try:
        name = soup.find("head", ).find("title").text.replace("en.chinagoods-", "").strip().replace("\\", "").replace("\xa0", "").replace("\n", '').replace("  ", ' ').replace("  ", ' ')
    except: name = None

    try:
        price = (str_html.split('"price":')[1].split(",")[0] + str_html.split('"currency":')[1].split(",")[0]).replace('"', " ").strip().replace("\\", "").replace("\xa0", "")
    except: price = None

    try:
        patterns_list = []
        script_text = list(filter((lambda x: x.text.replace("\n", "").replace(" ", "").startswith("window.__INITIAL_STATE__")), [scrpt_element for scrpt_element in soup.find_all("script")]))[0].text.replace("\\", '').replace("\n", '').replace("#", '').replace("false", "False").replace("true", "True").replace("window.__INITIAL_STATE__=", "").strip()[:-1]
        pattern_text = script_text.split('"attrName":"pattern"')[-1].split('"attrName":')[0]
        pattern = r'"attrValueName":"(.*?)"'
        pattern_value = re.findall(pattern, pattern_text)
        for value in pattern_value:
            patterns_list.append(value)
        patterns = patterns_list
    except: patterns = None

    try:
        colours_list = []
        script_text = list(
            filter((lambda x: x.text.replace("\n", "").replace(" ", "").startswith("window.__INITIAL_STATE__")),
                   [scrpt_element for scrpt_element in soup.find_all("script")]))[0].text.replace("\\", '').replace(
            "\n", '').replace("#", '').replace("false", "False").replace("true", "True").replace(
            "window.__INITIAL_STATE__=", "").strip()[:-1]
        colour_text = script_text.split('"attrName":"colour"')[-1].split('"attrName":')[0]
        pattern = r'"attrValueName":"(.*?)"'
        colour_value = re.findall(pattern, colour_text)
        for value in colour_value:
            colours_list.append(value)
        colours = colours_list
    except: colours = None

    try:
        description = " ".join([descr.text for descr in soup.find("div", {"class": "descriptions"}).find("div").find_all("p")]).replace("   ", " ").replace("  ", ' ').replace("  ", ' ').replace("\n", "").strip().replace("\\", "").replace("\xa0", "")
    except: description = None

    try:
        parameters_list_elements = soup.find("ul", {"class": "parameters_list"}).find_all("li")
    except: parameters_list_elements = None
    Sort = None
    Material = None
    MEAS = None
    G_W = None
    Place_of_origin = None
    Packing_qty = None
    CBM = None
    N_W = None
    if parameters_list_elements:
        try:
            Sort = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Sort:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Sort = None
        try:
            Material = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Material:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Material = None
        try:
            MEAS = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "MEAS.:" else None for parameter in parameters_list_elements]))[0].replace("\n", '').replace("   ", '').strip().replace("\\", "").replace("\xa0", "")
        except: MEAS = None
        try:
            G_W = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "G.W.:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: G_W = None
        try:
            Place_of_origin = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Place of Origin:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Place_of_origin = None
        try:
            Packing_qty = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Packing QTY:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Packing_qty = None
        try:
            CBM = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "CBM:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: CBM = None
        try:
            N_W = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "N.W.:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: N_W = None

    # photos_bytes_list = []
    photos_links = []
    try:
        photo_elements = soup.find("div", {"class": "picture"}).find_all("img")
    except: photo_elements = None
    if photo_elements:
        for photo_element in photo_elements:
            if photo_element.get("src"):
                try:
                    photos_links.append(photo_element.get("src"))
                    # photo_bytes = download_photo(photo_element.get("src"))
                    # photos_bytes_list.append(photo_bytes)
                except Exception as ex:
                    print(f"photo ---> {ex}")
    # print(f"!!!|name - {name}|\n price - {price}|\n description - {description}|\n patterns - {patterns}|\n colours - {colours}|\n sort - {Sort}|\n material - {Material}| meas - {MEAS}|\n G.W. - {G_W}|\n place of origin - {Place_of_origin}|\n packing_qty - {Packing_qty}|\n cbm - {CBM}|!!!")
    return ProductInformation(name=name, price=price,
                              descrition=description, patterns=patterns,
                              colours=colours, sort=Sort,
                              material=Material, meas=MEAS, g_w=G_W,
                              place_of_origin=Place_of_origin,
                              packing_qty=Packing_qty, cbm=CBM,
                              n_w=N_W, photos=photos_links)

def save_data(category: str, sub_category: str, product_id: str, product_information: namedtuple, idx: int,):
    engine = create_engine("sqlite:///chinagoods.db")
    with sessionmaker(bind=engine)() as session:
        product_object = mc.Product(
            site_id=str(product_id),
            category=category,
            sub_category=sub_category,
            name=product_information.name,
            price=product_information.price,
            description=product_information.descrition.replace("u002", '/') if product_information.descrition and \
                                                          "style =" not in product_information.patterns and \
                                                          "< strong >" not in product_information.patterns and \
                                                          "< span" not in product_information.patterns and \
                                                          "< br" not in product_information.patterns else None,
            patterns=", ".join(
                product_information.patterns) if product_information.patterns and \
                                                 "style =" not in product_information.patterns and \
                                                 "< strong >" not in product_information.patterns and \
                                                 "< span" not in product_information.patterns and \
                                                 "< br" not in product_information.patterns else None,
            colours=", ".join(
                product_information.colours).replace("u002", '/') if product_information.colours else None,
            sort=product_information.sort,
            place_of_origin=product_information.place_of_origin,
            material=product_information.material,
            packing_qty=product_information.packing_qty,
            meas=product_information.meas,
            cbm=product_information.cbm,
            gw=product_information.g_w,
            nw=product_information.n_w,
        )
        session.add(product_object)
        session.commit()
        for photo_bytes in product_information.photos:
            photo_object = mc.Photo(photo=photo_bytes,
                                    product=product_object.id)
            session.add(photo_object)
            session.commit()
        iter_time = time.time()
        print(
            f"<<<|||product #{idx + 1}||| id=>{product_id}.>>>")
async def fetch_product(session, product_id, url, headers):
    try:
        response = await session.get(url=url, headers=headers)
        product_information = parse_data(await response.text(encoding="utf-8"))
        return product_information
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")
        return None
async def get_product_information(headers: dict, idx_start_categoty: int, idx_end_category: int, proxy: aiohttp_proxy.ProxyConnector|None, unicue_products: list[str], process_num: int) -> None:
    with open("products_ids.json", 'r', encoding="utf-8") as file:
        categories_with_products_dict = json.load(file)

    async with aiohttp.ClientSession(connector=proxy) if proxy else aiohttp.ClientSession() as session:
        for idx_category, category in enumerate(
                list(categories_with_products_dict)[idx_start_categoty:idx_end_category]):
            for idx_sub_category, sub_category in enumerate(list(categories_with_products_dict[category])):
                print(sub_category)
                list_product_ids = categories_with_products_dict[category][sub_category]
                start_time = time.time()
                for idx, product_id in enumerate(list_product_ids):
                    try:
                        if product_id not in unicue_products:
                            unicue_products.append(product_id)
                            print(f"{product_id} ---> P ---> №{process_num}")
                            await asyncio.sleep(random.uniform(0.5, 1))
                            url = f"https://en.chinagoods.com/product/{product_id}"
                            product_information = await fetch_product(session, product_id, url, headers)
                            if product_information:
                                save_data(category, sub_category, product_id, product_information, idx)
    # exceptions = []
    # with open("products_ids.json", 'r', encoding="utf-8") as file:
    #     categories_with_products_dict = json.load(file)
    #
    # for idx_category, category in enumerate(list(categories_with_products_dict)[idx_start_categoty:idx_end_category]):
    #     for idx_sub_category, sub_category in enumerate(list(categories_with_products_dict[category])):
    #         print(sub_category)
    #         list_product_ids = categories_with_products_dict[category][sub_category]
    #         start_time = time.time()
    #         for idx, product_id in enumerate(list_product_ids):
    #
    #             if product_id not in unicue_products:
    #                 unicue_products.append(product_id)
    #                 print(f"{product_id} ---> P ---> №{process_num}")
    #                 # try:
    #                 time.sleep(random.uniform(0.1, 0.5))
    #                 if proxy:
    #                     async with aiohttp.ClientSession(connector=proxy) as session:
    #                         async with session.get(url=f"https://en.chinagoods.com/product/{product_id}", headers=headers) as response:
    #                             product_information = parse_data(await response.text(encoding="utf-8"))
    #                             save_data(category, sub_category, product_id, product_information, idx,)
    #                             await session.close()
    #                 else:
    #                     async with aiohttp.ClientSession() as session:
    #                         response = await session.get(url=f"https://en.chinagoods.com/product/{product_id}", headers=headers)
    #                         product_information = parse_data(await response.text(encoding="utf-8"))
    #                         save_data(category, sub_category, product_id, product_information, idx, )

                    except Exception as ex:
                        print(f"{ex} ||| {idx_category}->{category} ||| {idx_sub_category}->{sub_category} ||| {product_id}")
                        continue
        #
        # return exceptions


async def main():
    list_proxy = [
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@45.128.130.134:7002"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.199.81:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.241.247:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.227.194:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.241.241:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.199.197:9858"),
                  ]
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

    unicue_products = []
    try:
        task_0 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=0, idx_end_category=3, proxy=None,
                                    unicue_products=unicue_products, process_num=1))
        task_1 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=3, idx_end_category=6,
                                    proxy=list_proxy[0], unicue_products=unicue_products, process_num=2))
        task_2 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=6, idx_end_category=9,
                                    proxy=list_proxy[1], unicue_products=unicue_products, process_num=3))
        task_3 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=9, idx_end_category=12,
                                    proxy=list_proxy[2], unicue_products=unicue_products, process_num=4))
        task_4 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=12, idx_end_category=15,
                                    proxy=list_proxy[3], unicue_products=unicue_products, process_num=5))
        task_5 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=15, idx_end_category=18,
                                    proxy=list_proxy[4], unicue_products=unicue_products, process_num=6))
        task_6 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=18, idx_end_category=-1,
                                    proxy=list_proxy[5], unicue_products=unicue_products, process_num=7))
        tasks = [task_0, task_1, task_2, task_3, task_4, task_5, task_6]

        await asyncio.gather(*tasks)

    except Exception as ex:
        print(ex)
        winsound.Beep(500, 10000)


if __name__ == '__main__':
    asyncio.run(main())
