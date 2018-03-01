import eviltransform

class eviltransform_extra(object):
    
    __gcps = []
    def __init__(self):
        self.__init_gcp()


    def __init_gcp(self):
        with open('gcps_gd','r') as f:
            lines = f.readlines()
            for line in lines:
                values = line.split(',')
                gcp = {}
                gcp['x'] = float(values[0])
                gcp['y'] = float(values[1])
                gcp['delta_x'] = float(values[4])
                gcp['delta_y'] = float(values[5])
                self.__gcps.append(gcp)

    def __find_delta(self,lat,lng):
        delta_x = float('inf')
        delta_y = float('inf')
        distance_p = float('inf')
        for gcp in self.__gcps:
            distance = (lat - gcp['y'])**2 + (lng - gcp['x'])**2
            if distance < distance_p:
                distance_p = distance
                delta_x = gcp['delta_x']
                delta_y = gcp['delta_y']
        
        return delta_y, delta_x

    def transform(self,lat,lng):
        to_y, to_x = eviltransform.transform(lat, lng)
        delta_y,delta_x = self.__find_delta(lat,lng)
        return to_y + delta_y, to_x + delta_x
