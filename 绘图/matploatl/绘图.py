import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams["font.sans-serif"]=["simhei"]
matplotlib.rcParams["font.family"]="sans-serif"

plt.bar([1],[100],label="java")
plt.bar([2],[80],label="c")
plt.bar([3],[70],label="c#")
plt.bar([4],[60],label="python")

plt.legend()
plt.savefig("PragramSort.png")
plt.show()