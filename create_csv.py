import json

import pandas as pd
import numpy as np
from sqlalchemy.orm import sessionmaker
import mapping_chinagoods as mc


with sessionmaker(bind=mc.engine)() as session:
    with open("products_ids_copy.json", "r", encoding="utf-8") as file:
        dict_with_categories = json.load(file)

    rows_for_csv = []
    for category in list(dict_with_categories):
        category_row = list([category] + [None] * 28)
        category_row[11] = 1
        rows_for_csv.append(category_row)
        for idx, sub_category in enumerate(list(dict_with_categories[category])):
            sub_category_row = list(["!" + sub_category] + [None] * 28)
            sub_category_row[11] = 1
            rows_for_csv.append(sub_category_row)

            current_products = session.query(mc.Product).filter(mc.Product.category == category).filter(
                mc.Product.sub_category == sub_category)
            count_products = len(current_products.all())
            for current_product_object in current_products[:5]:
                photo_objects = session.query(mc.Photo).filter(mc.Photo.product == current_product_object.id).all()
                photos_links = []
                for photo_object in photo_objects:
                    photos_links.append(photo_object.photo)
                photos_links = photos_links[:5] if len(photos_links) > 5 else photos_links
                product_row = [
                    current_product_object.name,  # "Наименование",
                    "id",  # "Наименование Артикула",
                    current_product_object.id,  # артикул,
                    current_product_object.price.split(" ")[-1] if current_product_object.price else None,  # "Валюта",
                    current_product_object.price.split(" ")[0] if current_product_object.price else None,  # "Цена",
                    1,  # доступен для заказа
                    99,  # "В наличии @Москва",
                    99,  # "В наличии @Питер",
                    current_product_object.sort if current_product_object.sort else None,  # "Вид товара",
                    "<{" + current_product_object.patterns + "}>" if current_product_object.patterns else None,  # "Разновидности"
                    f"""{'Страна производитель: ' + current_product_object.place_of_origin if current_product_object.place_of_origin else ''}
                    {'Материал: ' + current_product_object.material if current_product_object.material else ''}
                    {'Количество в оставке: ' + current_product_object.packing_qty if current_product_object.packing_qty else ''}
                    {'Габариты: ' + current_product_object.meas if current_product_object.meas else ''}
                    {'Объем: ' + current_product_object.cbm if current_product_object.cbm else ''}
                    {'вес Брутто: ' + current_product_object.gw if current_product_object.gw else ''}
                    {'вес Нетто: ' + current_product_object.nw if current_product_object.nw else ''}.\n{current_product_object.description if current_product_object.description and "<" not in current_product_object.description else ""}""",  # "Описание",
                    1,  # "Статус",
                    current_product_object.sub_category,  # "Тип товаров",
                    "<{" + current_product_object.colours.replace(" ", '') + "}>" if current_product_object.colours else None,  # "Цвет",
                    photos_links[0] if photos_links else None,  # "Изображения",
                    photos_links[1] if photos_links and len(photos_links) >= 2 else None,  # "Изображения.1",
                    photos_links[2] if photos_links and len(photos_links) >= 3 else None,  # "Изображения.2",
                    photos_links[3] if photos_links and len(photos_links) >= 4 else None,  # "Изображения.3",
                    photos_links[4] if photos_links and len(photos_links) >= 5 else None,  # "Изображения.4",]
                ]
                rows_for_csv.append(product_row)
            print(len(product_row), " !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            if product_row:
                for idx, i in enumerate(product_row):
                    print(f"||||idx {idx + 1}|||| {i}")
                    print("_________________________________________________________________")
            columns_for_df = ["Наименование",
                              "Наименование артикула",
                              "Артикул",
                              "Валюта",
                              "Цена",
                              "Доступен для заказа",
                              "В наличии @Москва",
                              "В наличии @Питер",
                              "Вид товара",
                              "Разновидности",
                              "Описание",
                              "Статус",
                              "Тип товаров",
                              "Цвет",
                              "Изображения",
                              "Изображения.1",
                              "Изображения.2",
                              "Изображения.3",
                              "Изображения.4",
                              "Изображения.5",
                              "Изображения.6",
                              "Изображения.7",
                              "Изображения.8",
                              "Изображения.9",
                              "Изображения.10",
                              "Изображения.11",
                              "Изображения.12",
                              "Изображения.13",
                              "Изображения.14",
                              ]

            df = pd.DataFrame(data=rows_for_csv, columns=columns_for_df)
            df = df.drop_duplicates(subset=["Наименование"])

            df.to_csv(f"DATA_{idx}.csv", encoding="utf-8", index=False)
            print(df)

