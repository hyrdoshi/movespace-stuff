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
        authorname=namelayout.replace(namelayout[:len(movedata['measureSetName'])],movedata['measureSetName'].encode(), 1)

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
        movespace+=struct.pack('>Q',movedata['measureSet'])
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
        if msm.endswith('.txt') or msm.endswith('.msm'):
            msmname=msm
            print(msm.split('.'))
            os.makedirs('temp/', exist_ok=True)
            DeSerialize('input/'+msm, 'temp/'+msmname+'.json')
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
        movenamee=dtape['moveName']
        print("---Move Detected---")
        mapnamee=dtape['mapName']
        print("MapName: " + mapnamee)
        print("Move: " + str(movenamee))
        moveversion=dtape['version']
        print("Version: " + str(moveversion))
        movehigh=dtape['moveAccurateLowThreshold']
        print("LOW Thresh: " + str(movehigh))
        movelow=dtape['moveAccurateHighThreshold']
        print("HIGH Thresh: " + str(movelow))
        movecount=dtape['measureCount']
        print("Count: " + str(movecount))
        measureArray = []
        
        for measure in dtape['measures']:
            if dtape['measureCount'] <= 70:
                randDivide = random.SystemRandom().uniform(1.01,1.25) #dont put more than or equal to 2 otherwise slow moves broken
                divide=measure/randDivide
                newmeasure=divide
                
            else:
                randDivide = random.SystemRandom().uniform(1.01,1.05) #ubi weird tbh
                divide=measure/randDivide
                newmeasure=divide
               
            measureArray.append(newmeasure)
        dtape['measures']=measureArray


        # what should we do to the msm?
        # 1.2 and 3.5 - 5 is default values from jdu/jd+ maps who have updated tracking... (taken from scream n shout, lelia, carnaval boom, born this way...)
        dtape['moveAccurateLowThreshold']=random.SystemRandom().uniform(1.0,1.2)
        if dtape['moveDuration'] >= 0.85:
            dtape['moveAccurateHighThreshold']=random.SystemRandom().uniform(3.0,4.0)
        else:
            dtape['moveAccurateHighThreshold']=random.SystemRandom().uniform(4.5,5.0)

        # since v5 ignores some variables...
        if dtape['version']==7:
            dtape['autoCorrelationThreshold']=1.2
            dtape['moveDirectionImpactFactor']=random.SystemRandom().uniform(0.1,0.200000378)
        dtape['measureValue']=2
        #dtape['measureCount']=50
        json.dump(dtape,open(fr'temp/{files}', 'w'))
    
    
    print('[INFO]: JSON Data....')
    print('[INFO]: Serializing...')
    for msm in os.listdir('temp'):
        if msm.endswith('.json'):
            msm1=msm.split('.')[0]
            msm2=msm.split('.')[1]
            msmname=msm1+msm2
            print(msmname)
            Serialize('temp/'+msm, 'output/'+msmname+'.txt')
    print('[NOTE]: Successfully serialized JSON to MSM!')
  
    
while True:
    print('''
        (~) MSM Tools (~)
        by lunarst4r (v1.0)''')

    print("-------------------------------------------")

    fixing()
    print('Done! enjoy :)')
    shutil.rmtree('temp/')
    exit()
