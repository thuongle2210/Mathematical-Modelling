import matplotlib.pyplot as plt
import math
import numpy as np 
import pandas as pd 
import io 
import requests
import datetime as dt
def dx(cap_CO2_Air,cap_CO2_Top,MC_BlowAir,MC_ExtAir,MC_PadAir,MC_AirCan,MC_AirTop,MC_AirOut,MC_TopOut):
    MC_BlowAir=def_MC_BlowAir(Eta_HeatCO2,U_Blow,P_Blow,A_Flr)
    print(MC_BlowAir)
    MC_ExtAir=def_MC_ExtAir(U_ExtCO2,Phi_ExtCO2,A_Flr)
    
    MC_PadAir=def_MC_PadAir(U_Pad,Phi_Pad,A_Flr,CO2_Out,CO2_Air)

    f_ThScr=def_f_ThScr(U_ThScr,K_ThScr,Delta_T_AirTop,g,RO_Mean,Delta_RO)
    MC_AirTop=def_MC_AirTop(f_ThScr,CO2_Air,CO2_Top)

    ff_VentSide=def_f_VentRoofSide(C_d,A_Flr,U_Roof,0,U_Side,A_Side,g,h_SideRoof,Delta_T_AirOut,T_mean,C_w,v_Wind) # A_Roof=0
    Eta_InsScr=def_Eta_InsScr(Zeta_InsScr)
    f_leakage=def_f_leakage(v_Wind,C_leakage)
    f_VentRoofSide=def_f_VentRoofSide(C_d,A_Flr,U_Roof,A_Roof,U_Side,A_Side,g,h_SideRoof,Delta_T_AirOut,T_mean,C_w,v_Wind)
    f_VentForced=def_f_VentForced(Eta_InsScr,U_VentForced,Phi_VentForced,A_Flr)
    f_VentSide=def_f_VentSide(Eta_InsScr,ff_VentSide,f_leakage,U_ThScr,f_VentRoofSide,Eta_Side,Eta_SideThr)
    MC_AirOut=def_MC_AirOut(f_VentSide,f_VentForced,CO2_Air,CO2_Out)


    ff_VentRoof=def_ff_VentRoof(C_d,U_Roof,A_Roof,A_Flr,g,h_Roof,Delta_T_AirOut,T_mean,C_w,v_Wind)
    f_VentRoof=def_f_VentRoof(Eta_InsScr,ff_VentRoof,f_leakage,U_ThScr,f_VentRoofSide,Eta_Roof,Eta_RoofThr) 
    # can be changed
    MC_TopOut=def_MC_TopOut(f_VentRoof,CO2_Top,CO2_Out)
    
    h_C_Buf=def_h_C_Buf(C_Buf,C_Max_Buf)
    L=def_L(L0,K,LAI,m)
    fT=def_f(Hd,R,T,T0,S)
    KT=def_KT_WithLAI(LAI,K_T0,Ha,R,T,T0)
    PT_Max=def_PT_Max(KT,fT)
    P_Max_LT=def_PMax_LT(P_MLT,PT_Max,L,L_0_5)
    P=def_P(CO2_Air,CO2_0_5,Res,P_Max_LT)
    R_HOHAP=0.01*P
    MC_AirCan=def_MC_AirCan(M_CH2O,h_C_Buf,P,R_HOHAP)
    

    dx1=(MC_BlowAir+MC_ExtAir+MC_PadAir-MC_AirCan-MC_AirTop-MC_AirOut)/cap_CO2_Air
    dx2=(MC_AirTop-MC_TopOut)/cap_CO2_Top
    return [dx1,dx2]
def def_MC_BlowAir(Eta_HeatCO2,U_Blow,P_Blow,A_Flr):
    return Eta_HeatCO2*U_Blow*P_Blow/A_Flr

def def_MC_ExtAir(U_ExtCO2,Phi_ExtCO2,A_Flr):
    return U_ExtCO2*Phi_ExtCO2/A_Flr

def def_MC_PadAir(U_Pad,Phi_Pad,A_Flr,CO2_Out,CO2_Air):
    return U_Pad*Phi_Pad*(CO2_Out-CO2_Air)/A_Flr

def def_f_ThScr(U_ThScr,K_ThScr,Delta_T_AirTop,g,RO_Mean,Delta_RO):
    return U_ThScr*K_ThScr*((Delta_T_AirTop)**(2/3))+(1-U_ThScr)*((g*(1-U_ThScr)/(2*RO_Mean))*Delta_RO)**(1/2)

def def_MC_AirTop(f_ThScr,CO2_Air,CO2_Top):
    return f_ThScr*(CO2_Air-CO2_Top)

def def_f_VentRoofSide(C_d,A_Flr,U_Roof,A_Roof,U_Side,A_Side,g,h_SideRoof,Delta_T_AirOut,T_mean,C_w,v_Wind):
    component1=C_d/A_Flr
    component2=((U_Roof**2)*(U_Side**2)*(A_Roof**2)*(A_Side**2))/((U_Roof**2)*(A_Roof**2)+(U_Side**2)*(A_Side**2))
    component3=(2*g*h_SideRoof*Delta_T_AirOut)/T_mean
    component4=(((U_Roof*A_Roof+U_Side*A_Side)/2)**2)*C_w*(v_Wind**2)
    return component1*((component2*component3+component4)**(1/2))

def def_Eta_InsScr(Zeta_InsScr):
    return Zeta_InsScr*(2-Zeta_InsScr)

def def_f_leakage(v_Wind,C_leakage):
    if (v_Wind<0.25):
        return 0.25*C_leakage
    else:
        return v_Wind*C_leakage

def def_f_VentForced(Eta_InsScr,U_VentForced,Phi_VentForced,A_Flr):
    return Eta_InsScr*U_VentForced*Phi_VentForced/A_Flr

def def_f_VentSide(Eta_InsScr,ff_VentSide,f_leakage,U_ThScr,f_VentRoofSide,Eta_Side,Eta_SideThr):
    if (Eta_Side>=Eta_SideThr):
        return Eta_InsScr*ff_VentSide+0.5*f_leakage
    else:
        return Eta_InsScr*(U_ThScr*ff_VentSide+(1-U_ThScr)*f_VentRoofSide*Eta_Side)+0.5*f_leakage

def def_MC_AirOut(f_VentSide,f_VentForced,CO2_Air,CO2_Out):
    return (f_VentSide+f_VentForced)*(CO2_Air-CO2_Out)

def def_ff_VentRoof(C_d,U_Roof,A_Roof,A_Flr,g,h_Roof,Delta_T_AirOut,T_mean,C_w,v_Wind):
    component1=C_d*U_Roof*A_Roof/(2*A_Flr)
    component2=(g*h_Roof*Delta_T_AirOut/(2*T_mean))+C_w*(v_Wind**2)
    return component1*(component2**(1/2))

def def_f_VentRoof(Eta_InsScr,ff_VentRoof,f_leakage,U_ThScr,f_VentRoofSide,Eta_Roof,Eta_RoofThr):
    if (Eta_Roof>=Eta_RoofThr):
        return Eta_InsScr*ff_VentRoof+0.5*f_leakage
    else:
        return Eta_InsScr*(U_ThScr*ff_VentRoof+(1-U_ThScr)*f_VentRoofSide*Eta_Roof)+0.5*f_leakage

def def_MC_TopOut(f_VentRoof,CO2_Top,CO2_Out):
    return f_VentRoof*(CO2_Top-CO2_Out)

def def_h_C_Buf(C_Buf,C_Max_Buf):
    if (C_Buf>C_Max_Buf):
        return 0
    else:
        return 1

def def_MC_AirCan(M_CH2O,h_C_Buf,P,R):
    return M_CH2O*h_C_Buf*(P-R)

def def_P(CO2_Air,CO2_0_5,Res,P_Max_LT):
    return ((CO2_Air+CO2_0_5+Res*P_Max_LT)-((CO2_Air+CO2_0_5+Res*P_Max_LT)**2-4*CO2_Air*Res*P_Max_LT))**(1/2)/(2*Res)
def def_K(K_T0,Ha,R,T,T0):
    return K_T0*math.exp((-Ha/R)*(1/T-1/T0))
def def_f(Hd,R,T,T0,S):
    component1=1+math.exp((-Hd/R)*(1/T0-1/(Hd/S)))
    component2=1+math.exp((-Hd/R)*(1/T-1/(Hd/S)))
    return component1/component2
def def_PT_Max(KT,fT):
    return KT*fT
def def_L(L0,K,LAI,m):
    return L0*(1-(K*math.exp(-K*LAI))/(1-m))
def def_KT_WithLAI(LAI,K_T0,Ha,R,T,T0):
    return LAI*K_T0*math.exp((-Ha/R)*(1/T-1/T0))
def def_PMax_LT(P_MLT,PT_Max,L,L_0_5):
    return P_MLT*PT_Max*L/(L+L_0_5)
DATA1=pd.read_csv("https://raw.githubusercontent.com/CEAOD/Data/master/GH_Cucumber/AutonomousGreenhouseChallengeFirstEdition(2018)/Sonoma/Greenhouse_climate.csv")
DATA2=pd.read_csv("https://raw.githubusercontent.com/CEAOD/Data/master/GH_Cucumber/AutonomousGreenhouseChallengeFirstEdition(2018)/meteo.csv")
df1=pd.DataFrame(DATA1)
df2=pd.DataFrame(DATA2)
df1
df=pd.DataFrame()
df[['GHtime','CO2air','Tair','VentLee','Ventwind']]=df1[['GHtime','CO2air','Tair','VentLee','Ventwind']]
df[['Tout','Windsp']]=df2[['Tout','Windsp']]
df['GHtime']=pd.TimedeltaIndex(df['GHtime'],unit='d')+dt.datetime(1899,12,30)
#df
#df=df.dropna()
(df['GHtime'][1]-df['GHtime'][0]).total_seconds()
#for i in range(3,len(df['GHtime'])):
#    if ((df['GHtime'][i]-df['GHtime'][i-1]).total_seconds()>500)==True:
#        print(i)
df.dropna(inplace=True)
df.reset_index(drop=True,inplace=True)
type((df['GHtime'][2]-df['GHtime'][1]).total_seconds())
cap_CO2_Air=3.8 #m
cap_CO2_Top=0.4 #m 
A_Flr=14000 #m^2
U_Blow=1
Eta_HeatCO2=0.057 #mg{CO2}*J^(-1)
P_Blow=500 #W
U_ExtCO2=1
Phi_ExtCO2=72000 #mg*s^(-1)
CO2_Out=668 #mg*m^(-3)
U_Pad=1
Phi_Pad=16.7 #? #m^3*s^(-1)
U_ThScr=1
K_ThScr=0.05*(10**(-3)) #m*K^(-2/3)*s^(-1)
g=9.81 #m*s^(-1)
Delta_T_AirTop= 5 #? #K
RO_Mean= 0.2*(10**3) #kg*m^(-3) #lấy đại ở thermal
Delta_RO=0.5*(10**3) #? #kg*m^(-3)
U_Roof=1
U_Side=1
A_Roof=1400 #? #m^2
A_Side=0.09#? #m^2
C_d=0.2 #?  #Prediction_of_the_Effect_of_Insect-proof_Screens_o.pdf
C_w=0.3 #?
h_SideRoof=1.9 #m(Chua chac chan)
h_Roof=0.68 #m
Delta_T_AirOut= 8 #? #K
T_mean=293#? #K
Zeta_InsScr=1 
C_leakage=1*(10**(-4))
Eta_SideThr=0.9 #? 
Eta_RoofThr=0.9 
U_VentForced=1
Phi_VentForced= 16.7 #? #m^3*s^(-1)
C_Max_Buf=20*(10**3)  #mg{CO2}*m^(-2)
C_Buf=10*(10**3) #? #mg{CO2}*m^(-2)
M_CH2O=30
#Quang hợp
K_T0=0.84
T0=298.15
Ha=37000
R=8.314472
Hd=220000
S=710
Res=250#200
L_0_5=500 #406.5
L0=2000 #545.45
K=1
m=0.1
CO2_0_5=10000 #20000
P_MLT=50 #35
LAI=2
MC_BlowAir=0
MC_ExtAir=0
MC_PadAir=0
MC_AirCan=0
MC_AirTop=0
MC_AirOut=0
MC_TopOut=0
CO2_Air=0
CO2_Top=0
T=0
Eta_Side=0
Eta_Roof=0
v_Wind=0

for i in range(0,1):
    #KHAI Báo biến thay đổi dựa vào DATA
    CO2_Air=float(df['CO2air'][i]*0.0409*44.01)
    CO2_Top=CO2_Air
    T=float(df['Tout'][i]+273)
    Eta_Side=float(df['Ventwind'][i]/100)
    Eta_Roof=float(df['VentLee'][i]/100)
    v_Wind=float(df['Windsp'][i])
    print(dx(cap_CO2_Air,cap_CO2_Top,MC_BlowAir,MC_ExtAir,MC_PadAir,MC_AirCan,MC_AirTop,MC_AirOut,MC_TopOut))
