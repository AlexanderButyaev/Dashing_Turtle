from pathlib import Path
import math

import numpy as np
import pandas as pd

import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg

from contextlib import contextmanager


@contextmanager
def _mpl_context(params: dict | None = None):
    with matplotlib.rc_context(rc=params or {}):
        yield


def _ensure_dir(p: str | Path) -> Path:
    p = Path(p)
    p.mkdir(parents=True, exist_ok=True)
    return p


def plot_modification(
    mods,
    dir_name: str = "Default",
    save_path: str = "./",
    mod_type: str = "Modifications",
    seq_name: str = "Sequence",
):
    #### deprecated ####
    return
    ##### get positions and mods ############
    # ----- data prep (no pyplot) -----
    modifications = np.asarray(mods, dtype=int)
    positions = modifications[:, 0].tolist()
    # ALBU: I assume the second column is counts
    counts = modifications[:, 1].tolist()

    # keep only counts > 1
    idx = [i for i, n in enumerate(counts) if n > 1]
    positions = [positions[i] for i in idx]
    counts = [counts[i] for i in idx]

    positions_size = 50
    num_plots = math.floor(len(positions) / positions_size)

    # ----- color selection -----
    bar_color = "b"
    if mod_type == "Deletions":
        bar_color = "r"
    elif mod_type == "Insertions":
        bar_color = "g"

    # ----- figure length -----
    figlen = len(counts) * 0.3
    if figlen < 6.4:
        figlen = 6.4
    elif figlen > 100:
        figlen = 100

    # fig.set_figwidth(10)

    # ----- output dir -----
    outdir = Path(save_path) / f"{dir_name}_Modification_Plots"
    outdir.mkdir(parents=True, exist_ok=True)

    outputs = []
    curr_pos = 0
    with _mpl_context({"font.size": 20}):
        for i in range(num_plots):
            mod_pos = np.array(positions[curr_pos : curr_pos + positions_size])
            mod_num = np.array(counts[curr_pos : curr_pos + positions_size])

            df = pd.DataFrame(
                {
                    "Reference Nucleotide Position": mod_pos,
                    "Number of Modifications": mod_num,
                }
            )

            # isolated Agg figure/canvas
            fig = Figure(figsize=(figlen, 10), dpi=100)
            FigureCanvasAgg(fig)  # attach Agg renderer
            ax = fig.add_subplot(111)

            df.plot.bar(
                x="Reference Nucleotide Position",
                y="Number of Modifications",
                rot=90,
                ax=ax,
                color=bar_color,
                xlabel="Reference Nucleotide Position",
                ylabel=f"Number of {mod_type}",
                title=f"{seq_name} {mod_type}",
                legend=False,
            )

            #### OLD plot modifications (just for idea - don't use) #####
            # fig, ax = plt.figure(figsize=(figlen, 4.8)) #6.4, 4.8 default size
            # fig, ax = plt.subplots(num_plots)
            # fig.set_size_inches(10, 50)
            # fig.set_figheight(figlen)
            # fig.suptitle(seq_name +' '+ dir_name +' ' + mod_type, fontsize="xx-large")

            fig.tight_layout()

            figname = outdir / f"{seq_name}_{mod_type}_{i}.png"
            fig.savefig(figname, bbox_inches="tight")
            outputs.append(str(figname.resolve()))

            curr_pos += positions_size

    return outputs


def plot_modification_summary(
    mods,
    dir_name: str = "Default",
    save_path: str | Path = "./",
    mod_type: str = "Modification Summary",
    seq_name: str = "Sequence",
):
    ##### deprecated for now #########
    return
    # ----- data prep -----
    modifications = np.asarray(mods, dtype=int)
    positions = modifications[:, 0].tolist()

    # Safe norm (avoid divide-by-zero)
    def _safe_norm(v: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(v)
        return (v / n) if n > 0 else np.zeros_like(v, dtype=float)

    dels = _safe_norm(modifications[:, 1]).tolist()
    ins = _safe_norm(modifications[:, 2]).tolist()
    mismatch = _safe_norm(modifications[:, 3]).tolist()

    positions_size = 50
    num_plots = math.floor(len(positions) / positions_size)

    # ----- figure length -----
    figlen = len(mods) * 0.3
    if figlen < 6.4:
        figlen = 6.4
    elif figlen > 6.4:
        figlen = 30

    # ----- output dir -----
    outdir = Path(save_path) / f"{dir_name}_Modification_Plots"
    outdir.mkdir(parents=True, exist_ok=True)

    outputs: list[str] = []
    curr_pos = 0

    with _mpl_context({"font.size": 20}):
        for i in range(num_plots):
            mod_pos = np.array(positions[curr_pos : curr_pos + positions_size])
            mod_del = np.array(dels[curr_pos : curr_pos + positions_size])
            mod_ins = np.array(ins[curr_pos : curr_pos + positions_size])
            mod_mis = np.array(mismatch[curr_pos : curr_pos + positions_size])

            df = pd.DataFrame(
                {
                    "Reference Nucleotide Position": mod_pos,
                    "Deletions": mod_del,
                    "Insertions": mod_ins,
                    "Mismatches": mod_mis,
                }
            )

            # isolated Agg figure/canvas
            fig = Figure(figsize=(figlen, 10), dpi=100)
            FigureCanvasAgg(fig)  # attach Agg renderer
            ax = fig.add_subplot(111)

            df.plot.bar(
                x="Reference Nucleotide Position",
                rot=90,
                ax=ax,
                xlabel="Reference Nucleotide Position",
                ylabel=f"Number of {mod_type}",
                title=f"{seq_name} {mod_type}",
                legend=True,
                ylim=(0, 0.01),
            )

            fig.tight_layout()

            figname = outdir / f"{seq_name}_{mod_type}_{i}.png"
            fig.savefig(figname, bbox_inches="tight")
            outputs.append(str(figname.resolve()))

            curr_pos += positions_size

    return outputs

    # #### plot modifications #####
    # fig = plt.figure(figsize=(figlen, 4.8)) #6.4, 4.8 default size
    # ax = fig.add_axes([.1, .2, .8, .7])
    # ax.margins(.005, .5)
    # ax.set_xticks(range(0, len(positions)))
    # ax.set_xticklabels(positions)
    # ax.tick_params(direction='out', length=6, rotation=90)
    # ax.set_xlabel('Reference Nucleotide Position', fontsize="xx-large")
    # ax.set_ylabel('Number of ' + mod_type, fontsize="xx-large")
    # ax.set_title(seq_name +' '+ dir_name +' ' + mod_type, fontsize="xx-large")
    # ax.grid(axis='y')
    # # proper ticks
    # X = np.arange(len(mods))
    # ax.plot(X, dels, color='r', label="Deletions")
    # #ax.bar_label(pps, label_type='edge')
    # ax.plot(X, ins, color='g', label="Insertions")
    # ax.plot(X, mismatch, color='b', label="Mismatches")
    # ax.legend()
    # fig = plt.gcf()
    # dir_name = save_path + dir_name + '_Modification_Plots'
    # if not os.path.exists(dir_name):
    #     os.makedirs(dir_name)
    # figname = os.path.join(dir_name + '/' + seq_name + '_' + mod_type + '.png')
    # fig.savefig(figname)
    # plt.tight_layout()
    # #plt.show)


def plot_mismatch(
    mismatches,
    seq_name: str = "Sequence",
    dir_name: str = "Default",
    save_path: str = "./",
    mod_type: str = "Mismatched Bases",
):
    #### deprecated for now ####
    return
    ##### get positions and mods ############
    # ----- data prep (no pyplot) -----
    data = np.asarray(mismatches)
    positions = data[:, 0].tolist()
    num_mismatch = data[:, 1].astype(float).tolist()
    nuc_mismatch = data[:, 2].tolist()
    ref_seq_label = data[:, 3].tolist()

    ref_label = [
        f"{positions[i]} {ref_seq_label[i]}" for i in range(len(ref_seq_label))
    ]

    print(seq_name)

    #### set figure length #####
    figlen = len(positions) * 0.3
    if figlen < 6.4:
        figlen = 6.4
    elif figlen > 100:
        figlen = 100

    # ----- output dir -----
    outdir = Path(save_path) / f"{dir_name}_Modification_Plots"
    outdir.mkdir(parents=True, exist_ok=True)

    # ----- render without pyplot/global backend -----
    with matplotlib.rc_context({"font.size": 20}):
        fig = Figure(figsize=(figlen, 6), dpi=100)
        FigureCanvasAgg(fig)  # attach Agg renderer
        ax = fig.add_axes([0.1, 0.2, 0.8, 0.7])

        ax.margins(0.005, 0.2)
        ax.set_xticks(range(len(positions)))
        ax.set_xticklabels(ref_label)
        ax.tick_params(direction="out", length=6, rotation=90)
        ax.set_xlabel("Reference Nucleotide Position", fontsize="xx-large")
        ax.set_ylabel(f"Number of {mod_type}", fontsize="xx-large")
        ax.set_title(f"{seq_name} {mod_type}", fontsize="xx-large")
        ax.grid(axis="y")

        X = np.arange(len(num_mismatch))
        bars = ax.bar(
            X,
            np.asarray(num_mismatch, dtype=float),
            color="b",
            align="center",
            edgecolor="black",
            width=0.2,
        )

        # Ensure labels length matches the bars length
        if len(nuc_mismatch) >= len(bars):
            labels = nuc_mismatch[: len(bars)]
        else:
            labels = nuc_mismatch + [""] * (len(bars) - len(nuc_mismatch))

        ax.bar_label(bars, labels, label_type="edge")

        figname = outdir / f"{seq_name}_Mismatched_Bases.png"
        fig.savefig(figname, bbox_inches="tight")

    return str(figname.resolve())


def plot_average_mod_rate(df, dir_name="Default", save_path="./"):
    print("plot_average_mod_rate")

    # --- Data prep ---
    df2 = df.drop(columns=["Condition"], errors="ignore")
    df2 = df2 * 100.0  # percent

    # --- Build figure without pyplot/global backend ---
    with _mpl_context({"font.size": 20}):
        fig = Figure(figsize=(12, 12), dpi=100)  # independent of GUI backend
        FigureCanvasAgg(fig)  # attach Agg renderer to this Figure
        ax = fig.add_subplot(111)

        # Use pandas plotting but direct it to our Axes (no pyplot)
        df2.plot(kind="bar", rot=30, title="Overall Modification Rates", ax=ax)

        fig.tight_layout()

        outdir = _ensure_dir(Path(save_path) / f"{dir_name}_Modification_Plots")
        figname = outdir / "Average_Modification_Rate.png"

        # Save via the Figure object (thread-safe)
        fig.savefig(figname, bbox_inches="tight")

    # Return absolute path for the GUI thread to load
    return str(figname.resolve())


def plot_average_mod_by_pos_rate(df, dir_name="Default", save_path="./"):
    print("plot_average_mod_by_pos_rate")

    # --- Data prep (no plotting side-effects) ---
    df2 = df * 100.0  # percent

    # x = df.values  # returns a numpy array
    # min_max_scaler = preprocessing.MinMaxScaler()
    # x_scaled = min_max_scaler.fit_transform(x)
    # df = pd.DataFrame(x_scaled)
    # df = df.iloc[:, :] * 100
    # --- Build figure without pyplot/global backend ---
    with _mpl_context({"font.size": 20}):
        fig = Figure(figsize=(12, 8), dpi=100)  # independent of GUI backend
        FigureCanvasAgg(fig)  # attach Agg renderer to this Figure
        ax = fig.add_subplot(111)
        df2.plot(
            kind="line",
            rot=45,
            title="Modification Rates by Position",
            ylim=(0, 100),
            color="purple",
            ax=ax,
        )

        fig.tight_layout()

        outdir = _ensure_dir(Path(save_path) / f"{dir_name}_Modification_Plots")
        figname = outdir / "Position_Modification_Rate.png"

        # Save via the Figure object (thread-safe)
        fig.savefig(figname, bbox_inches="tight")

    # Return absolute path for the GUI thread to load
    return str(figname.resolve())
