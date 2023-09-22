import json

import pandas as pd
from sqlalchemy.orm import sessionmaker

import mapping_chinagoods as mc


def get_csv(sub_category: str):

    with sessionmaker(bind=mc.engine)() as session:
        product_objects = session.query(mc.Product).filter(mc.Product.sub_category == sub_category).all()
        # for


if __name__ == '__main__':
    with open("products_ids.json", "r", encoding="utf-8") as file:
        dict_with_categories = json.load(file)

    for category in list(dict_with_categories):
        for sub_category in list(dict_with_categories[category]):
            get_csv(sub_category=sub_category)