import sys
sys.path.insert(0,'cpp_lib')
import cpp_core
import random
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager


font_path = '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'
font_manager.fontManager.addfont(font_path)
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False

def python_cosine(a,b):
    dot=sum(x*y for x,y in zip(a,b))
    norm_a=sum(x*x for x in a)**0.5
    norm_b=sum(y*y for y in b)**0.5
    return dot/(norm_a*norm_b) if norm_a and norm_b else 0.0

dims=[128,256,512,1024,2048,4096]
cpp_times,py_times=[],[]

for dim in dims:
    a=[random.random() for _ in range(dim)]
    b=[random.random() for _ in range(dim)]
    iterations=1000

    #C++
    start=time.perf_counter()
    for _ in range(iterations):
        cpp_core.cosine_similarity(a,b)
    cpp_times.append((time.perf_counter()-start)/iterations*1e6)

    #Python
    start=time.perf_counter()
    for _ in range(iterations):
        python_cosine(a,b)
    py_times.append((time.perf_counter()-start)/iterations*1e6)

print("维度 | C++ (μs) | Python (μs) | 加速比")
for i,dim in enumerate(dims):
    print(f"{dim:4d}|{cpp_times[i]:8.1f}|{py_times[i]:11.1f}|{py_times[i]/cpp_times[i]:5.1f}x")

plt.figure(figsize=(10,6))
plt.plot(dims,cpp_times,'o-',label='C++')
plt.plot(dims,py_times,'s-',label='Python')
plt.xlabel('维度')
plt.ylabel('耗时 (μs)')
plt.title('余弦相似度: C++ vs Python')
plt.legend()
plt.grid(True)
plt.xscale('log',base=2)
plt.yscale('log')
plt.savefig('benchmarks/similarity_comparison.png',dpi=150)
print("图表已保存: benchmarks/similarity_comparison.png")




