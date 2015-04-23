import math
import numpy as np
from annoy import AnnoyIndex
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

def ll_to_3d(lat, lon):
    lat *= math.pi / 180
    lon *= math.pi / 180
    x = math.cos(lon) * math.cos(lat)
    z = math.cos(lon) * math.sin(lat)
    y = math.sin(lon)
    return [x, y, z]

ai = AnnoyIndex(3, 'angular')
xs, ys, ts = [], [], []
for line in open('log.txt'):
    try:
        lon, lat, t = map(float, line.strip().split())
    except:
        print 'could not parse', line
        continue

    p = ll_to_3d(lat, lon)
    ai.add_item(len(ts), p)
    xs.append(lat)
    ys.append(lon)
    ts.append(t)

print 'building index...'
ai.build(20)

print 'building up data points'
lats = np.arange(-180, 180, 1.0)
lons = np.arange(-90, 90, 1.0)
X, Y = np.meshgrid(lats, lons)
Z = np.zeros(X.shape)

for i, _ in np.ndenumerate(Z):
    lat, lon = X[i], Y[i]

    v = ll_to_3d(lat, lon)

    js = ai.get_nns_by_vector(v, 100)[:30]
    all_ts = [ts[j] for j in js]
    p = np.median(all_ts)
    Z[i] = p

print 'plotting'
plt.contour(X, Y, Z, 6)

c_norm = colors.Normalize(vmin=0.0, vmax=0.5)
scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=plt.get_cmap('jet'))

colors = [scalar_map.to_rgba(t) for t in ts]

plt.scatter(xs, ys, c=colors, marker='x')
plt.show()

    
