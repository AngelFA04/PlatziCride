import csv
from cride.circles.models import Circle

def load_data(filename, db_name):
    with open(f'{filename}.csv', encoding='utf-8') as f:
        file = csv.reader(f)
        headers = dict()
        for n,row in enumerate(file):
            if n == 0:
                headers = row
            else:
                # Create a dict with all the data
                data = dict(zip(headers, row))
                if data['members_limit'] != '0':
                    data['is_limited'] = True
                else:
                    data['is_limited'] = False
                print(data)
                # Create an instance in DB
                circle = db_name.objects.create(**data)
                # Save it
                circle.save()

        print(headers)

if __name__ == "__main__":
    load_data('circles', Circle)
