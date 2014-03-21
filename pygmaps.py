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
    def draw(self):
        with open('map.js','w') as f:
            f.write('function initialize() {\n')
            self.drawmap(f)
            for point in  self.points:
                self.drawpoint(f,point[0],point[1],point[2],point[3])
            self.drawPolyline(f, self.paths)
            f.write('}\n')        
    
    #Draw the map
    def drawmap(self, f):
        f.write('\tvar centerlatlng = new google.maps.LatLng(%f, %f);\n' % (self.center[0],self.center[1]))
        f.write('\tvar myOptions = {\n')
        f.write('\t\tzoom: %d,\n' % (self.zoom))
        f.write('\t\tcenter: centerlatlng,\n')
        f.write('\t\tmapTypeId: google.maps.MapTypeId.ROADMAP\n')
        f.write('\t};\n')
        f.write('\tvar map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);\n')
        f.write('\n')
    
    #Add the points to the map
    def drawpoint(self,f,lat,lon,color,title):
        f.write('\tvar latlng = new google.maps.LatLng(%f, %f);\n'%(lat,lon))
        f.write('\tvar img = new google.maps.MarkerImage(\'%s\');\n' % (self.coloricon.replace('XXXXXX',color)))
        f.write('\tvar marker = new google.maps.Marker({\n')
        if title !=None:
            f.write('\ttitle: "'+str(title)+'",\n')
        f.write('\ticon: img,\n')
        f.write('\tposition: latlng\n')
        f.write('\t});\n')
        f.write('\tmarker.setMap(map);\n')
        f.write('\n')
        
    #Add the line between points
    def drawPolyline(self,f,path, clickable = False, geodesic = True,strokeColor = "#FF0000",strokeOpacity = 1.0, strokeWeight = 2):
        print path
        f.write('\tvar PolylineCoordinates = [\n')
        for coordinate in path[0][:-1]:
            f.write('\t\tnew google.maps.LatLng(%f, %f),\n' % (coordinate[0],coordinate[1]))
        f.write('\t];\n')
        f.write('\n')
        
        f.write('\tvar lineSymbol = { \n')
        f.write('\t\tpath: google.maps.SymbolPath.FORWARD_CLOSED_ARROW \n')
        f.write('\t}; \n')
        f.write('\tvar Path = new google.maps.Polyline({\n')
        f.write('\t\tclickable: %s,\n' % (str(clickable).lower()))
        f.write('\t\tgeodesic: %s,\n' % (str(geodesic).lower()))
        f.write('\t\tpath: PolylineCoordinates,\n')
        f.write('\t\ticons: [{ \n')
        f.write('\t\t\ticon: lineSymbol,\n')
        f.write('\t\t\toffset: "100%"\n')
        f.write('\t\t}],\n')
        f.write('\t\tstrokeColor: "%s",\n' %(strokeColor))
        f.write('\t\tstrokeOpacity: %f,\n' % (strokeOpacity))
        f.write('\t\tstrokeWeight: %d\n' % (strokeWeight))
        f.write('\t});\n')
        f.write('\n')
        f.write('\tPath.setMap(map);\n')
        f.write('\n\n')