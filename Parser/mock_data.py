import random


# функция генерации мок-данных
def fetch_yacht_data(yacht_type, budget):
    yacht_types = ['Моторная яхта', 'Парусная яхта', 'Катамаран', 'Рыболовное судно', 'Люксовая яхта']
    locations = ['Средиземное море', 'Карибы', 'Тихий океан']

    yacht_data = []
    for _ in range(5):
        price = random.randint(1, budget)
        yacht = {'type': random.choice(yacht_types),
                 'price': price,
                 'location': random.choice(locations),
                 'url':'https://example.com/yacht'
                 }
        yacht_data.append(yacht)
    return yacht_data