import webvtt
from datetime import datetime
import pandas as pd
deSubTitel=webvtt.read('de_70105212.vtt')
enSubTitel=webvtt.read('en_70105212.vtt')

# EndTimeSubEns=[datetime.strptime(enSubTitel[i].end.split('.')[0],'%X') for i in range(1,len(enSubTitel)) ]
# StartTimeSubEns=[datetime.strptime(enSubTitel[i].start.split('.')[0],'%X') for i in range(1,len(enSubTitel)) ]
StartTimeSubEns=[float((enSubTitel[i].start).replace(':','')) for i in range(1,len(enSubTitel))]
EndTimeSubEns=[float((enSubTitel[i].end).replace(':','')) for i in range(1,len(enSubTitel))]

TextSubEns=[enSubTitel[i].text for i in range(1,len(enSubTitel)) ]


# EndTimeSubDes=[datetime.strptime(deSubTitel[i].end.split('.')[0],'%X') for i in range(1,len(deSubTitel)) ]
# StartTimeSubDes=[datetime.strptime(deSubTitel[i].start.split('.')[0],'%X') for i in range(1,len(deSubTitel)) ]
EndTimeSubDes=[float((deSubTitel[i].end).replace(':','')) for i in range(1,len(deSubTitel))]
StartTimeSubDes=[float((deSubTitel[i].start).replace(':','')) for i in range(1,len(deSubTitel))]


TextSubDes=[deSubTitel[i].text for i in range(1,len(deSubTitel)) ]

def Cheack(StartFirst,EndFirst,StartSecond,EndSecond):
    if int(StartFirst)==int(StartSecond):
        return True
    if (StartSecond-EndFirst)>  (-0.2):
        return False
    elif (StartFirst-EndSecond)>(-0.2):
        return False
    else:
        return True

def getTime(t):
    return t[:2] + ':' + t[2:]

times=[]
textsEn=[]
textsDe=[]
counterEnSub,counterDeSub=0,0
counter=0

while counterDeSub<len(TextSubDes) and counterEnSub<len(TextSubEns):
    Detxt=''
    Entxt=''
    # if len(textsDe)==16:
    #     pass

    while True:
        
        
        if Entxt=='':
            s=min(StartTimeSubDes[counterDeSub],StartTimeSubEns[counterEnSub])
            t='{:04d}'.format(int(str(s).split('.')[0]))
            times.append(getTime(t))
        if (TextSubDes[counterDeSub] not in Detxt) or (TextSubDes[counterDeSub]==TextSubDes[counterDeSub-1]) :
            Detxt+=TextSubDes[counterDeSub]+' '
            pass
        if  (TextSubEns[counterEnSub] not in Entxt) or (TextSubEns[counterEnSub]==TextSubEns[counterEnSub-1]) :
            Entxt+=TextSubEns[counterEnSub]+' '
            pass
        try:
            if Cheack(StartTimeSubDes[counterDeSub+1],EndTimeSubDes[counterDeSub+1],StartTimeSubEns[counterEnSub],EndTimeSubEns[counterEnSub]):
                counterDeSub+=1
            elif  Cheack(StartTimeSubDes[counterDeSub],EndTimeSubDes[counterDeSub],StartTimeSubEns[counterEnSub+1],EndTimeSubEns[counterEnSub+1]):
                counterEnSub+=1
            else :
                counterEnSub+=1
                counterDeSub+=1
                textsEn.append(Entxt)
                textsDe.append(Detxt)
                break
        except:
            textsEn.append(Entxt)
            textsDe.append(Detxt)
            break
    counter+=1
    if counter==len(TextSubDes):
        break

textsEn
textsDe

da=pd.DataFrame({
    'Time':times,
    'Subtitle':textsEn,
    'Translation':textsDe
})
da.to_excel('Data.xlsx')
