import os, re, json, struct, random, shutil
# [NOTE] Cleaned code successfully!
# [INFO] Release Dist v1.0

inputFolder='input/'
# deserialize
def DeSerialize(input,output):
        movespace={}
        running=True
        # read the header
        m=open(input,'rb')
        m.read(4)
        
        # variables
        movespace['version']=struct.unpack('>I',m.read(4))[0]
        movespace['moveName']=m.read(0x40).replace(b'\x00',b'').decode('utf-8')
        movespace['mapName']=m.read(0x40).replace(b'\x00',b'').decode('utf-8')
        movespace['authorName']=m.read(0x40).replace(b'\x00',b'').decode('utf-8')
        movespace['moveDuration']=struct.unpack('>f',m.read(4))[0]
        movespace['moveAccurateLowThreshold']=struct.unpack('>f',m.read(4))[0]
        movespace['moveAccurateHighThreshold']=struct.unpack('>f',m.read(4))[0]
        
        #since v5 doesnt have everything
        if movespace['version']==7:
            movespace['autoCorrelationThreshold']=struct.unpack('>f',m.read(4))[0]
            movespace['moveDirectionImpactFactor']=struct.unpack('>f',m.read(4))[0]
       
        # unknown data
        movespace['moveMeasureBitfield']=struct.unpack('>Q',m.read(8))[0]
        movespace['measureValue']=struct.unpack('>I',m.read(4))[0]
        movespace['measureCount']=struct.unpack('>I',m.read(4))[0]
        movespace['energyMeasureCount']=struct.unpack('>I',m.read(4))[0]
        movespace['moveCustomizationFlags']=struct.unpack('>I',m.read(4))[0]
        #x,y data
        movespace['measures']=[]

        while running:
            byte=m.read(4)
            if byte==b'':
                running=False
            else:
                movespace['measures'].append(struct.unpack('>f',byte)[0])

        json.dump(movespace,open(output,'w'))

def Serialize(input,output):
        movespace=b''
        namelayout=b''
        
        # first 16 bytes of the file are blank, so we replicate this
        for byte in range(16):
            namelayout+=struct.pack('>I',0)
        
        # load the json data, and pack the version
        movedata=json.load(open(input))
        movespace+=struct.pack('>I',1)
        movespace+=struct.pack('>I',movedata['version'])
        
        # moveName mapName authorName?
        movename=namelayout.replace(namelayout[:len(movedata['moveName'])],movedata['moveName'].encode(), 1)
        mapname=namelayout.replace(namelayout[:len(movedata['mapName'])],movedata['mapName'].encode(), 1)
        authorname=namelayout.replace(namelayout[:len(movedata['authorName'])],movedata['authorName'].encode(), 1)

        # add it to the file (+=)
        movespace+=movename+mapname+authorname

        # variables?
        movespace+=struct.pack('>f',movedata['moveDuration'])
        movespace+=struct.pack('>f',movedata['moveAccurateLowThreshold'])
        movespace+=struct.pack('>f',movedata['moveAccurateHighThreshold'])
        
        # skips data v5 doesnt have
        if movedata['version']==7:
            movespace+=struct.pack('>f',movedata['autoCorrelationThreshold'])
            movespace+=struct.pack('>f',movedata['moveDirectionImpactFactor'])
        
        # unknwon flags
        movespace+=struct.pack('>Q',movedata['moveMeasureBitfield'])
        movespace+=struct.pack('>I',movedata['measureValue'])
        movespace+=struct.pack('>I',movedata['measureCount'])
        movespace+=struct.pack('>I',movedata['energyMeasureCount'])
        movespace+=struct.pack('>I',movedata['moveCustomizationFlags'])
        
        #update x,y
        for measure in movedata['measures']:
            movespace+=struct.pack('>f',measure)

        msmdata=open(output,'wb')
        msmdata.write(movespace)
        msmdata.close()

def fixing():
    print('[INFO]: Deserializing...')
    for msm in os.listdir('input'):
        if msm.endswith('.msm'):
            msmname=msm.split('.')[0]
            os.makedirs('temp/', exist_ok=True)
            DeSerialize('input/'+msm, 'temp/'+msm+'.json')
    print('[SUCCESS] Successfuly deserialized MSM!')
    
    for files in os.listdir("temp/"):
        current_file = files
        def readCKD2(files):
            jsonbytes=open(fr'temp/{files}','rb')
            bytedata=jsonbytes.read()
            bytelength=len(bytedata)
            uselessbyte=bytedata[bytelength-1:]
            if uselessbyte==b'\x00':
                jsondata=bytedata[:bytelength-1]
            else:
                jsondata=bytedata
            return jsondata.decode('utf-8')

        dtape=json.loads(readCKD2(files))
        measureArray = []
        
        
        # what should we do to the msm?
        # 1.2 and 3.5 - 5 is default values from jdu/jd+ maps who have updated tracking... (taken from scream n shout, lelia, carnaval boom, born this way...)
        dtape['moveAccurateLowThreshold']=1.0
        dtape['moveAccurateHighThreshold']=4.0
        json.dump(dtape,open(fr'temp/{files}', 'w'))
    
    
    print('[INFO]: JSON Data....')
    print('[INFO]: Serializing...')
    for msm in os.listdir('temp'):
        msmname=msm
        filefor=re.split("[_.]", msm)
        mapName=filefor[0]
        os.makedirs('output/world/maps/'+mapName+'/timeline/moves/wiiu/', exist_ok=True)
        Serialize('temp/'+msm, 'output/world/maps/'+mapName+'/timeline/moves/wiiu/'+msm)
    print('[NOTE]: Successfully serialized JSON to MSM!')
  
    
while True:
    print('''
    
        DO NOT SHARE! TOOL IS NOT FINAL YET!
        (~) MSM Tools (~)
        by lunarst4r (v1.0)''')

    print("-------------------------------------------")

    fixing()
    print('Done! enjoy :)')
    shutil.rmtree('temp/')
    exit()
