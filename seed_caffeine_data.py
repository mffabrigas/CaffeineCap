import csv
# from app_models import Caffeine_Drink

def caffeine_dataset(drink_name):
    with open('caffeine.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                pass
            else:
                if row[0] == drink_name:
                    caffeine_per_serving = row[2]
                    return caffeine_per_serving
                    # caffeine_drink = Caffeine_Drink(drink_name=row[0],
                    #                                 serving_size=float(row[1]),
                    #                                 caffeine_per_serving=float(row[2]),
                    #                                 caffeine_density=float(row[3])
                    #                                 ).put()
            line_count = line_count + 1

    # print(f'Processed {line_count-1} lines.')
    # caffeine_drinks = Caffeine_Drink.query().fetch()
    # for caffeine_drink in caffeine_drinks:
    #     print(caffeine_drink)
