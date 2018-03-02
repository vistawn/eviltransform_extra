import eviltransform
from rtree import index

class Eviltransform_extra(object):
    
    __gcps = {}
    p = index.Property()
    p.dimension = 2
    idx2d = index.Index(properties=p)

    def __init__(self):
        self.__init_gcp()


    def __init_gcp(self):
        
        with open('gcps_gd','r') as f:
            lines = f.readlines()
            id = 0
            for line in lines:
                values = map(float, line.split(','))
                x, y = values[0:2]
                delta_x, delta_y = values[3:5]
                gcp = {
                    'x': x,
                    'y': y,
                    'delta_x': delta_x,
                    'delta_y': delta_y
                }
                
                self.__gcps[id] = gcp
                self.idx2d.add(id,(x, y))
                id += 1

    def __find_delta(self,lat,lng):
        index = list(self.idx2d.nearest((110, 45)))[0]
        p = self.__gcps[index]
        return p['delta_y'], p['delta_x']

    def transform(self,lat,lng):
        to_y, to_x = eviltransform.transform(lat, lng)
        delta_y,delta_x = self.__find_delta(lat,lng)
        return to_y + delta_y, to_x + delta_x
