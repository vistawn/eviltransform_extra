from rtree import index

points = {}

p = index.Property()
p.dimension = 2
idx2d = index.Index(properties=p)

with open('gcps_gd', 'r') as f:
    lines = f.readlines()
    id = 0
    for line in lines:
        values = line.split(',')
        gcp = {}
        x = float(values[0])
        y = float(values[1])
        gcp['x'] = x
        gcp['y'] = y
        gcp['delta_x'] = float(values[4])
        gcp['delta_y'] = float(values[5])
        points[id] = gcp

        idx2d.add(id, (x,y))
        id+=1


nearest = idx2d.nearest((110,45))

dir(nearest)

