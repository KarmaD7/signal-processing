# Fourier级数的可视化 实验报告

2019011265 计93 丁韶峰

## 可视化逻辑分析

画出$2n+1$个圆，半径分别为 $Fourier$ 级数各项的系数，把 $nt$ 当作角度寻找圆上一点，通过该点与圆心连线的长度在y轴方向的投影表示正弦或余弦函数的值，并把该点当作下一个圆的圆心，最后一个点的纵坐标即为$g(t)$的值。

## 可视化方波系数

首先需要实现方波信号，直接将$f(t) =0.5sgn(\sin(t))+0.5$写入`square_wave`函数中即可，其中使用`numpy`的`sign`函数实现`sgn`。

之后先计算各项的 $Fourier$ 展开的系数，有
$$
a_0=\frac{1}{2\pi}\int_{0}^{\pi}1\mathrm{dt}=0.5 \\
a_n=\frac{1}{\pi}\int_{0}^{\pi}\cos nt \mathrm{dt}=0 \\
b_n=\frac{1}{\pi}\int_{0}^{\pi}\sin nt \mathrm{dt}= 
\left\{\begin{matrix}0，n为偶数\\ \frac{2}{n\pi}，n为奇数 \end{matrix}\right.
$$
将以上各项写入`fourier_coefficient`函数中即可。

此外，为了不运行一次就会将100张图片都显示出来，我将代码中的`plt.show()`注释掉了。

