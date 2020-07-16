
# 函数输出打分
output_score = list(range(12))
print(output_score)

# 正确分类
y = [0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1]
print(len(y))

# 设定p，集合中正例比例，这里范围为0-100，所以还要除以100
p = list(range(0,101,10))
p = [i/100 for i in p]
print(p)

# 设定代价
c01 = 3
c02 = 2

# 判断阈值
theta = 6.5

# 函数输出判断
def calculate_output_result(output_score,theta):
    output_result = []
    for i in range(len(output_score)):
        if output_score[i] < theta:
            output_result.append(0)
        else:
            output_result.append(1)
    return output_result 

output_result = calculate_output_result(output_score,theta)
print(output_result)

# 统计正例和反例的个数
import pandas as pd
def calculate_m_positive_negative(y):
    result = pd.value_counts(y)
    m_positive = result[1]
    m_negative = result[0]
    return m_positive, m_negative
m_positive, m_negative = calculate_m_positive_negative(y)
print(m_positive, m_negative)

# 计算混淆矩阵的圈1，圈2，圈3，圈4
def calculate_confusion(y,output_result):
    con1 = 0
    con2 = 0
    con3 = 0
    con4 = 0
    for i in range(len(y)):
        if y [i] == 1:  # 如果是真正例
            if y[i] == output_result[i]:    # 且预测结果也是正例
                con1 += 1
            else:   # 预测结果是反例，即预测错误
                con2 += 1
        else:
            if y[i] == output_result[i]: # 否则真反例，且预测结果也是反例
                con4 += 1
            else:   # 反例预测成真例
                con3 += 1
    return con1, con2, con3, con4
con1, con2, con3, con4 = calculate_confusion(y,output_result)
print(con1, con2, con3, con4)

# 求几个比例，保留四位小数
def calculate_FNR_FPR(con1,con2,con3,con4):
    FNR = round(con2/(con1+con2), 4)
    FPR = round(con3/(con3+con4),4)
    return FNR, FPR
FNR, FPR = calculate_FNR_FPR(con1,con2,con3,con4)
print(FNR, FPR)

# 正概率代价
def calculate_Pcost(p, c01, c02):
    Pcosts = []
    for i in range(len(p)):
        Pcost = round((p[i]*c01)/(p[i]*c01+(1-p[i])*c02),4)
        Pcosts.append(Pcost)
    return Pcosts
Pcosts  = calculate_Pcost(p, c01, c02)
print(Pcosts)

# 归一化总概率
def calculate_cost_norm(p, c01, c02, FNR, FPR):
    costs_norm = []
    for i in range(len(p)):
        cost_norm = round((FNR*(p[i]*c01)+FPR*(1-p[i])*c02)/(p[i]*c01+(1-p[i])*c02),4)
        costs_norm.append(cost_norm)
    return costs_norm
costs_norm = calculate_cost_norm(p, c01, c02, FNR, FPR)
print(costs_norm)

# 画出图像
import matplotlib as mpl
import matplotlib.pyplot as plt
def plot_lines(X, Y, color):
    plt.plot(X, Y, color)
    return
plot_lines(Pcosts, costs_norm,'r')
plot_lines(p, costs_norm, "b:")
plt.show()

# 生成theta(多个theta)
thetas = list(range(12))
thetas = [i+0.5 for i in thetas]
print(thetas)

# 定义计算每个theta对应的点的函数，并存在列表里
def calculate_Pcost_cost_norm(thetas, output_score, y, calculate_Pcost, calculate_cost_norm):
    Pcosts_n = []
    costs_norm_n = []
    theta_FPR_FNR = {}
    for i in range(len(thetas)):
        theta = thetas[i]
        
        # 计算输出结果
        output_result = calculate_output_result(output_score,theta)
        # print(output_result)

        # 统计正例反例个数
        m_positive, m_negative = calculate_m_positive_negative(y)
        
        # 计算混淆矩阵
        con1, con2, con3, con4 = calculate_confusion(y,output_result)
        # print(con1, con2, con3, con4)
        
        # 求 FNR FPR
        FNR, FPR = calculate_FNR_FPR(con1,con2,con3,con4)
        theta_FPR_FNR[theta]=[FNR, FPR]
        
        # 正概率代价
        Pcosts  = calculate_Pcost(p, c01, c02)
        Pcosts_n.append(Pcosts)
        
        # 归一化总概率
        costs_norm = calculate_cost_norm(p, c01, c02, FNR, FPR)
        costs_norm_n.append(costs_norm)
        
    return Pcosts_n, costs_norm_n, theta_FPR_FNR    

# 调用函数计算每个theta对应的点
Pcosts_n, costs_norm_n, theta_FPR_FNR  = calculate_Pcost_cost_norm(thetas, output_score,y, calculate_Pcost, calculate_cost_norm)

for i in range(len(Pcosts_n)):
    plot_lines(Pcosts_n[i], costs_norm_n[i],'r')
plt.show()

# 查看theta与对应的FPR，FNR
print(theta_FPR_FNR)
print(' ')
