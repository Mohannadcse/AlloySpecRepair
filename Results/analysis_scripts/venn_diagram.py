import matplotlib.pyplot as plt
from venn.pyvenn.venn import venn5, get_labels
from matplotlib_venn import venn2


# Define colors for the sets
default_colors = [
    [92 / 255.0, 192 / 255.0, 98 / 255.0, 0.5],  # Arepair
    [90 / 255.0, 155 / 255.0, 212 / 255.0, 0.5],  # ICEBAR
    [246 / 255.0, 236 / 255.0, 86 / 255.0, 0.6],  # BeAFix
    [241 / 255.0, 90 / 255.0, 96 / 255.0, 0.4],  # ATR
    [255 / 255.0, 117 / 255.0, 0 / 255.0, 0.3],  # Setting-1
]

benchmark = {
    "addr",
    "arr-1",
    "arr-2",
    "balancedBST-1",
    "balancedBST-2",
    "balancedBST-3",
    "bempl",
    "cd-1",
    "cd-2",
    "ctree",
    "dll-1",
    "dll-2",
    "dll-3",
    "dll-4",
    "farmer",
    "fsm-1",
    "fsm-2",
    "grade",
    "other",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
    "student-9",
    "student-10",
    "student-11",
    "student-12",
    "student-13",
    "student-14",
    "student-15",
    "student-16",
    "student-17",
    "student-18",
    "student-19",
}

a_repair = {
    "addr",
    "arr-1",
    "arr-2",
    "balancedBST-1",
    "ctree",
    "fsm-1",
    "fsm-2",
    "student-1",
    "student-2",
}
icebar = {
    "addr",
    "arr-1",
    "arr-2",
    "balancedBST-1",
    "balancedBST-2",
    "bempl",
    "cd-1",
    "cd-2",
    "dll-1",
    "dll-2",
    "dll-3",
    "fsm-1",
    "fsm-2",
    "grade",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
}
beafix = {
    "addr",
    "arr-1",
    "arr-2",
    "balancedBST-1",
    "cd-1",
    "cd-2",
    "dll-1",
    "dll-2",
    "dll-3",
    "fsm-1",
    "other",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
    "student-9",
    "student-10",
    "student-11",
    "student-12",
    "student-13",
}
atr = {
    "addr",
    "arr-1",
    "balancedBST-1",
    "bempl",
    "cd-1",
    "cd-2",
    "dll-1",
    "dll-2",
    "fsm-1",
    "fsm-2",
    "grade",
    "other",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
    "student-9",
    "student-10",
}

# Settings
setting_1 = {
    "balancedBST-1",
    "cd-1",
    "ctree",
    "dll-1",
    "dll-2",
    "dll-3",
    "dll-4",
    "farmer",
    "fsm-1",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
}

# Setting-2
setting_2 = {
    "balancedBST-1",
    "cd-1",
    "cd-2",
    "ctree",
    "dll-1",
    "dll-2",
    "dll-3",
    "dll-4",
    "farmer",
    "fsm-1",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
}

# Setting-3
setting_3 = {
    "addr",
    "balancedBST-1",
    "balancedBST-2",
    "cd-1",
    "cd-2",
    "ctree",
    "dll-1",
    "dll-2",
    "farmer",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
}

# Setting-4
setting_4 = {
    "arr-1",
    "balancedBST-1",
    "bempl",
    "cd-1",
    "cd-2",
    "ctree",
    "dll-1",
    "dll-2",
    "farmer",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
}

# Setting-5
setting_5 = {
    "addr",
    "balancedBST-1",
    "bempl",
    "cd-1",
    "ctree",
    "dll-1",
    "dll-2",
    "farmer",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
    "student-9",
    "student-10",
    "student-11",
}

# Setting-6
setting_6 = {
    "arr-1",
    "addr",
    "balancedBST-1",
    "bempl",
    "cd-1",
    "cd-2",
    "ctree",
    "dll-1",
    "dll-2",
    "dll-3",
    "dll-4",
    "farmer",
    "fsm-1",
    "grade",
    "other",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
    "student-9",
    "student-10",
    "student-11",
    "student-12",
    "student-13",
}

chatgpt = {
    "arr-1",
    "balancedBST-1",
    "balancedBST-2",
    "bempl",
    "cd-1",
    "cd-2",
    "ctree",
    "dll-1",
    "dll-2",
    "dll-3",
    "grade",
    "student-1",
    "student-2",
    "student-3",
    "student-4",
    "student-5",
    "student-6",
    "student-7",
    "student-8",
    "student-9",
    "student-10",
    "student-11",
    "student-12",
    "student-13",
    "student-14",
    "student-15",
}

# List of settings for iteration
settings = [setting_1, setting_2, setting_3, setting_4, setting_5, setting_6]
setting_names = [
    "Setting-1",
    "Setting-2",
    "Setting-3",
    "Setting-4",
    "Setting-5",
    "Setting-6",
]

default_fontsize = 16  # Increase this value as needed

# print(f"Length of Arepair: {len(a_repair)}")
# print(f"Length of ICEBAR: {len(icebar)}")
# print(f"Length of BeAFix: {len(beafix)}")
# print(f"Length of ATR: {len(atr)}")
# print(f"Length of Setting-1: {len(setting_1)}")
# print(f"Length of Setting-2: {len(setting_2)}")
# print(f"Length of Setting-3: {len(setting_3)}")
# print(f"Length of Setting-4: {len(setting_4)}")
# print(f"Length of Setting-5: {len(setting_5)}")
# print(f"Length of Setting-6: {len(setting_6)}")
# print(f"Length of chatgpt: {len(chatgpt)}")


# Modify the function definitions to accept and use a fontsize parameter
# Example modification for a custom text drawing function
def draw_text(
    fig,
    ax,
    x,
    y,
    text,
    color=[0, 0, 0, 1],
    fontsize=default_fontsize,
    ha="center",
    va="center",
):
    ax.text(
        x,
        y,
        text,
        horizontalalignment=ha,
        verticalalignment=va,
        fontsize=fontsize,
        color="black",
    )


# Ensure when calling venn5 or similar functions, fontsize is either set directly or passed through
# Example adjusted loop for generating and saving Venn diagrams with increased font size
for i, (setting, setting_name) in enumerate(zip(settings, setting_names), start=1):
    data = [a_repair, icebar, beafix, atr, setting]
    labels = get_labels(data, fill=["number"])
    names = ["Arepair", "ICEBAR", "BeAFix", "ATR", setting_name]
    fig, ax = venn5(
        labels, names, colors=default_colors, fontsize=default_fontsize
    )  # Pass fontsize here if the function supports it

    pdf_filename = f"venn_diagram_{setting_name}.pdf"
    plt.savefig(pdf_filename, bbox_inches="tight")
    plt.close(fig)


# Create a Venn2 diagram
plt.figure(figsize=(10, 8))
venn = venn2([setting_6, chatgpt], set_labels=("Setting-6", "ChatGPT"))

# Adjusting font sizes for labels and subset numbers
for text in venn.set_labels:
    text.set_fontsize(14)
for text in venn.subset_labels:
    if text:
        text.set_fontsize(14)

pdf_filename = "venn_diagram_setting_6_chatgpt.pdf"
plt.savefig(pdf_filename, bbox_inches="tight")
plt.show()
