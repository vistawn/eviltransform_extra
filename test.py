from __future__ import print_function
import random, time, requests
import math, numpy
import eviltransform
import eviltransform_extra
import distance_calculator
import config


min_x = config.test_extent['min_lng'] + 0.0
min_y = config.test_extent['min_lat'] + 0.0
max_x = config.test_extent['max_lng'] + 0.0
max_y = config.test_extent['max_lat'] + 0.0
interval_x = max_x - min_x
interval_y = max_y - min_y

def performance_test(points_count):

    print('start transform -- ' + time.ctime())
    print('init -- ' + time.ctime())
    start = time.time()
    trans = eviltransform_extra.Eviltransform_extra()
    stop = time.time()
    print('init finish. -- ' + time.ctime())
    print('init seconds: ' + str(stop - start))
    start = time.time()
    for x in xrange(0,points_count):
        trans.transform(min_y + interval_y * random.random(), min_x + interval_x * random.random())
    
    stop = time.time()
    print('finish. -- ' + time.ctime())
    print('transform seconds: ' + str(stop - start))

def querygaode(lat,lng):
    reqdata = {
        'locations': str(lng) + ',' + str(lat),
        'coordsys': 'gps',
        'output': 'json',
        'key': config.gaode_key
    }

    r = requests.get(
        'http://restapi.amap.com/v3/assistant/coordinate/convert', params=reqdata)


    r_json = r.json()
    gd_str = r_json['locations']
    gd_coords = gd_str.split(',')
    return float(gd_coords[1]), float(gd_coords[0])


def test_gaode(sample_count):
    interval_x = max_x - min_x
    interval_y = max_y - min_y

    ex_trans = eviltransform_extra.Eviltransform_extra()

    dis_loc = []
    dis_ex = []
    for x in xrange(0,sample_count):
        q_x = round(min_x + interval_x * random.random(),6)
        q_y = round(min_y + interval_y * random.random(),6)
        loc_y,loc_x = eviltransform.transform(q_y, q_x)
        ex_y, ex_x = ex_trans.transform(q_y,q_x)
        gaode_y, gaode_x = querygaode(q_y, q_x)

        loc_distance = distance_calculator.calculate_distance(gaode_y,gaode_x,loc_y,loc_x)
        ex_distance = distance_calculator.calculate_distance(gaode_y, gaode_x, ex_y, ex_x)

        dis_loc.append(loc_distance)
        dis_ex.append(ex_distance)
        print(loc_distance, ex_distance)

        time.sleep(0.1)
    

    print('avg_loc: ' + str(numpy.average(dis_loc)) +
          ' std_loc:' + str(numpy.std(dis_loc)) +
          ' avg_ex:' + str(numpy.average(dis_ex)) +
          ', std_ex:' + str(numpy.std(dis_ex)))


#test_gaode(30)

#performance_test(50000)


if __name__ == "__main__":
    import profile
    profile.run("performance_test(5000)")
