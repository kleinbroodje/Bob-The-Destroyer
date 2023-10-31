from csv import reader

def import_csv_layout(path):
    with open(path) as map:
        terrain_map = []
        level = reader(map, delimiter=",")
        for row in level:
            terrain_map.append(list(row))
            
    return terrain_map

class Level:
    def __init__(self, csv):
        self.terrain = import_csv_layout(csv)

    def update(self):
        pass

print(import_csv_layout("platform.csv"))