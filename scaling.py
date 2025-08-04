import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator

# ==== Color and style configuration ====
color_config = {
    # five baseline bar colours  (ordered to minimise adjacent clashes)
    'baseline_colors': (
        '#3B5B92',   # arctic-blue
        '#4FA3B5',   # glacier-cyan
        '#8CA77B',   # moss-sage
        '#E1B168',   # muted-sand
        '#D46A6A'    # faded-crimson
    ),
    # accent line colour for “ours”
    'ours_line': '#750014',     # deep midnight-blue
    # figure background
    'background': 'white'
}

# ==== Font configuration ====
plt.rcParams.update({
    'font.family': 'Times New Roman',
    'font.size': 16,
    'axes.titlesize': 16,
    'axes.labelsize': 16,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'axes.facecolor': color_config['background']
})

# ==== Data ====
our_labels = ['Quality', 'Balanced', 'Medium', 'Fast', 'Turbo']
our_speedups = np.array([1.70, 1.92, 2.25, 2.91, 3.65])
our_lpips =     np.array([0.0417, 0.0436, 0.0655, 0.1353, 0.2239])

other_labels =  ['ToCa', 'DiTFastAttn2', 'TeaCache', 'SADA', 'TaylorSeer']
other_speedups = np.array([1.36, 1.42, 2.00, 2.02, 3.18])
other_lpips =    np.array([0.3469, 0.3430, 0.2160, 0.0600, 0.4259])

# ==== Annotation offsets ====
baseline_offsets = {
    'ToCa':         0.008,
    'DiTFastAttn2': -0.008,
    'TeaCache':      0.011,
    'SADA':         -0.005,
    'TaylorSeer':    0.000
}

ours_offsets = {
    'Quality':   0.015,
    'Balanced': -0.005,
    'Medium':    0.012,
    'Fast':      0.008,
    'Turbo':     0.015
}

# ==== Plot ====
fig, ax = plt.subplots(figsize=(8, 5))

bar_width = 0.18
for i, (x, lpips, label) in enumerate(zip(other_speedups, other_lpips, other_labels)):
    bar_color = color_config['baseline_colors'][i]          # base hue
    ax.bar(x, lpips, width=bar_width, color=bar_color, alpha=0.4)
    offset = baseline_offsets.get(label, 0.0)
    ax.text(x, lpips + offset, label, ha='center', va='bottom',
            color=bar_color, fontweight='bold')             # deeper label

# Our method line
x_line = np.concatenate(([1.0], our_speedups))
y_line = np.concatenate(([0.0], our_lpips))
ax.plot(x_line, y_line, marker='o', linestyle='-',
        color=color_config['ours_line'], linewidth=3)
ax.fill_between(x_line, y_line, alpha=0.2,
                color=color_config['ours_line'])

# Annotate our points
for x, lpips, label in zip(our_speedups, our_lpips, our_labels):
    offset = ours_offsets.get(label, 0.0)
    ax.text(x, lpips + offset, label, ha='center', va='bottom',
            fontweight='bold')

# Axes labels and title
ax.set_xlabel('Speedup (×)')
ax.set_ylabel('LPIPS ↓')

# Y-axis ticks at intervals of 0.1
ax.yaxis.set_major_locator(MultipleLocator(0.1))

# Grid and limits
ax.set_xlim(0.8, 3.8)
ax.set_ylim(0, 0.45)

# No legend requested
plt.tight_layout(pad=0.1)
plt.show()
