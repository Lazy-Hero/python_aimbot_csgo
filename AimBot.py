import pymem
import pymem.process
import math

pm = pymem.Pymem("csgo.exe")

client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
engine = pymem.process.module_from_name(pm.process_handle, "engine.dll").lpBaseOfDll


def calculateAngle(entityPositionX, entityPositionY, entityPositionZ, localPlayer):

    localPlayerPositionX = pm.read_float(localPlayer + 0x138)
    localPlayerPositionY = pm.read_float(localPlayer + 0x138+4)
    localPlayerPositionZ = pm.read_float(localPlayer + 0x138+8)

    deltaX = entityPositionX - localPlayerPositionX
    deltaY = entityPositionY - localPlayerPositionY
    deltaZ = entityPositionZ - localPlayerPositionZ

    ah = math.sqrt(deltaX*deltaX + deltaY*deltaY)

    yaw = math.atan2(-deltaZ, ah) * 180.0 / math.pi
    pitch = math.atan2(deltaY, deltaX) * 180.0 / math.pi

    NormalizeViewAngles(yaw, pitch, 0)

    return NormalizeViewAngles(yaw, pitch, 0)

def NormalizeViewAngles(x, y, z):
    if (x > 89):
      x = 89
    if (x < -89):
      x = -89

    while (y > 180):
      y -= 360
    while (y < -180):
      y += 360

    if (z != 0):
      z = 0

    return x, y, z

def getEntityPos(entity):
    entityPositionX = pm.read_float(entity + 0x138)
    entityPositionY = pm.read_float(entity + 0x138+4)
    entityPositionZ = pm.read_float(entity + 0x138+8)

    return entityPositionX, entityPositionY, entityPositionZ


targetList = list()

def aim():

	entity = targetList[0]

	localPlayerInt = pm.read_uint(client + 0xdea964)

	dwClientState = pm.read_uint(engine + (0x59F19C))
	dwClientState_ViewAngles = (0x4D90)

	entityPositionX = getEntityPos(entity)[0]
	entityPositionY = getEntityPos(entity)[1]
	entityPositionZ = getEntityPos(entity)[2]

	angle = calculateAngle(entityPositionX, entityPositionY, entityPositionZ, localPlayerInt)

	pm.write_float(dwClientState + dwClientState_ViewAngles, angle[0])
	
	pm.write_float(dwClientState + dwClientState_ViewAngles + 4, angle[1])

def main():
	while True:
	    entityList = (0x4dffef4)
	        
	    localPlayerInt = pm.read_uint(client + 0xdea964)
	    
	    for i in range(0, 32):
	        entity = pm.read_uint(client + entityList + i * 0x10)
	        
	        
	        if entity and entity != localPlayerInt:
	            entityHealth = pm.read_int(entity + 0x100)
	            if entityHealth > 0 : 
	                targetList.append(entity)
	            else:
	            	targetList.remove(entity)
	            aim()

if __name__ == '__main__':
	main()