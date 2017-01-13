import arcpy
from arcpy import mapping


def logMessage(msg):
	print(msg)
	arcpy.AddMessage(msg)

targetFile = r"C:\data\JOE_20160915.mxd" #This is for test
# targetFile = arcpy.GetParameterAsText(0) #For user input in script tool
mxd = mapping.MapDocument(targetFile)
layers = mapping.ListLayers(mxd)
brokenLayers = mapping.ListBrokenDataSources(mxd)
paths = []
for layer in layers:
	if layer in brokenLayers:
		logMessage("Layer " + str(layer) + " is broken")
		continue	
	else:
		if layer.supports("DATASOURCE") and layer.supports("workspacePath") and layer.supports("SERVICEPROPERTIES"):
		#"workspacepath" excludes web service, "serviceproperties" excludes layer from file goedatabase 		
			if arcpy.Exists(layer.workspacePath):
			#this check excludes broken layers
				desc = arcpy.Describe(layer.workspacePath)
				if desc.connectionProperties.server.lower() == "gistst":
					if layer.workspacePath not in paths:
						paths.append(layer.workspacePath)
logMessage("Updating datasource...")
for path in paths:
	mxd.findAndReplaceWorkspacePaths(path, r"Database Connections\RPUD_PRODDB.sde")
	logMessage("Replaced data source from " + str(path) + " to Database Connections\RPUD_PRODDB.sde")
mxd.save()
logMessage("Datasource updated")

