# eviltransform_extra

GCJ02 and wgs84 transform

increase the accuracy by control points


## Generate Control Points
Default gcp file's grid interval is 1 degree. If you want generate new gcp file,please run:

```shell
python generate_gcp.py
```

## Transform WGS84 to GCJ02

```python
from pygcj import GCJProj 
trans = GCJProj()
# wgs84 to gcj
gcj_lat, gcj_lon = trans.wgs_to_gcj(45.2,112.8)

# gcj to wgs84
wgs_lat, wgs_lon = trans.gcj_to_wgs(45.2,112.8)
```