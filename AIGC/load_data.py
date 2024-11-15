import scipy.io
import os

# 电池名称列表
battery_names = [29, 33, 41, 45, 49, 53]

# 输出目录
output_dir = r'C:\\Users\\Administrator\\Desktop\\AIGC-batterty\\AIGC\\output'

# 如果输出目录不存在，创建一个
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 读取.mat文件并提取数据
def extract_and_save_data(mat_file_path, battery_name):
    # 加载.mat文件
    mat_data = scipy.io.loadmat(mat_file_path)
    filename = mat_file_path.split('\\')[-1].split('.')[0]
    col = mat_data[filename]

    col = col[0][0][0][0]  # 提取矩阵数据
    size = col.shape[0]

    Voltage = []
    Current = []
    Temperature = []
    Time = []

    # 解析每条数据的详细内容
    for i in range(size):
        if str(col[i][0][0]) == 'charge':  # 只处理 'charge' 类型的数据
            Voltage1 = []
            Current1 = []
            Temperature1 = []
            Time1 = []
            # 提取各项数据
            for j in range(6):
                if j == 0:  # Voltage
                    t = col[i][3][0][0][j][0]
                    Voltage1.extend([t[m] for m in range(len(t))])
                elif j == 1:  # Current
                    t = col[i][3][0][0][j][0]
                    Current1.extend([t[m] for m in range(len(t))])
                elif j == 2:  # Temperature
                    t = col[i][3][0][0][j][0]
                    Temperature1.extend([t[m] for m in range(len(t))])
                elif j == 5:  # Time
                    t = col[i][3][0][0][j][0]
                    Time1.extend([t[m] for m in range(len(t))])

            Voltage.extend(Voltage1)
            Voltage.append("\n")
            Current.extend(Current1)
            Current.append("\n")
            Temperature.extend(Temperature1)
            Temperature.append("\n")
            Time.extend(Time1)
            Time.append("\n")

            # 保存到文件
    battery_num = f'{battery_name:02d}'  # 电池编号格式为两位数
    save_to_file(Voltage, Current, Temperature, Time, battery_num)

# 将数据保存到文件的辅助函数
def save_to_file(Voltage, Current, Temperature, Time, battery_num):
    # 写入文本文件
    file_path_voltage = os.path.join(output_dir, f'Voltage_{battery_num}.txt')
    file_path_current = os.path.join(output_dir, f'Current_{battery_num}.txt')
    file_path_temperature = os.path.join(output_dir, f'Temperature_{battery_num}.txt')
    file_path_time = os.path.join(output_dir, f'Time_{battery_num}.txt')

    # 以追加的方式写入数据（每次循环的数据写在一行）
    with open(file_path_voltage, 'a') as f_voltage:
        f_voltage.write(' '.join(map(str, Voltage)) + '\n')

    with open(file_path_current, 'a') as f_current:
        f_current.write(' '.join(map(str, Current)) + '\n')

    with open(file_path_temperature, 'a') as f_temperature:
        f_temperature.write(' '.join(map(str, Temperature)) + '\n')

    with open(file_path_time, 'a') as f_time:
        f_time.write(' '.join(map(str, Time)) + '\n')

# 遍历每个电池文件，提取数据并保存
for battery_name in battery_names:
    mat_file_path = f'C:\\Users\\Administrator\\Desktop\\AIGC-batterty\\AIGC\\venv\\B00{battery_name}.mat'
    if os.path.exists(mat_file_path):
        extract_and_save_data(mat_file_path, battery_name)
    else:
        print(f"文件 {mat_file_path} 不存在，跳过。")

print("数据提取完成！")
