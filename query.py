import random
import traceback
import subprocess
import time
import os

from multiprocessing.pool import ThreadPool, Pool

FNULL = open(os.devnull, 'w')

def get_random_ip():
    return '.'.join(map(str, [random.randint(0, 255) for i in xrange(4)]))

def ping_ip(ip, lat, lon):
    try:
        print ip, lat, lon, '?'
        t0 = time.time()
        status = subprocess.call(['ping', '-c1', '-t2', ip], stdout=FNULL, stderr=FNULL)
        if status != 0:
            return None
        return ip, lat, lon, time.time() - t0
    except:
        traceback.print_exc()

if __name__ == '__main__':
    pool = ThreadPool(processes=100)
    f = open('log.txt', 'a')

    def cb(result):
        print result
        if result is None:
            return
        ip, lat, lon, t = result
        print >>f, lat, lon, t

    from geoip import geolite2

    for i in xrange(10000):
        ip = get_random_ip()
        match = geolite2.lookup(ip)
        if match is None or match.location is None:
            continue
        lat, lon = match.location
        pool.apply_async(ping_ip, args=(ip, lat, lon), callback=cb)

    pool.close()
    pool.join()

    f.close()
