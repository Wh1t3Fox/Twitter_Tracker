###########################################################
## Google map python wrapper V0.1
## Origin: https://code.google.com/p/pygmaps/
## Modified by: Craig West
############################################################

class maps:

    def __init__(self, centerLat, centerLng, zoom ):
        self.center = (float(centerLat),float(centerLng))
        self.zoom = int(zoom)
        self.paths = []
        self.points = []
        self.coloricon = 'http://chart.apis.google.com/chart?cht=mm&chs=12x16&chco=FFFFFF,XXXXXX,000000&ext=.png'

    #Add a point to the list
    def addpoint(self, lat, lng, color = '#FF0000', title = None):
        self.points.append((lat,lng,color[1:],title))
    
    #Add a list of points to the path list
    def addpath(self,path,color = '#FF0000'):
        path.append(color)
        self.paths.append(path)
    
    #Create the file
    def draw(self, htmlfile):
        with open(htmlfile,'w') as f:
            f.write('<html>\n')
            f.write('<head>\n')
            f.write('<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />\n')
            f.write('<meta http-equiv="content-type" content="text/html; charset=UTF-8"/>\n')
            f.write('<title>Google Maps - pygmaps </title>\n')
            f.write('<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>\n')
            f.write('<script type="text/javascript">\n')
            f.write('\tfunction initialize() {\n')
            self.drawmap(f)
            for point in  self.points:
                self.drawpoint(f,point[0],point[1],point[2],point[3])
            for path in self.paths:
                self.drawPolyline(f,path[:-1], strokeColor = path[-1])
            f.write('\t}\n')
            f.write('</script>\n')
            f.write('</head>\n')
            f.write('<body style="margin:0px; padding:0px;" onload="initialize()">\n')
            f.write('\t<div id="map_canvas" style="width: 100%; height: 100%;"></div>\n')
            f.write('</body>\n')
            f.write('</html>\n')        
    
    #Draw the map
    def drawmap(self, f):
        f.write('\t\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
        f.write('\t\tvar myOptions = {\n')
        f.write('\t\t\tzoom: %d,\n' % (self.zoom))
        f.write('\t\t\tcenter: centerlatlng,\n')
        f.write('\t\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
        f.write('\t\t};\n')
        f.write('\t\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
        f.write('\n')
    
    #Add the points to the map
    def drawpoint(self,f,lat,lon,color,title):
        f.write('\t\tvar latlng = new google.maps.LatLng(%f, %f);\n'%(lat,lon))
        f.write('\t\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon.replace('XXXXXX',color)))
        f.write('\t\tvar marker = new google.maps.Marker({\n')
        if title !=None:
            f.write('\t\ttitle: "'+str(title)+'",\n')
        f.write('\t\ticon: img,\n')
        f.write('\t\tposition: latlng\n')
        f.write('\t\t});\n')
        f.write('\t\tmarker.setMap(map);\n')
        f.write('\n')
        
    #Add the line between points
    def drawPolyline(self,f,path,\
            clickable = False, \
            geodesic = True,\
            strokeColor = "#FF0000",\
            strokeOpacity = 1.0,\
            strokeWeight = 2
            ):
        f.write('\t\tvar PolylineCoordinates = [\n')
        for coordinate in path:
            f.write('\t\t\tnew google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
        f.write('\t\t];\n')
        f.write('\n')
        
        f.write('\t\tvar lineSymbol = { \n')
        f.write('\t\t\tpath: google.maps.SymbolPath.FORWARD_CLOSED_ARROW \n')
        f.write('\t\t}; \n')
        f.write('\t\tvar Path = new google.maps.Polyline({\n')
        f.write('\t\t\tclickable: %s,\n' % (str(clickable).lower()))
        f.write('\t\t\tgeodesic: %s,\n' % (str(geodesic).lower()))
        f.write('\t\t\tpath: PolylineCoordinates,\n')
        f.write('\t\t\ticons: [{ \n')
        f.write('\t\t\t\ticon: lineSymbol,\n')
        f.write('\t\t\t\toffset: "100%"\n')
        f.write('\t\t\t}],\n')
        f.write('\t\t\tstrokeColor: "%s",\n' %(strokeColor))
        f.write('\t\t\tstrokeOpacity: %f,\n' % (strokeOpacity))
        f.write('\t\t\tstrokeWeight: %d\n' % (strokeWeight))
        f.write('\t\t});\n')
        f.write('\n')
        f.write('\t\tPath.setMap(map);\n')
        f.write('\n\n')
