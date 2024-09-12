import json, struct

class MoveSpace:
    def DeSerialize(input,output):
        movespace={}
        # Endianness Check
        m=open(input,'rb')
        m.read(4)
        
        # variables
        movespace['version']=struct.unpack('>I',m.read(4))[0]
        movespace['moveName']=m.read(0x40).replace(b'\x00',b'').decode('utf-8')
        movespace['mapName']=m.read(0x40).replace(b'\x00',b'').decode('utf-8')
        movespace['measureSetName']=m.read(0x40).replace(b'\x00',b'').decode('utf-8')
        movespace['moveDuration']=struct.unpack('>f',m.read(4))[0]
        movespace['moveAccurateLowThreshold']=struct.unpack('>f',m.read(4))[0]
        movespace['moveAccurateHighThreshold']=struct.unpack('>f',m.read(4))[0]
        
        #since v5 doesnt have everything
        if movespace['version']==7:
            movespace['autoCorrelationThreshold']=struct.unpack('>f',m.read(4))[0]
            movespace['moveDirectionImpactFactor']=struct.unpack('>f',m.read(4))[0]
       
        # unknown data
        movespace['measureSet']=struct.unpack('>Q',m.read(8))[0]
        movespace['measureValue']=struct.unpack('>I',m.read(4))[0]
        movespace['measureCount']=struct.unpack('>I',m.read(4))[0]
        movespace['energyMeasureCount']=struct.unpack('>I',m.read(4))[0]
        movespace['moveCustomizationFlags']=struct.unpack('>I',m.read(4))[0]
        # Floats, we dont really know how measures work
        movespace['measures']=[]

        # Deprecated
        # while running:
            # byte=m.read(4)
            # if byte==b'':
                # running=False
            # else:
                # movespace['measures'].append(struct.unpack('>f',byte)[0])

        # Instead this is better and faster
        while i := m.read(4):
            movespace['measures'].append(struct.unpack('>f',byte)[0])
        
        json.dump(movespace,open(output,'w'))

    def Serialize(input,output):
        movespace=b''
        namelayout=b''
        for byte in range(16):
            namelayout+=struct.pack('>I',0)
        movedata=json.load(open(input))
        movespace+=struct.pack('>I',1)
        movespace+=struct.pack('>I',movedata['version'])
        movename=namelayout.replace(namelayout[:len(movedata['moveName'])],movedata['moveName'].encode(), 1)
        mapname=namelayout.replace(namelayout[:len(movedata['mapName'])],movedata['mapName'].encode(), 1)
        authorname=namelayout.replace(namelayout[:len(movedata['measureSetName'])],movedata['measureSetName'].encode(), 1)

        movespace+=movename+mapname+authorname

        movespace+=struct.pack('>f',movedata['moveDuration'])
        movespace+=struct.pack('>f',movedata['moveAccurateLowThreshold'])
        movespace+=struct.pack('>f',movedata['moveAccurateHighThreshold'])
        if movedata['version']==7:
            movespace+=struct.pack('>f',movedata['autoCorrelationThreshold'])
            movespace+=struct.pack('>f',movedata['moveDirectionImpactFactor'])
        movespace+=struct.pack('>Q',movedata['measureSet'])
        movespace+=struct.pack('>I',movedata['measureValue'])
        movespace+=struct.pack('>I',movedata['measureCount'])
        movespace+=struct.pack('>I',movedata['energyMeasureCount'])
        movespace+=struct.pack('>I',movedata['moveCustomizationFlags'])
        for measure in movedata['measures']:
            movespace+=struct.pack('>f',measure)

        msmdata=open(output,'wb')
        msmdata.write(movespace)
        msmdata.close()
