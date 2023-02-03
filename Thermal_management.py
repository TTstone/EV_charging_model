#导入依赖库
import Battery_pack as bat
import pandas as pd

#热管理系统
T_target = 25 #目标温度
Active_heating = 0 #默认关闭主动加热功能
#heating_COP = 0.8 #PTC工作效率
COP_heat = 0.85 #PTC效率
COP_cool = 2.9 #空调效率 >2.2，实际数据2.9，电池包利用效率 10%
COP_utility_rate = 0.15

#数据读取
df_Thermal = pd.read_excel("input.xlsx", sheet_name='Thermal')

#温控功率需求
def T_power_consumption(T_bat, dT=0, Active_heating=0):
    i_map = 0
    if T_bat < 0:
        j_map = 1
    elif 0 <= T_bat < 10:
        j_map = 2
    elif 10 <= T_bat < 30:
        j_map = 2
    elif 30 <= T_bat < 40:
        j_map = 4
    elif 40 <= T_bat < 50:
        j_map = 5
    elif 50 <= T_bat < 60:
        j_map = 6
    elif T_bat > 60:
        j_map = 7
    T_power = float(df_Thermal.iloc[i_map,j_map])
    return(T_power)

#自然对流
def P_Nature_conv(T_bat, T_air):
    P_conv = bat.pack_area * bat.Convection_nature_rate * (T_air - T_bat)
    return(P_conv)

#总体热量交换
def P_thermal_control(Power, T_bat, T_air):
    P_active = Power * COP_cool * COP_utility_rate * -1
    P_all = P_Nature_conv(T_bat, T_air) + P_active
    return(P_all)