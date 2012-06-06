import urllib
import sys
import Image
import string
import numpy
from PIL import Image

def readParams( filename ):
    res = {}
    try:
        f = open(filename)
        for line in f:
            if string.strip(line)[0] == '#':
                continue
            params = string.split(line)
            res[params[0]] = params[1:]
        return res
    except:
        print 'Error: file <' + filename + '> does not exist or contamenated'
        sys.exit(1)

def buildParams( params_dict ):
    """
    builds url params? specific to Google Maps APIv2 into a single string
    """
    res = []
    for param_name, param_values in params_dict.iteritems():
        if param_name == 'size':
            res.append('size='+string.join([str(x) for x in param_values], 'x'))
        elif param_name == 'center':
            res.append('center='+string.join([str(x) for x in param_values], ','))
        else:
            res.append(param_name+'='+str(param_values[0]))
    return string.join(res, '&')

def ifRange( start, stop, num ):
    res = []
    if start > stop:
        res = numpy.linspace(start, stop, num)
    else:
        res = numpy.linspace(stop, start, num)
    return res

def buildCoordRange( start, stop, num ):
    return zip(ifRange(start[0], stop[0], num), ifRange(start[1], stop[1], num))

def getMapImage( params, out_file = 'out' ):
    """
    gets .png image from google maps
    """
    url = 'http://maps.googleapis.com/maps/api/staticmap?'
    print 'Downloading:', url + params, 'loaction'
    urllib.urlretrieve(url+params, out_file)

def main():
    args = sys.argv[1:]
    #getMapImage( [40.714728, -73.998672], 14, [400, 400] )
    params = {}
    out_file = ''
    coord_range = {}
    if len(args) and args[0] == '--conf' or args[0] == '-c':
        params = readParams(args[1])
        args = args[2:]
    if len(args) and args[0] == '--position' or args[0] == '-p':
        params.update( {'center': [float(x) for x in args[1:3]]} )
        args = args[3:]
    if len(args) and args[0] == '--range' or args[0] == '-r':
        coord_range['range'] = [float(x) for x in args[1:3]]
        args = args[3:]
    if len(args) and args[0] == '--number_of_pics' or args[0] == '-n':
        coord_range['num'] = int(args[1])
        args = args[2:]
    #if len(args) and args[0] == '--out' or args[0] == '-o':
    #   out_file = args[1]
    #   args = args[2:]
    
    coords = buildCoordRange(params['center'], coord_range['range'], coord_range['num'])
    for coord in coords:
        params['center'] = list(coord)
        str_param = buildParams(params)
        out_file_name = '_'.join([str(x) for x in coord]) + '.png'
        getMapImage(str_param, out_file_name)

if __name__ == '__main__':
    main()
