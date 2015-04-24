import math
import numpy as np
from annoy import AnnoyIndex
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from mpl_toolkits import basemap

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
    if len(ts) == 1000:
        break

print 'building index...'
ai.build(5)

print 'building up data points'
lons = np.arange(-180, 180, 3.0)
lats = np.arange(-90, 90, 3.0)
X, Y = np.meshgrid(lons, lats)
Z = np.zeros(X.shape)

for i, _ in np.ndenumerate(Z):
    lon, lat = X[i], Y[i]

    v = ll_to_3d(lat, lon)

    js = ai.get_nns_by_vector(v, 200)[:100]
    all_ts = [ts[j] for j in js]
    cutoff = np.percentile(all_ts, 90)
    p = np.mean([t for t in all_ts if t < cutoff])
    Z[i] = p

print 'plotting'
map = basemap.Basemap(projection='ortho',lat_0=45,lon_0=-100,resolution='l')
# draw coastlines, country boundaries, fill continents.
map.drawcoastlines(linewidth=0.25)
map.drawcountries(linewidth=0.25)
# map.fillcontinents(color='coral',lake_color='aqua')
# draw the edge of the map projection region (the projection limb)
# map.drawmapboundary(fill_color='aqua')
# draw lon/lat grid lines every 30 degrees.
map.drawmeridians(np.arange(0,360,30))
map.drawparallels(np.arange(-90,90,30))
# Z = basemap.maskoceans(lon, lat, Z)

# contour data over the map.
cf = map.contourf(X, Y, Z, 20, cmap=plt.get_cmap('jet'), norm=plt.Normalize(vmin=0.0, vmax=0.2), latlon=True)
plt.show()

