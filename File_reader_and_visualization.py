import glob

import matplotlib.pyplot as plt


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


unique_vertex_counts = sorted(list(set(r['vertexes'] for r in all_results)))

print(f"Знайдено груп за вершинами: {unique_vertex_counts}")

plt.style.use('dark_background')


for v_target in unique_vertex_counts:


    group_data = [r for r in all_results if r['vertexes'] == v_target]


    group_data.sort(key=lambda x: x['density'])


    x_labels = [f"{i + 1}" for i in range(len(group_data))]
    y_vertexes = [r['vertexes'] for r in group_data]  # Це буде пряма лінія
    y_density = [r['density'] * 100 for r in group_data]  # Густина x100
    y_time = [r['avg_time'] for r in group_data]


    fig, ax1 = plt.subplots(figsize=(14, 7))


    fig.canvas.manager.set_window_title(f'Analysis for {v_target} Vertexes')
    plt.title(f'Performance Analysis: Fixed {v_target} Vertexes (Sorted by Density)')


    line1, = ax1.plot(x_labels, y_vertexes, color='#a48eff', linewidth=2, linestyle='--',
                      label=f'Vertexes ({v_target})')


    line2, = ax1.plot(x_labels, y_density, color='#ff8ea4', linewidth=2, marker='o', markersize=4,
                      label='Density (x100)')

    ax1.set_xlabel('Experiments (Sorted by increasing Density)')
    ax1.set_ylabel('Count / Percentage', color='white')
    ax1.tick_params(axis='y', labelcolor='white')


    total_points = len(x_labels)
    if total_points > 20:
        step = total_points // 20 + 1
        ax1.set_xticks(range(0, total_points, step))
        ax1.set_xticklabels(x_labels[::step])
    else:
        ax1.set_xticks(range(len(x_labels)))
        ax1.set_xticklabels(x_labels)


    ax2 = ax1.twinx()

    line3, = ax2.plot(x_labels, y_time, color='#ffcf60', linewidth=3, label='Avg Time')

    ax2.set_ylabel('Time (seconds)', color='#ffcf60')
    ax2.tick_params(axis='y', labelcolor='#ffcf60')


    lines = [line1, line2, line3]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left', frameon=False)

    plt.grid(True, linestyle='--', alpha=0.2)
    plt.tight_layout()



    plt.show()

