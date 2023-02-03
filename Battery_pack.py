import scipy
import pandas as pd
import numpy as np

#电池参数
pack_num = 120 #电芯数量
weight = 2967 #单电芯质量 g
thermal_capacity = 1.1121 #比热 J/(g*C)
capacity_ref = 132 #容量 Ah
SOC_ini = 10 #初始 SOC
TEM_ini = 25 #初始温度
pack_area = 3 #自然对流散热面积
Convection_nature_rate = 20 #W/(m2 K)
Internal_heating_rate = 1.25 #修正内阻发热

#文件读取
df_C_rate = pd.read_excel("input.xlsx", sheet_name='C_rate')
df_OCV = pd.read_excel("input.xlsx", sheet_name='SOC-OCV')
df_R = pd.read_excel("input.xlsx", sheet_name='Resistance')

def capcity_mapping(Tem): #输入摄氏温度，输出相对容量（容量/标准容量）
    Capcity_rate = 0.96094 + 0.0026028 * Tem - 4.2432e-5 * Tem * Tem
    return Capcity_rate

def charge_mapping(Tem, SOC): #输入摄氏温度与SOC，输出充电倍率限制
    if  -25 <= Tem < -20:
        i_map = 0
    elif -20 <= Tem < -15:
        i_map = 1
    elif -15 <= Tem < -10:
        i_map = 2
    elif -10 <= Tem < -5:
        i_map = 3
    elif -5 <= Tem < 0:
        i_map = 4
    elif 0 <= Tem < 5:
        i_map = 5
    elif 5 <= Tem < 10:
        i_map = 6            
    elif 10 <= Tem < 15:
        i_map = 7    
    elif 15 <= Tem < 20:
        i_map = 8    
    elif 20 <= Tem < 25:
        i_map = 9    
    elif 25 <= Tem < 45:
        i_map = 10    
    elif 45 <= Tem < 50:
        i_map = 11    
    elif 50 <= Tem < 55:
        i_map = 12
    elif 55 <= Tem:
        i_map = 13       
    else:
        return(None)
    
    if 0 <= SOC < 0.05:
        j_map = 1
    elif 0.05 <= SOC < 0.1:
        j_map = 2
    elif 0.1 <= SOC < 0.2:
        j_map = 3
    elif 0.2 <= SOC < 0.3:
        j_map = 4
    elif 0.3 <= SOC < 0.4:
        j_map = 5
    elif 0.4 <= SOC < 0.5:
        j_map = 6
    elif 0.5 <= SOC < 0.6:
        j_map = 7
    elif 0.6 <= SOC < 0.7:
        j_map = 8
    elif 0.7 <= SOC < 0.8:
        j_map = 9
    elif 0.8 <= SOC < 0.85:
        j_map = 10
    elif 0.85 <= SOC < 0.9:
        j_map = 11
    elif 0.9 <= SOC < 0.95:
        j_map = 12
    elif 0.95 <= SOC < 0.98:
        j_map = 13
    elif 0.98 <= SOC:
        j_map = 14
    else: 
        return(None)
    '''
    #针对SOC线性插值
    C_rate_BMS_left = float(df_C_rate.iloc[i_map,j_map-1])
    C_rate_BMS_right = float(df_C_rate.iloc[i_map,j_map])
    d_C = C_rate_BMS_right - C_rate_BMS_left
    k = (SOC - float(df_C_rate.iloc[14,j_map-1]))/(float(df_C_rate.iloc[14,j_map]) - float(df_C_rate.iloc[14,j_map-1]))
    C_rate_BMS = C_rate_BMS_left + k * d_C
    '''

    #取消差值
    C_rate_BMS = float(df_C_rate.iloc[i_map,j_map])

    #C_rate_BMS = float(df_C_rate.iloc[i_map,j_map])
    return(C_rate_BMS)

def charge_effi(Tem,SOC): #输出库伦效率
    #df = pd.read_excel('E:\BaiduSyncdisk\充电性能维度\充电速度仿真模型搭建\充电简化map.xlsx', sheet_name='Efficiency')
    Coulomb_eff = 1
    return(Coulomb_eff)


def Internal_resistance(Tem,SOC=0): #输出充电内阻
    #Interal_R = 0.3111+4.1888*np.exp((-10-float(Tem))/10.339)
    if  0 <= Tem < 10:
        i_map = 0          
    elif 10 <= Tem < 25:
        i_map = 1    
    elif 25 <= Tem < 35:
        i_map = 2    
    elif 35 <= Tem < 45:
        i_map = 3    
    elif 45 <= Tem < 55:
        i_map = 4    
    elif 55 <= Tem:
        i_map = 5       
    else:
        return(None)
    
    if 0 <= SOC < 0.05:
        j_map = 1
    elif 0.05 <= SOC < 0.1:
        j_map = 2
    elif 0.1 <= SOC < 0.15:
        j_map = 3
    elif 0.15 <= SOC < 0.2:
        j_map = 4
    elif 0.2 <= SOC < 0.25:
        j_map = 5
    elif 0.25 <= SOC < 0.3:
        j_map = 6
    elif 0.3 <= SOC < 0.35:
        j_map = 7
    elif 0.35 <= SOC < 0.4:
        j_map = 8
    elif 0.4 <= SOC < 0.45:
        j_map = 9
    elif 0.45 <= SOC < 0.5:
        j_map = 10
    elif 0.5 <= SOC < 0.55:
        j_map = 11
    elif 0.55 <= SOC < 0.6:
        j_map = 12
    elif 0.6 <= SOC < 0.65:
        j_map = 13
    elif 0.65 <= SOC < 0.7:
        j_map = 14
    elif 0.7 <= SOC < 0.75:
        j_map = 15
    elif 0.75 <= SOC < 0.8:
        j_map = 16
    elif 0.8 <= SOC < 0.85:
        j_map = 17    
    elif 0.85 <= SOC < 0.9:
        j_map = 18
    elif 0.9 <= SOC < 0.95:
        j_map = 19
    elif 0.95 <= SOC < 1:
        j_map = 20
    elif SOC >= 1:
        j_map = 21
    else: 
        return(None)
    
    Interal_R = float(df_R.iloc[i_map,j_map])
    Interal_R *= pack_num*0.001
    Interal_R *= Internal_heating_rate
    return(Interal_R)

'''
def Internal_resistance(Tem,SOC=0): #输出充电内阻
    Interal_R = 0.3111+4.1888*np.exp((-10-float(Tem))/10.339)
    Interal_R *= pack_num*0.001
    Interal_R *= 3.5
    return(Interal_R)
'''

def OCV_SOC(Tem, SOC): #输入摄氏温度，输出OCV
    if -20 <= Tem < 10:
        i_map = 0
    elif 10 <= Tem < 25:
        i_map = 0
    elif 25 <= Tem < 45:
        i_map = 0          
    elif Tem >= 45:
        i_map = 0   
    else:
        return(None)
    
    if 0 <= SOC < 0.05:
        j_map = 21
    elif 0.05 <= SOC < 0.1:
        j_map = 20
    elif 0.1 <= SOC < 0.15:
        j_map = 19
    elif 0.15 <= SOC < 0.2:
        j_map = 18
    elif 0.2 <= SOC < 0.25:
        j_map = 17
    elif 0.25 <= SOC < 0.3:
        j_map = 16
    elif 0.3 <= SOC < 0.35:
        j_map = 15
    elif 0.35 <= SOC < 0.4:
        j_map = 14
    elif 0.4 <= SOC < 0.45:
        j_map = 13
    elif 0.45 <= SOC < 0.5:
        j_map = 12
    elif 0.5 <= SOC < 0.55:
        j_map = 11
    elif 0.55 <= SOC < 0.6:
        j_map = 10
    elif 0.6 <= SOC < 0.65:
        j_map = 9
    elif 0.65 <= SOC < 0.7:
        j_map = 8
    elif 0.7 <= SOC < 0.75:
        j_map = 7
    elif 0.75 <= SOC < 0.8:
        j_map = 6
    elif 0.8 <= SOC < 0.85:
        j_map = 5    
    elif 0.85 <= SOC < 0.9:
        j_map = 4
    elif 0.9 <= SOC < 0.95:
        j_map = 3
    elif 0.95 <= SOC < 1:
        j_map = 2
    elif SOC >= 1:
        j_map = 1
    else: 
        return(None)
    OCV = float(df_OCV.iloc[i_map,j_map])
    return(OCV)

#print(charge_mapping(25, 0.68))
#print(capcity_mapping(33))
#print(Internal_resistance(25, 0.45))
#print(OCV_SOC(30,0.57))