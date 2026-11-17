import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager

font_manager.fontManager.addfont("/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc")
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei"]
plt.rcParams["axes.unicode_minus"] = False

with open("docs/hyde_eval_result.json", "r", encoding="utf-8") as f:
    data = json.load(f)

modes = ["原始检索", "HyDE 检索"]
accs = [data["original"]["accuracy"] * 100, data["hyde"]["accuracy"] * 100]

plt.figure(figsize=(8, 5))
bars = plt.bar(modes, accs, color=["#4C72B0", "#DD8452"])
for bar, acc in zip(bars, accs):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, f"{acc:.1f}%", ha="center")
plt.ylabel("准确率 (%)")
plt.title("HyDE vs 原始检索准确率对比")
plt.ylim(0, 110)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.savefig("benchmarks/hyde_comparison.png", dpi=150)
print("图表已保存: benchmarks/hyde_comparison.png")
