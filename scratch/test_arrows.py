import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

fig, ax = plt.subplots(figsize=(6, 2))
ax.axis('off')
ax.text(0.5, 0.5, "▲ +2.54%   ▼ -4.47%   - 0.00%", fontsize=18, ha='center', va='center',
        fontfamily='DejaVu Sans', color='#C00000')
out_path = 'scratch/test_arrows.png'
plt.savefig(out_path, bbox_inches='tight', dpi=150)
plt.close(fig)
print(f"Saved {out_path}, size: {os.path.getsize(out_path)}")
