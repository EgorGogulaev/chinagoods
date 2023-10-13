

from sqlalchemy.orm import sessionmaker

import mapping_chinagoods as mc

if __name__ == '__main__':
    with sessionmaker(bind=mc.engine)() as session:

        product_objects = session.query(mc.Product).all()

        tokens_str = ""

        for idx, product_object in enumerate(product_objects):
            print(f"iter num -> {idx + 1}")
            name = product_object.name if product_object.name else None
            if name:
                tokens_str += f" {name}"
            description = product_object.description if product_object.description else None
            if description:
                tokens_str += f" {description}"

        tokens = tokens_str.split()

        print(f"Количество: {len(tokens)}")
        print(f"Цена $: {len(tokens) / 100 * 0.0035}")
        print(f"Цена Р: {len(tokens) / 100 * 0.0035 * 99}")

