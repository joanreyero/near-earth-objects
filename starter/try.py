from database import NEODatabase as NEO

db = NEO('data/neo_data.csv')
db.load_data()
print(db.db['(2020 AE1)'].print_orbits())
