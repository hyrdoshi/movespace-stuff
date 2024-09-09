import os
from MoveSpace import MoveSpace
    
for msm in os.listdir('input'):
    if msm.endswith('.json'):
        print(msm)
        msmname=msm.split('.')[0]
        
        MoveSpace.Serialize('input/'+msm, 'output/'+msmname+'.msm')
