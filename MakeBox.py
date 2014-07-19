import copy
import Rhino
import rhinoscriptsyntax as rs
import rhinoscript

## Box dimension is calculated based on inside volume.

## tolerance reference:
	#Laser cutting
		# Masonite 3mm thick - 0.01 inch
	
def main():
	#Get parameters
	width = rs.GetReal("Width of box: ",10.0,1.0)
	height = rs.GetReal("height of box: ",10.0,1.0)
	depth = rs.GetReal("depth of box: ",10.0,1.0)
	wt = rs.GetReal("Wall Thickness: ",0.25,0.06125)
	tolerance = rs.GetReal("tolerance: ",0.01,0)
	numSeg = rs.GetInteger("number of segment: ",10,3)

	#Validate parameters
	if not width or not height or not depth: return Rhino.Commands.Result.Failure
	if not wt or not numSeg: return Rhino.Commands.Result.Failure
	
	#Make walls
	bottom = topBottomPanel(width,depth,numSeg,wt,tolerance)
	top = topBottomPanel(width,depth,numSeg,wt,tolerance)
	right = sidePanel(depth,height,numSeg,wt,tolerance)
	left = sidePanel(depth,height,numSeg,wt,tolerance)
	back = frontBackPanel(width,height,numSeg,wt,tolerance)
	front = frontBackPanel(width,height,numSeg,wt,tolerance)
	rs.MoveObject(right,Rhino.Geometry.Point3d(width+(wt*2), -wt, 0))
	rs.MoveObject(left,Rhino.Geometry.Point3d(-height-(wt*4), -wt, 0))
	rs.MoveObject(back,Rhino.Geometry.Point3d(0, depth+(wt*2), 0))
	rs.MoveObject(front,Rhino.Geometry.Point3d(0, -height-(wt*4), 0))
	rs.MoveObject(top,Rhino.Geometry.Point3d(0, (depth+wt*2)+(height+wt*4), 0))
	
	return Rhino.Commands.Result.Success

def sidePanel(depth,height,numSeg,wt,tolerance):
	points = makeZig(Rhino.Geometry.Point3d(wt, 0, 0),height,numSeg,wt,tolerance)
	points.insert(0,Rhino.Geometry.Point3d(0, 0, 0))
	points.append(Rhino.Geometry.Point3d(height+(wt*2), 0, 0))
	zig1 = rhinoscript.curve.AddPolyline(points)
	
	points = makeZig4(Rhino.Geometry.Point3d(wt, 0, 0),depth,numSeg,wt,tolerance)
	points.insert(0,Rhino.Geometry.Point3d(0, 0, 0))
	points.append(Rhino.Geometry.Point3d(depth+(wt*2), 0, 0))
	zig2 = rhinoscript.curve.AddPolyline(points)
	
	rs.RotateObject(zig2,Rhino.Geometry.Point3d(0, 0, 0),90)
	zig3 = rs.MirrorObject(zig2,Rhino.Geometry.Point3d((height+(wt*2))/2, 0, 0),Rhino.Geometry.Point3d((height+(wt*2))/2,depth, 0),True)
	zig4 = rs.MirrorObjects(zig1,Rhino.Geometry.Point3d(0,(depth+(wt*2))/2, 0),Rhino.Geometry.Point3d(height, (depth+(wt*2))/2, 0),True)
	return rhinoscript.curve.JoinCurves([zig1,zig2,zig3,zig4],True)

def frontBackPanel(width,height,numSeg,wt,tolerance):
	points = makeZig(Rhino.Geometry.Point3d(0, 0, 0),width,numSeg,wt,tolerance)
	zig1 = rhinoscript.curve.AddPolyline(points)
	points = makeZig(Rhino.Geometry.Point3d(wt, 0, 0),height,numSeg,wt,tolerance)
	points.insert(0,Rhino.Geometry.Point3d(0, 0, 0))
	points.append(Rhino.Geometry.Point3d(height+(wt*2), 0, 0))
	zig2 = rhinoscript.curve.AddPolyline(points)
	rs.RotateObject(zig2,Rhino.Geometry.Point3d(0, 0, 0),90)
	zig3 = rs.MirrorObjects(zig1,Rhino.Geometry.Point3d(0, (height+(wt*2))/2, 0),Rhino.Geometry.Point3d(width, (height+(wt*2))/2, 0),True)
	zig4 = rs.MirrorObjects(zig2,Rhino.Geometry.Point3d(width/2, 0, 0),Rhino.Geometry.Point3d(width/2, (height+(wt*2)), 0),True)
	return rhinoscript.curve.JoinCurves([zig1,zig2,zig3,zig4],True)	
def topBottomPanel(width,depth,numSeg,wt,tolerance):
	points = makeZig2(Rhino.Geometry.Point3d(0, 0, 0),width,numSeg,wt,tolerance)
	zig1 = rhinoscript.curve.AddPolyline(points)
	points = makeZig3(Rhino.Geometry.Point3d(0, 0, 0),depth,numSeg,wt,tolerance)
	zig2 = rhinoscript.curve.AddPolyline(points)
	rs.RotateObject(zig2,Rhino.Geometry.Point3d(0, 0, 0),90)
	zig3 = rs.MirrorObjects(zig1,Rhino.Geometry.Point3d(0, depth/2, 0),Rhino.Geometry.Point3d(width, depth/2, 0),True)
	zig4 = rs.MirrorObjects(zig2,Rhino.Geometry.Point3d(width/2, 0, 0),Rhino.Geometry.Point3d(width/2, depth, 0),True)
	return rhinoscript.curve.JoinCurves([zig1,zig2,zig3,zig4],True)
	
	
def makeZig(startPoint,length,numSeg,wt,tolerance):
	segmentLength = length / ((numSeg*2)+1)
	points = []
	points.append(startPoint)
	for i in range(0,numSeg*2,2):
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)+tolerance/2, startPoint[1], startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)+tolerance/2, startPoint[1]+wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)-tolerance/2, startPoint[1]+wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)-tolerance/2, startPoint[1], startPoint[2]))
	points.append(Rhino.Geometry.Point3d(startPoint[0]+length, startPoint[1], startPoint[2]))
	return points

def makeZig2(startPoint,length,numSeg,wt,tolerance):
	segmentLength = length / ((numSeg*2)+1)
	points = []
	points.append(startPoint)
	for i in range(0,numSeg*2,2):
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)-tolerance/2, startPoint[1], startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)-tolerance/2, startPoint[1]-wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)+tolerance/2, startPoint[1]-wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)+tolerance/2, startPoint[1], startPoint[2]))
	points.append(Rhino.Geometry.Point3d(startPoint[0]+length, startPoint[1], startPoint[2]))
	return points

def makeZig3(startPoint,length,numSeg,wt,tolerance):
	segmentLength = length / ((numSeg*2)+1)
	points = []
	points.append(startPoint)
	for i in range(0,numSeg*2,2):
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)-tolerance/2, startPoint[1], startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)-tolerance/2, startPoint[1]+wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)+tolerance/2, startPoint[1]+wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)+tolerance/2, startPoint[1], startPoint[2]))
	points.append(Rhino.Geometry.Point3d(startPoint[0]+length, startPoint[1], startPoint[2]))
	return points

def makeZig4(startPoint,length,numSeg,wt,tolerance):
	segmentLength = length / ((numSeg*2)+1)
	points = []
	points.append(startPoint)
	for i in range(0,numSeg*2,2):
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)+tolerance/2, startPoint[1], startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+1)+tolerance/2, startPoint[1]-wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)-tolerance/2, startPoint[1]-wt, startPoint[2]))
		points.append(Rhino.Geometry.Point3d(startPoint[0]+segmentLength*(i+2)-tolerance/2, startPoint[1], startPoint[2]))
	points.append(Rhino.Geometry.Point3d(startPoint[0]+length, startPoint[1], startPoint[2]))
	return points
				
if __name__=="__main__":
	main()