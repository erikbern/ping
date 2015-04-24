import math
import numpy as np
from annoy import AnnoyIndex
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits import basemap

vmin, vmax = 0.0, 0.4

def ll_to_3d(lat, lon):
    lat *= math.pi / 180
    lon *= math.pi / 180
    x = math.cos(lat) * math.cos(lon)
    z = math.cos(lat) * math.sin(lon)
    y = math.sin(lat)
    return [x, y, z]

ai = AnnoyIndex(3, 'angular')
xs, ys, ts = [], [], []
for line in open('log.txt'):
    try:
        lat, lon, t = map(float, line.strip().split())
    except:
        print 'could not parse', line
        continue

    p = ll_to_3d(lat, lon)
    ai.add_item(len(ts), p)
    xs.append(lon)
    ys.append(lat)
    ts.append(t)

print 'building index...'
ai.build(10)

print 'building up data points'
lons = np.arange(-180, 181, 0.2)
lats = np.arange(-90, 91, 0.2)
X, Y = np.meshgrid(lons, lats)
Z = np.zeros(X.shape)

count = 0
for i, _ in np.ndenumerate(Z):
    lon, lat = X[i], Y[i]

    v = ll_to_3d(lat, lon)

    js = ai.get_nns_by_vector(v, 200)
    all_ts = [ts[j] for j in js]
    cutoff = np.percentile(all_ts, 90)
    p = np.mean([t for t in all_ts if t < cutoff])
    p = np.clip(p, vmin, vmax)
    Z[i] = p
    count += 1
    if count % 1000 == 0:
        print count, np.prod(Z.shape)

print 'plotting'
map = basemap.Basemap(projection='ortho',lat_0=30,lon_0=-30,resolution='l')

# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)

# draw lon/lat grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))

# remove oceans
Z = basemap.maskoceans(X, Y, Z, resolution='h', grid=1.25)

# contour data over the map.
cf = map.contourf(X, Y, Z, 20, cmap=plt.get_cmap('jet'), norm=plt.Normalize(vmin=vmin, vmax=vmax), latlon=True)
map.colorbar(cf)
# cf = map.contour(X, Y, Z, 20, latlon=True, colors='b')

plt.show()
