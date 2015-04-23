import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

xs, ys, ts = [], [], []
for line in open('log.txt'):
    try:
        lon, lat, t = map(float, line.strip().split())
        xs.append(lat)
        ys.append(lon)
        ts.append(t)
    except:
        print 'could not parse', line
        continue

print len(ts)

c_norm = colors.Normalize(vmin=0.0, vmax=0.3)
scalar_map = cmx.ScalarMappable(norm=c_norm, cmap=plt.get_cmap('jet'))

colors = [scalar_map.to_rgba(t) for t in ts]

plt.scatter(xs, ys, c=colors, marker='x')
plt.savefig('world.png')
