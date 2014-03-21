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
    def draw(self, legend):
        with open('map.js','w') as f:
            f.write('function initialize() {')
            f.write('var legend = document.getElementById("legend");')
            for item in legend:
                f.write('var div = document.createElement("div");')
                f.write('div.innerHTML = "<img src=\'%s\'> %s";' % (self.coloricon.replace('XXXXXX','FF0000'), item))
                f.write('legend.appendChild(div);')
            self.drawmap(f)
            for point in  self.points:
                self.drawpoint(f,point[0],point[1],point[2],point[3])
            if self.paths:
                self.drawPolyline(f, self.paths)
            f.write('map.controls[google.maps.ControlPosition.LEFT_CENTER].push(legend);')
            f.write('}')        
    
    #Draw the map
    def drawmap(self, f):
        f.write('var centerlatlng = new google.maps.LatLng(%f, %f);' % (self.center[0],self.center[1]))
        f.write('var myOptions = {')
        f.write('zoom: %d,' % (self.zoom))
        f.write('center: centerlatlng,')
        f.write('mapTypeId: google.maps.MapTypeId.ROADMAP')
        f.write('};')
        f.write('var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);')
        f.write('')
    
    #Add the points to the map
    def drawpoint(self,f,lat,lon,color,title):
        f.write('var latlng = new google.maps.LatLng(%f, %f);'%(lat,lon))
        f.write('var img = new google.maps.MarkerImage(\'%s\');' % (self.coloricon.replace('XXXXXX',color)))
        f.write('var marker = new google.maps.Marker({')
        if title !=None:
            f.write('title: "'+str(title)+'",')
        f.write('icon: img,')
        f.write('position: latlng')
        f.write('});')
        f.write('marker.setMap(map);')
        
    #Add the line between points
    def drawPolyline(self,f,path, clickable = False, geodesic = True,strokeColor = "#0000FF",strokeOpacity = 1.0, strokeWeight = 2):
        f.write('var PolylineCoordinates = [')
        for coordinate in path[0][:-1]:
            f.write('new google.maps.LatLng(%f, %f),' % (coordinate[0],coordinate[1]))
        f.write('];')
        f.write('var lineSymbol = {path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW};')
        f.write('var Path = new google.maps.Polyline({')
        f.write('clickable: %s,' % (str(clickable).lower()))
        f.write('geodesic: %s,' % (str(geodesic).lower()))
        f.write('path: PolylineCoordinates,')
        f.write('icons: [{')
        f.write('icon: lineSymbol,')
        f.write('offset: "100%"')
        f.write('}],')
        f.write('strokeColor: "%s",' %(strokeColor))
        f.write('strokeOpacity: %f,' % (strokeOpacity))
        f.write('strokeWeight: %d' % (strokeWeight))
        f.write('});')
        f.write('Path.setMap(map);')
