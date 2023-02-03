#导入依赖库
import pandas

#充电桩参数
V_charger_limit = 1200 #电压限制
I_charger_limit = 250 #电流限制
P_charger_limit = 250000 #功率限制
T_prep = 3 #充电桩交互初始时间
#V_charger_ratio = 0.98 #电压跟随能力
I_charger_ratio = 0.985 #电流跟随能力 0.98
#dt = main.dt #传输时间步长

#判断电流爬升、下降方向
def Sign(input): 
    if input > 0:
        output = 1
    elif input < 0:
        output = -1
    else:
        output = 0
    return(output)

#电流跟随速度
def I_response_rate(I_Req, I_Out_C):
    dI = float(I_Req - I_Out_C)
    #print("dI")
    #print(dI)
    if abs(dI) == 0:
        dIdt = Sign(dI) * 0
    elif abs(dI) > 125:
        dIdt = Sign(dI) * 25
    elif abs(dI) > 20 and abs(dI) <=125:
        dIdt = Sign(dI) * 15
    elif abs(dI) <= 20:
        dIdt = Sign(dI) * 5
    else:
        dIdt = 0
    return(dIdt)

#功率切换延迟
def response_fun(I_Req, I_Out_C):
    if I_Out_C != I_Req * I_charger_ratio:
        time_response = 60
    else: time_response = 0
    return(time_response)

#print(I_response_rate(80,0))
#星星充电-电流切换功率模块响应1min
#3-8s到达需求功率