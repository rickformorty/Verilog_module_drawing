import os
import numpy as np
import matplotlib.pyplot as plt

# 指定文件夹路径
folder_path = "."

# 定义一个函数来解析模块定义内的内容
def read_module_content_for_one(lines):
    module_content = []  # 用于存储模块定义内的内容
    module_start = False  # 标记是否已经进入了模块定义

    # 遍历文件的每一行
    for line in lines:
        line = line.strip()  # 去除首尾空白字符

        # 如果已经进入了模块定义
        if module_start:
            # 如果当前行为空或者以注释符号开头，则跳过
            if not line or line.startswith('//'):
                continue
            # 如果遇到模块定义结束的符号，则停止解析
            elif line == ');':
                module_content.append(line)
                break
            # 否则将当前行添加到模块内容中
            else:
                module_content.append(line)
        # 如果还没有进入模块定义，检查当前行是否包含模块定义的开始符号
        elif line.startswith('module'):
            module_start = True
            module_content.append(line)

    return module_content

def get_subplot_num(num):
    row, column = int(np.ceil(num/3)), 3
    return row, column

def get_module_name(module_content):
    module_name = module_content[0].replace('module', '').strip()
    return module_name

def get_input_name(module_content):
    input_ports = []
    clk_exist = False
    for line in module_content:
        if 'input' in line:
            if 'clk' in line:
                clk_exist = True
            else:
                input_ports.append(line.split('input')[1].strip(',').strip(' '))        # Assume format: input in_data,
    return input_ports, clk_exist

def get_output_name(module_content):
    output_ports = []
    for line in module_content:
        if 'output' in line:
            output_ports.append(line.split('output')[1].strip(',').strip(' '))      # Assume format: output out_data,
    return output_ports

# draw port
def draw_module(path, index, row, column):
    clk_draw_top = True
    margin = .2
    # read .v file
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    module_content = read_module_content_for_one(lines)

    # get module name
    module_name = get_module_name(module_content)
    # read port
    input_list, clk_exist = get_input_name(module_content)
    output_list = get_output_name(module_content)

    # get num
    input_num = len(input_list)
    output_num = len(output_list)
    max_port = max(input_num, output_num)
    high_max = (max_port+1)*margin

    # draw a rectangle 
    width = .6
    plt.subplot(row, column, index)
    plt.plot([0, width], [0, 0], color='black')                     # bottom
    plt.plot([0, 0], [0, high_max], color='black')                  # left
    plt.plot([width, width], [0, high_max], color='black')          # right
    plt.plot([0, width], [high_max, high_max], color='black')       # top

    upper_fact = 0.37
    if (input_num < output_num):
    # input num < output num
        # input port
        margin_input = high_max/(input_num +1)
        for i in range(1,input_num + 1):
            high = i*margin_input
            text_high = high_max - high + .15*margin_input
            plt.plot([-.2, 0], [high, high], color='black')  # input port
            plt.text(-.05, text_high, input_list[i-1], va='center', ha='right', fontsize=8)
            plt.arrow(-0.08, high, 0.05, 0, head_width=0.05, head_length=0.03, fc='black', ec='black')

        # output port
        high = margin
        margin_output = margin
        for i in range(1,output_num + 1):
            text_high = high_max - high + upper_fact*margin_output
            plt.plot([width, width + .2], [high, high], color='black')  # output port
            plt.text(width+.05, text_high, output_list[i-1], va='center', ha='left', fontsize=8)
            arrow_length = -.08
            plt.arrow(width+.2 + arrow_length, high, 0.05, 0, head_width=.05, head_length=.03, fc='black', ec='black')
            high += margin
    else:
    # input num > output num
        # input port
        high = margin
        margin_input = margin
        for i in range(1,input_num + 1):
            text_high = high_max - high + upper_fact*margin_input
            plt.plot([-.2, 0], [high, high], color='black')  # input port
            plt.text(-.05, text_high, input_list[i-1], va='center', ha='right', fontsize=8)
            plt.arrow(-0.08, high, 0.05, 0, head_width=0.05, head_length=0.03, fc='black', ec='black')
            high += margin

        # output port
        margin_output = high_max/(output_num +1)
        for i in range(1,output_num + 1):
            high = i*margin_output
            text_high = high_max - high + .15*margin_output
            plt.plot([width, width+.2], [high, high], color='black')  # output port
            plt.text(width+.05, text_high, output_list[i-1], va='center', ha='left', fontsize=8)
            arrow_length = -.08
            plt.arrow(width+.2 + arrow_length, high, 0.05, 0, head_width=.05, head_length=.03, fc='black', ec='black')

    # clk arrow
    if(clk_exist):
        if(clk_draw_top == True):
            # top arrow
            plt.arrow(width/2, high_max+.1, 0, -.1, head_width=0.05, head_length=0.07, fc='none', ec='blue')
            plt.plot([width/2, width/2], [high_max, high_max-.03], color='blue')     # triangle inside line
            plt.text(width/2-.07, high_max+.05, f'clk', va='center', ha='left', fontsize=8)
        else:
            # bottom arrow
            plt.arrow(.5, -.1, 0, .1, head_width=0.05, head_length=0.07, fc='none', ec='blue')
            plt.plot([.5, .5], [0, .03], color='black')     # triangle inside line

    # module name
    plt.text(width/2, high_max/2, module_name, va='center', ha='center', fontsize=16, color = 'red')

    plt.xlim(-0.5, width+.5)
    plt.axis('off')

# 获取文件夹中所有文件的列表
files = os.listdir(folder_path)

# 筛选出以'.v'后缀结尾的文件
v_files = [file for file in files if file.endswith('.v')]

module_num = len(v_files)
row, column = get_subplot_num(module_num)

plt.figure(figsize=(8*column,6*row))
for index, file in enumerate(v_files):
    draw_module(path = os.path.join(folder_path, file), index = index + 1, row= row, column = column)

plt.tight_layout()
plt.savefig('module_Fig.png')
plt.show()