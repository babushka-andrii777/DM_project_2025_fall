import glob
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


def process_experiment_file(experiments_data):
    total_time = 0.0
    vertex_count = 0
    density_val = 0.0
    metadata_captured = False

    with open(experiments_data, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        if not line.strip(): continue
        parts = line.split(',')
        if len(parts) < 4: continue

        try:
            time_part = parts[0].split(':')[-1].strip()
            total_time += float(time_part)
        except ValueError:
            pass

        if not metadata_captured:
            try:
                vertex_part = parts[2].split(':')[-1].strip()
                vertex_count = int(vertex_part)
                density_part = parts[3].split(':')[-1].strip()
                density_val = float(density_part)
                metadata_captured = True
            except (ValueError, IndexError):
                pass

    return total_time, vertex_count, density_val


files = glob.glob("experiments_data*.txt")
all_results = []

for experiments_data in files:
    try:
        t_time, v_count, d_val = process_experiment_file(experiments_data)
        avg_time = t_time / 20 if t_time > 0 else 0

        all_results.append({
            'filename': experiments_data,
            'avg_time': avg_time,
            'vertexes': v_count,
            'density': d_val
        })
    except Exception:
        pass


unique_densities = sorted(list(set(r['density'] for r in all_results)))
plt.style.use('dark_background')

for target_density in unique_densities:

    group_data = [r for r in all_results if r['density'] == target_density]
    group_data.sort(key=lambda x: x['vertexes'])

    if not group_data: continue

    x_vals = [r['vertexes'] for r in group_data]
    y_time = [r['avg_time'] for r in group_data]


    fig, ax = plt.subplots(figsize=(12, 6))

    fig.canvas.manager.set_window_title(f'Analysis for Density {target_density}')
    plt.title(f'Time vs Vertex Count (Fixed Density: {target_density})')

    ax.plot(x_vals, y_time, color='#ffcf60', linewidth=2, marker='o', markersize=6, label='Avg Time')

    ax.set_xlabel('Number of Vertexes')
    ax.set_ylabel('Average Time (seconds)', color='#ffcf60')
    ax.tick_params(axis='y', labelcolor='#ffcf60')


    y_ticks = [y_time[0]]
    for i in range(1, 6):
        y_ticks.append(y_time[0] + (y_time[-1] - y_time[0]) / 6 * i)
    y_ticks.append(y_time[-1])
    ax.set_yticks(y_ticks)

    ax.set_xticks(x_vals)
    ax.legend(loc='upper left', frameon=False)
    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()

    print(f"Показую графік для густини {target_density}...")
    plt.show()

print("Всі графіки показано.")
