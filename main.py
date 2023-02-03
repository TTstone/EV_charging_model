import Battery_pack as bat
import Charger
import Thermal_management as TM
import matplotlib.pyplot as plt
import time
import matplotlib
import pandas as pd
matplotlib.rc("font",family='FangSong') #字体显示问题
matplotlib.rcParams['font.size'] = 16

#建模全局参数
EV_name = 'E70  '
dt = 0.5 #计算时间步长=50ms
T_bat_ini_global = 21 #默认电池包初始温度

TEM_air = 20 #默认周围空气温度
SOC_ini = 0.12 #默认电池包SOC
SOC_target = 0.9 #默认截止SOC
Capacity = bat.capacity_ref * bat.capcity_mapping(T_bat_ini_global) #实际初始容量
I_out = 0 #充电机初始输出电流
U_out = 0
#T_target = 35 #热管理目标温度

#保存数组
Time_record = []; U_req_record = [] ; I_req_record = []; I_out_record = []; I_in_record = []; SOC_record = []; TEM_record = []

#迭代初始化
SOC = SOC_ini; i = 0; Timer = 0; Q = Capacity * SOC ; T_bat = T_bat_ini_global

#完整迭代
for i in range(3600000):
    Timer += dt
    if Timer <= Charger.T_prep:
        continue
    #计算充电需求以及充电桩输出
    U_req = bat.OCV_SOC(T_bat,SOC) * bat.pack_num
    I_req = bat.charge_mapping(T_bat,SOC) * bat.capacity_ref
    dIdt = Charger.I_response_rate(I_req,I_out)
    I_out = I_out + (dIdt * dt)
    if I_out/I_req >= Charger.I_charger_ratio:
        I_out = I_req * Charger.I_charger_ratio
    U_out = U_req
    P_out = U_out * I_out
    P_T_consumption = TM.T_power_consumption(T_bat)
    if P_T_consumption > P_out:
        P_T_consumption = P_out
    
    #更新SOC
    P_in = P_out - P_T_consumption
    I_in = P_in / U_req
    d_Charge = I_in * dt * bat.charge_effi(T_bat,SOC)
    d_Q = d_Charge/3600 #从秒到Ah换算
    Q += d_Q
    Capacity_RT = bat.capacity_ref * bat.capcity_mapping(T_bat)
    SOC = Q / Capacity_RT
    #更新温度
    P_heat_cool = TM.P_thermal_control(P_T_consumption,T_bat,TEM_air)
    P_R_internal = I_in * I_in * bat.Internal_resistance(T_bat,SOC) #充电内阻功率
    P = P_R_internal + P_heat_cool #总功率
    d_T = (P * dt) / (bat.pack_num * bat.weight * bat.thermal_capacity)
    T_bat += d_T
    #保存数据
    if i % (1/dt) == 0:
        Time_record.append(Timer/60)
        #print(Timer/60)
        #print(I_req)
        U_req_record.append(U_req)
        I_out_record.append(I_out/bat.capacity_ref)
        I_in_record.append(I_in/bat.capacity_ref)
        I_req_record.append(I_req/bat.capacity_ref)
        SOC_record.append(SOC*100)
        TEM_record.append(T_bat)

    #判断是否充满
    if SOC >= SOC_target:
        #print(f"{'外部循环截止时间：'} {Timer/60} ")
        print(f"{str(SOC_ini * 100)} {'%SOC-'} {str(SOC_target * 100)} {'%SOC充电时间：'} {Timer/60} {'min'}")
        break


#定义充电计算函数
def charging_loop(SOC_start=0, SOC_end=1, timer=0):
    global Capacity
    global dt
    global T_bat_ini_global
    global TEM_air
    t_bat = T_bat_ini_global
    #print(f"{'内部初始温度：'} {t_bat} ")
    i_out = 0
    Q = Capacity * SOC_start
    soc = SOC_start
    Time_record = []; U_req_record = [] ; I_req_record = []; I_out_record = []; I_in_record = []; SOC_record = []; TEM_record = []
    for i in range(3600000):
        timer += dt
        if timer <= Charger.T_prep:
            continue
        #计算充电需求以及充电桩输出
        U_req = bat.OCV_SOC(t_bat,soc) * bat.pack_num
        I_req = bat.charge_mapping(t_bat,soc) * bat.capacity_ref
        dIdt = Charger.I_response_rate(I_req,i_out)
        i_out = i_out + (dIdt * dt)
        if i_out/I_req >= Charger.I_charger_ratio:
            i_out = I_req * Charger.I_charger_ratio
        U_out = U_req
        P_out = U_out * i_out
        P_T_consumption = TM.T_power_consumption(t_bat)
        if P_T_consumption > P_out:
            P_T_consumption = P_out
        
        #更新SOC
        P_in = P_out - P_T_consumption
        I_in = P_in / U_req
        d_Charge = I_in * dt * bat.charge_effi(t_bat,soc)
        d_Q = d_Charge/3600 #从秒到Ah换算
        Q += d_Q
        Capacity_RT = bat.capacity_ref * bat.capcity_mapping(t_bat)
        soc = Q / Capacity_RT
        #更新温度
        P_heat_cool = TM.P_thermal_control(P_T_consumption,t_bat,TEM_air)
        P_R_internal = I_in * I_in * bat.Internal_resistance(t_bat,soc) #充电内阻功率
        P = P_R_internal + P_heat_cool #总功率
        d_T = (P * dt) / (bat.pack_num * bat.weight * bat.thermal_capacity)
        t_bat += d_T
        #print(f"{'内部实时温度：'} {t_bat} ")
        
        '''
        #保存数据
        if i % (1/dt) == 0:
            Time_record.append(timer/60)
            #print(Timer/60)
            #print(I_req)
            U_req_record.append(U_req)
            I_out_record.append(i_out/bat.capacity_ref)
            I_in_record.append(I_in/bat.capacity_ref)
            I_req_record.append(I_req/bat.capacity_ref)
            SOC_record.append(soc*100)
            TEM_record.append(t_bat)
        '''
        
        #判断是否充满
        if soc >= SOC_end:
            #print(f"{'内部循环截止时间：'} {timer/60} ")
            print(f"{str(SOC_start * 100)} {'%SOC-'} {str(SOC_end * 100)} {'%SOC充电时间：'} {timer/60} {'min'}")
            break
    '''
    plt.figure(figsize=(16,9))
    plt.suptitle(info,fontsize=16)
    plt.subplot(221)
    plt.ylabel("充电倍率")
    plt.plot(Time_record, I_req_record,label="I_Req")
    plt.plot(Time_record, I_out_record,label="I_CCS")
    plt.plot(Time_record, I_in_record,label="I_BMS")
    plt.legend()
    plt.subplot(222)
    plt.ylabel("SOC")
    plt.plot(Time_record, SOC_record,label="SOC")
    plt.legend()
    plt.subplot(223)
    plt.ylabel("U_Req")
    plt.xlabel('Time [min]')
    plt.plot(Time_record, U_req_record,label="U_Req")
    plt.legend()
    plt.subplot(224)
    plt.ylabel("温度")
    plt.xlabel('Time [min]')
    plt.plot(Time_record, TEM_record,label="TEM")
    plt.legend()
    plt.show()
    '''

t_charge = max(Time_record)

info = '车型：'+ EV_name+'SOC:'+str(int(SOC_ini*100))+'-'+str(int(SOC_target*100))+'%    环境温度:'+str(TEM_air)+'℃'+'    充电时间： '+str(int(t_charge))+'分钟'

#结果可视化
def basic_plot():
    plt.figure(figsize=(16,9))
    plt.suptitle(info,fontsize=16)
    plt.subplot(221)
    plt.ylabel("充电倍率")
    plt.plot(Time_record, I_req_record,label="I_Req")
    plt.plot(Time_record, I_out_record,label="I_CCS")
    plt.plot(Time_record, I_in_record,label="I_BMS")
    plt.legend()
    plt.subplot(222)
    plt.ylabel("SOC")
    plt.plot(Time_record, SOC_record,label="SOC")
    plt.legend()
    plt.subplot(223)
    plt.ylabel("U_Req")
    plt.xlabel('Time [min]')
    plt.plot(Time_record, U_req_record,label="U_Req")
    plt.legend()
    plt.subplot(224)
    plt.ylabel("温度")
    plt.xlabel('Time [min]')
    plt.plot(Time_record, TEM_record,label="TEM")
    plt.legend()
    
    #plt.savefig('E:/BaiduSyncdisk/Python/ChargingTimeSimu/output/'+'SOC_'+str(int(SOC_ini*100))+'-'+str(int(SOC_target*100))+'TEM_'+str(TEM_air)+'C.pdf',bbox_inches='tight')
    plt.show()
    return()

def verification_plot():
    df_ref = pd.read_excel("ref.xlsx", sheet_name='data')
    #length = df_ref['t'].count()
    length = max(df_ref.count())
    #print(length)
    Time_ref = []; SOC_ref = []; TEM_ref = []; I_bms_ref = []; V_bms_ref = []; C_rate_ref = []
    for i in range(length):
        time_ref = df_ref.iloc[i, 0]
        soc_ref = df_ref.iloc[i, 1]
        tem_ref = df_ref.iloc[i, 2]
        i_bms_ref = -1 * df_ref.iloc[i,3]
        v_bms_ref = df_ref.iloc[i,4]
        Time_ref.append(time_ref/60)
        SOC_ref.append(soc_ref)
        TEM_ref.append(tem_ref)
        I_bms_ref.append(i_bms_ref)
        C_rate_ref.append(i_bms_ref/132)
        V_bms_ref.append(v_bms_ref)
    fig, ax =plt.subplots()
    ax.plot(Time_ref, SOC_ref, label='实测SOC', color='green')
    ax.plot(Time_record, SOC_record, label='仿真SOC',linestyle='--', color = 'black')
    ax.set(xlabel='时间 [min]', ylabel='SOC [%]')
    ax.set_xlim((0, 60))
    ax2 = ax.twinx()
    ax2.plot(Time_ref, C_rate_ref, label='实测倍率', color='red')
    ax2.plot(Time_record, I_in_record, label='仿真倍率', color='black',linestyle='--')
    ax2.set(ylabel='充电倍率')
    #ax2.set_ylim((0.44, 0.9))
    #ax2.spines['right'].set_color('green')  # 轴颜色
    #ax2.yaxis.label.set_color('green')  #  标签颜色
    ax2.legend(loc='center left')
    ax.legend(loc='center right')
    ax2.grid()
    fig.suptitle(info)
    
    fig, ax =plt.subplots()
    ax.plot(Time_ref, TEM_ref, label='实测温度', color='green')
    ax.plot(Time_record, TEM_record, label='仿真温度',linestyle='--', color = 'black')
    ax.set(xlabel='时间 [min]', ylabel='温度 [%]')
    ax.set_xlim((0, 60))
    ax.legend(loc='center right')
    ax.grid()
    fig.suptitle(info)
    plt.show()
    return()


#绘图

#verification_plot()
#charging_loop()
charging_loop(0.12, 0.9)
charging_loop(0.3, 0.8)
charging_loop(0.1, 0.9)
basic_plot()
