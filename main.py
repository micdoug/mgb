from period import Period
from entity import Entity
from mobile_neighborhood import MobileNeighborhood

if __name__ == '__main__':
    entities = MobileNeighborhood()
    entities.add(1)
    entities.add(2)
    print(entities)
    print(entities[2])
    print(1 in entities)
    print(3 in entities)
    print(Entity(3) in entities)
    print(Entity(1) in entities)
