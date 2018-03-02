# eviltransform_extra

WGS to GCJ02

increase the accuracy by control points


## Generate Control Points
Default gcp file's grid interval is 1 degree. If you want generate new gcp file,please run:

```shell
python generate_gcp.py
```

## Transform WGS84 to GCJ02

```python
import eviltransform_extra
trans = eviltransform_extra.Eviltransform_extra()
gcj_x,gcj_y = trans.transform(45.2,112.8)
```