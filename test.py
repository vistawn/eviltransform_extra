from __future__ import print_function
import random
import time
import requests
from pygcj.pygcj import GCJProj
from pygcj.pygcj import great_circle_distance
from pygcj import config

import sys
if sys.version_info >= (3, 0):
    xrange = range

min_lng = config.test_extent['min_lng'] + 0.0
min_lat = config.test_extent['min_lat'] + 0.0
max_lng = config.test_extent['max_lng'] + 0.0
max_lat = config.test_extent['max_lat'] + 0.0
interval_lng = max_lng - min_lng
interval_lat = max_lat - min_lat

def performance_test(points_count):

    print('start transform -- ' + time.ctime())
    print('init -- ' + time.ctime())
    start = time.time()
    trans = GCJProj()
    stop = time.time()
    print('init finish. -- ' + time.ctime())
    print('init seconds: ' + str(stop - start))
    start = time.time()
    for x in xrange(0,points_count):
        trans.wgs_to_gcj(min_lat + interval_lat * random.random(), min_lng + interval_lng * random.random())
    
    stop = time.time()
    print('finish. -- ' + time.ctime())
    print('transform seconds: ' + str(stop - start))


def querygaode(wgs_points, amapkey):
    locstr = ''
    for point in wgs_points:
        locstr += str(point[1]) + ',' + str(point[0]) + '|'
    
    reqdata = {
        'locations': locstr,
        'coordsys': 'gps',
        'output': 'json',
        'key': amapkey
    }

    r = requests.get(
        'http://restapi.amap.com/v3/assistant/coordinate/convert', params=reqdata)


    r_json = r.json()
    gd_str = r_json['locations']
    gd_coords = gd_str.split(';')
    result = []
    for gd_coord in gd_coords:
        lnglat = gd_coord.split(',')
        result.append((float(lnglat[1]), float(lnglat[0])))
    return result


def statistic(arry):
    l = len(arry)
    s = sum(arry)
    m = s/l
    d = 0
    for i in arry:
        d += (i - m)**2
    stdev = (d/(l-1)) ** 0.5
    return (m,stdev)

def test_gaode(amapkey):

    trans = GCJProj()

    wgs_points = []
    raw_points = []
    rectify_points = []

    for x in xrange(0,40):
        lng = round(min_lng + interval_lng * random.random(),6)
        lat = round(min_lat + interval_lat * random.random(),6)
        wgs_points.append((lat,lng))
        raw_points.append(trans.wgs_to_gcj_raw(lat, lng))
        rectify_points.append(trans.wgs_to_gcj(lat, lng))
    
    gd_points = querygaode(wgs_points,amapkey)

    diff_ori = []
    diff_raw = []
    diff_rectify = []
    
    for x in xrange(0,40):
        d_ori = great_circle_distance(wgs_points[x][0],wgs_points[x][1],gd_points[x][0],gd_points[x][1])
        diff_ori.append(d_ori)
        d_raw = great_circle_distance(
            raw_points[x][0], raw_points[x][1], gd_points[x][0], gd_points[x][1])
        diff_raw.append(d_raw)
        d_rectify = great_circle_distance(
            rectify_points[x][0], rectify_points[x][1], gd_points[x][0], gd_points[x][1])
        diff_rectify.append(d_rectify)

    print('wgs<->gcj distance mean: ' + str(statistic(diff_ori)[0]) + '\r\n' +
          'wgs<->gcj distance stdev: ' + str(statistic(diff_ori)[1]) + '\r\n' +
          'raw<->gcj distance mean: ' + str(statistic(diff_raw)[0]) + '\r\n' +
          'raw<->gcj distance stdev: ' + str(statistic(diff_raw)[1]) + '\r\n' +
          'rectify<->gcj distance mean: ' + str(statistic(diff_rectify)[0]) + '\r\n' +
          'rectify<->gcj distance stdev: ' + str(statistic(diff_rectify)[1]))



def test_transform():
    ex_trans = GCJProj()

    for x in xrange(0,10):
        t_x = 100 + x * random.random()
        t_y = 35 + x * random.random()
        wgs_y, wgs_x = (t_y, t_x)
        y1, x1 = ex_trans.wgs_to_gcj(wgs_y, wgs_x)
        y, x = ex_trans.gcj_to_wgs(y1, x1, 1e-8)

        print('wgs:({},{}) to_gcj:({},{}) back_to_wgs:({},{})'.format(wgs_y,wgs_x,y1,x1,y,x))


#test_gaode('your amap key')

performance_test(50000)

# if __name__ == "__main__":
#     import profile
#     profile.run("performance_test(5000)")
#     test_transform()
