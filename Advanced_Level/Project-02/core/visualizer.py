"""
core/visualizer.py
Stats dashboard and chart generation using Matplotlib.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from datetime import datetime
from config   import Config
from core.database import FaceDatabase

DARK   = '#0d1117'
GRID   = '#21262d'
TEXT   = '#c9d1d9'
GREEN  = '#3fb950'
BLUE   = '#58a6ff'
ORANGE = '#d29922'
RED    = '#f85149'


class Visualizer:
    def __init__(self, cfg: Config):
        self.cfg = cfg
        plt.style.use('dark_background')

    def show_stats(self, db: FaceDatabase):
        stats   = db.get_recognition_stats()
        persons = db.list_persons()

        print(f"\n{'='*55}")
        print(f"  📊 System Statistics")
        print(f"{'='*55}")
        print(f"  Registered Persons   : {stats['registered_persons']}")
        print(f"  Total Recognitions   : {stats['total_recognitions']}")
        print(f"  Known Recognitions   : {stats['known_recognitions']}")
        print(f"  Unknown Detections   : {stats['unknown_recognitions']}")
        print(f"  Spoof Attempts       : {stats['spoof_attempts']}")
        print(f"\n  👥 Registered Persons:")
        for p in persons:
            print(f"     {p['label']:>3}. {p['name']:<25} {p['sample_count']} samples")
        print(f"\n  🏆 Top Recognized:")
        for t in stats['top_persons']:
            print(f"     {t['name']:<25} {t['count']} times")
        print(f"\n  🕐 Recent Events:")
        for r in stats['recent_events'][:5]:
            print(f"     {r['name']:<20} {r['confidence']:.1f}%  {r['time'][:19]}")
        print(f"{'='*55}\n")

        if stats['total_recognitions'] > 0:
            self._plot_stats(stats)

    def _plot_stats(self, stats: dict):
        fig = plt.figure(figsize=(16, 10), facecolor=DARK)
        gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

        # ── 1. Known vs Unknown Pie ────────────────────────────────
        ax1 = fig.add_subplot(gs[0, 0])
        ax1.set_facecolor(DARK)
        vals   = [stats['known_recognitions'], stats['unknown_recognitions'],
                  stats['spoof_attempts']]
        labels = ['Known', 'Unknown', 'Spoof']
        colors = [GREEN, ORANGE, RED]
        wedges, texts, autotexts = ax1.pie(
            vals, labels=labels, colors=colors,
            autopct='%1.1f%%', startangle=140,
            textprops={'color': TEXT, 'fontsize': 10}
        )
        for at in autotexts:
            at.set_color(DARK)
            at.set_fontweight('bold')
        ax1.set_title('Recognition Distribution', color=TEXT,
                      fontsize=12, fontweight='bold')

        # ── 2. Top Persons Bar ─────────────────────────────────────
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.set_facecolor(DARK)
        ax2.spines[:].set_color(GRID)
        ax2.tick_params(colors=TEXT)
        if stats['top_persons']:
            names  = [t['name'] for t in stats['top_persons']]
            counts = [t['count'] for t in stats['top_persons']]
            bars   = ax2.barh(names, counts, color=BLUE, alpha=0.85)
            for bar, cnt in zip(bars, counts):
                ax2.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                         str(cnt), va='center', color=TEXT, fontsize=9)
        ax2.set_title('Top Recognized Persons', color=TEXT,
                      fontsize=12, fontweight='bold')
        ax2.set_xlabel('Recognition Count', color=TEXT)

        # ── 3. KPI Cards ──────────────────────────────────────────
        ax3 = fig.add_subplot(gs[1, :])
        ax3.set_facecolor(DARK)
        ax3.axis('off')
        kpis = [
            ("Total\nRecognitions",   str(stats['total_recognitions']),  BLUE),
            ("Known\nRecognitions",   str(stats['known_recognitions']),  GREEN),
            ("Unknown\nDetections",   str(stats['unknown_recognitions']),ORANGE),
            ("Spoof\nAttempts",       str(stats['spoof_attempts']),      RED),
            ("Registered\nPersons",   str(stats['registered_persons']),  BLUE),
        ]
        for i, (label, value, color) in enumerate(kpis):
            x  = 0.05 + i * 0.19
            ax3.add_patch(plt.FancyBboxPatch(
                (x, 0.1), 0.16, 0.8,
                boxstyle="round,pad=0.02",
                facecolor=GRID, edgecolor=color, linewidth=2,
                transform=ax3.transAxes
            ))
            ax3.text(x + 0.08, 0.65, value, ha='center', va='center',
                     fontsize=20, fontweight='bold', color=color,
                     transform=ax3.transAxes)
            ax3.text(x + 0.08, 0.25, label, ha='center', va='center',
                     fontsize=8, color=TEXT, transform=ax3.transAxes)

        fig.suptitle("Facial Recognition System — Dashboard",
                     color=TEXT, fontsize=16, fontweight='bold', y=1.01)

        out = os.path.join(self.cfg.output_dir,
                           f"stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
        fig.savefig(out, dpi=130, bbox_inches='tight',
                    facecolor=DARK, edgecolor='none')
        plt.close(fig)
        print(f"   📊 Stats chart saved → {out}")