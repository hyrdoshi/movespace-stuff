import os
from MoveSpace import MoveSpace
    
for msm in os.listdir('input'):
    if msm.endswith('.msm'):
        print(msm)
        msmname=msm.split('.')[0]
        
        MoveSpace.DeSerialize('input/'+msm, 'output/'+msmname+'.json')
