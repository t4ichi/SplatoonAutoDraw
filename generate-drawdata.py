import numpy as np
from PIL import Image
from queue import Queue
import tqdm
import tkinter
import tkinter.filedialog

# 画像をint型の配列に変換
def img_to_array(file_path):
    img = Image.open(file_path).convert('L')
    img_data = np.array(img)
    int_array = img_data.astype(np.int32)
    return int_array

# int型の配列を2進数に変換
def int_array_to_bin_array(int_array):
    bin_array = [[0 for i in range(int_array.shape[1])] for j in range(int_array.shape[0])]
    for i in range(int_array.shape[0]):
        for j in range(int_array.shape[1]):
            if int_array[i][j] > 128:
                bin_array[i][j] = 1
            else:
                bin_array[i][j] = 0
    return bin_array

# 配列から点の数を数える
def count_point(bin_array):
    row,col = np.shape(bin_array)
    count = 0
    for i in range(row):
        for j in range(col):
            if bin_array[i][j] == 0:
                count += 1
    return count

# 配列から点の座標を求める
def get_point(bin_array):
    row,col = np.shape(bin_array)
    point = [[0 for i in range(2)] for j in range(count_point(bin_array))]
    cnt = 0
    for i in range(row):
        for j in range(col):
            if bin_array[i][j] == 0:
                point[cnt][0] = j
                point[cnt][1] = i
                cnt += 1
    return point

# 二頂点間のユークリッド距離を求める関数
def euclid_distance(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

# 貪欲法で最短経路を求める
def greedy_shortest_path(bin_array):
    row,col = np.shape(bin_array)
    dist = [[-1 for _ in range(col)] for _ in range(row)]

    visited = set()
    visited.add((0,0))
    points = get_point(bin_array)
    prev = [0,0]

    # for i in range(len(points)):
    for i in tqdm.tqdm(range(len(points)),leave=False):
        nex = min([(euclid_distance(prev[0],prev[1],points[j][0],points[j][1]),j) for j in range(len(points)) if (points[j][0],points[j][1]) not in visited])[1]
        x2,y2 = points[nex][0],points[nex][1]
        visited.add((x2,y2))
        dist[y2][x2] = i
        prev = [x2,y2]
    return dist

# bfsで最短経路を求める
def bfs_shortest_path(shortest_array,cnt_point):
    dxs = [1,0,-1,0]
    dys = [0,-1,0,1]
    row,col = np.shape(shortest_array)
    prev = [0,0]
    orders = list()
    # for i in range(cnt_point):
    for i in tqdm.tqdm(range(cnt_point),leave=False):
        seen = [[False for _ in range(col)] for _ in range(row)]
        prev_pass = [[-1 for _ in range(col)] for _ in range(row)]

        que = Queue()
        que.put(prev)
        seen[prev[1]][prev[0]] = True
        is_found = False
        while not que.empty() and not is_found:
            x,y = que.get()
            
            for dx,dy in zip(dxs,dys):
                x2,y2 = x + dx, y + dy
                if x2 < 0 or x2 >= col or y2 < 0 or y2 >= row:
                    continue
                if seen[y2][x2] == True:
                    continue
                seen[y2][x2] = True
                que.put([x2,y2])
                prev_pass[y2][x2] = [x,y]

                if shortest_array[y2][x2] == i:
                    cur = [x2,y2]
                    prev = cur
                    order = []
                    while cur != -1:
                        order.append(cur)
                        cur = prev_pass[cur[1]][cur[0]]
                    order.reverse()
                    orders.append(order)
                    is_found = True
    return orders

# リストからコマンドに変換
def list_to_command(orders):
    command = list()
    for order in orders:
        for i in range(len(order)-1):
            dx = order[i+1][0] - order[i][0]
            dy = order[i][1] - order[i+1][1]
            #(0,1) → U → (0,0)
            #(1,0) → R → (0,1)
            #(0,-1)→ D → (1,0)
            #(-1,0)→ L → (1,1)
            if dx == 1:
                command.append(0)
                command.append(1)
            elif dx == -1:
                command.append(1)
                command.append(1)
            elif dy == 1:
                command.append(0)
                command.append(0)
            elif dy == -1:
                command.append(1)
                command.append(0)
    return command

# 2進数の2次元配列を16進数に変換
def bin_array_to_hex_array_2D(bin_array):
    row,col = np.shape(bin_array)
    hex_array = [[0 for _ in range(col // 8)] for _ in range(row)]
    # print(np.shape(hex_array))
    for i in range(row):
        for j in range(col // 8):
            hex_array[i][j] = int(''.join(map(str, bin_array[i][j*8:(j+1)*8])), 2)
    return hex_array

# 2進数の配列を10進数に変換
def bin_array_to_dec_array(bin_array):
    row,col = np.shape(bin_array)
    hex_array = list()
    for i in range(row):
        hex_array.append(int(''.join(map(str, bin_array[i][0:])),2))
    return hex_array

# 2進数の配列を10進数の配列に変換
def binary_array_to_decimal_array(bin_array):
    decimal_array = []
    chunk_size = 8

    remainder = chunk_size - len(bin_array) % chunk_size
    for _ in range(remainder):
        bin_array.append(0)

    num_chunks = len(bin_array) // chunk_size

    # 8の倍数の区切りごとに処理
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        binary_chunk = bin_array[start:end]
        decimal_value = 0
        for bit in binary_chunk:
            decimal_value = decimal_value * 2 + bit
        decimal_array.append(decimal_value)

    return decimal_array

# C++の配列として保存
def int_array_to_cpp_array(int_array):
    cpp_array = ''
    for row in int_array:
        cpp_row = '{'
        for channel in row:
            cpp_row += str(channel) + ', '
        cpp_row = cpp_row[:-2] + '},\n'
        cpp_array += cpp_row
    cpp_array = cpp_array[:-2] + '\n'
    return cpp_array

# 配列をtxtファイルとして保存
def array_to_txt(int_array, file_path):
    np.set_printoptions(threshold=np.inf)
    with open(file_path, 'w') as f:
        f.write(str(int_array))

# bmp画像として保存
def int_array_to_bmp(int_array, file_path):
    img_data = int_array.astype(np.uint8)
    img = Image.fromarray(img_data)
    img.save(file_path)

def main():
    # 画像を読み込み
    file_path = tkinter.filedialog.askopenfilename()
    # 画像を2進数の配列に変換
    bin = int_array_to_bin_array(img_to_array(file_path))
    # 経路を算出
    path = bfs_shortest_path(greedy_shortest_path(bin),count_point(bin))
    # 経路をコマンドに変換
    command = list_to_command(path)
    command_dec = binary_array_to_decimal_array(command)
    # 画像から配列を算出
    img_hex = bin_array_to_hex_array_2D(bin)
    # データをC++の配列として保存
    output = ""
    output += "const uint8_t ImageData[121][40] PROGMEM = {\n"
    output += int_array_to_cpp_array(img_hex)
    output += "};\n"
    output += f"const uint8_t CommandData[] PROGMEM = {str(command_dec).replace('[','{').replace(']','}')};\n" 
    output += f"const uint16_t FINISH_COUNT = {int(len(command)/2)};"
    # データを保存
    array_to_txt(output, 'data.h')

if __name__ == '__main__':
    main()
