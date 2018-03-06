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
        with open('gcps_gd', 'r') as f:
            lines = f.readlines()
            id = 0
            for line in lines:
                values = map(float, line.split(','))
                x, y = values[0:2]
                delta_x, delta_y = values[4:6]
                gcp = {
                    'x': x,
                    'y': y,
                    'delta_x': delta_x,
                    'delta_y': delta_y
                }

                self.__gcps[id] = gcp
                self.idx2d.add(id, (x, y))
                id += 1

    def __find_delta(self, lat, lng):
        index = list(self.idx2d.nearest((110, 45)))[0]
        p = self.__gcps[index]
        return p['delta_y'], p['delta_x']

    def wgs_to_gcj(self, lat, lng):
        """ wgs84 to gcj02

        Arguments:
            lat {float} -- latitude in WGS84
            lng {float} -- longitude in WGS84

        Returns:
            {(float,float)} -- (lat,lng) in GCJ02
        """

        to_y, to_x = eviltransform.transform(lat, lng)
        delta_y, delta_x = self.__find_delta(lat, lng)
        return to_y + delta_y, to_x + delta_x

    def gcj_to_wgs(self, lat, lng, threshold=0.000001):
        """gcj02 to wgs84
        
        Arguments:
            lat {float} -- latitude in gcj02
            lng {float} -- longitude in gcj02
        
        Keyword Arguments:
            threshold {float} -- threshold in decimal degredd (default: {0.000001})
        
        Returns:
            [(float,float)] -- [(lat,lng) in wgs84]
        """

        if eviltransform.outOfChina(lat, lng):
            return lat, lng
        delta = 0.01
        d_lat = d_lng = delta
        min_lat = lat - d_lat
        min_lng = lng - d_lng
        max_lat = lat + d_lat
        max_lng = lng + d_lng
        
        w_lat = lat
        w_lng = lng
        while abs(d_lat) > threshold and abs(d_lng) > threshold:
            w_lat = (min_lat + max_lat) / 2
            w_lng = (min_lng + max_lng) / 2
            tmp_lat, tmp_lng = self.wgs_to_gcj(w_lat, w_lng)
            d_lat = tmp_lat - lat
            d_lng = tmp_lng - lng
            if abs(d_lat) < threshold and abs(d_lng) < threshold:
                return w_lat, w_lng
            if d_lat > 0:
                max_lat = w_lat
            else:
                min_lat = w_lat
            if d_lng > 0:
                max_lng = w_lng
            else:
                min_lng = w_lng
        
        return w_lat, w_lng
