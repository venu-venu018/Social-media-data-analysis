import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Sample social media data
data = {
    "Platform": [
        "Instagram", "Instagram", "Instagram",
        "Facebook", "Facebook", "Facebook",
        "X", "X",
        "LinkedIn", "LinkedIn"
    ],
    "Age": [20, 22, 26, 30, 35, 35, 24, 30, 28, 32],
    "Gender": [
        "Male", "Female", "Male",
        "Female", "Male", "Female",
        "Male", "Male",
        "Female", "Male"
    ],
    "Daily_Hours": [3, 5, 4, 2, 3, 2, 1, 1, 2, 2]
}

df = pd.DataFrame(data)

# Calculate statistics
platform_users = df["Platform"].value_counts()
gender_users = df["Gender"].value_counts()
daily_usage = df.groupby("Platform")["Daily_Hours"].mean()
average_age = df.groupby("Platform")["Age"].mean()

df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 18, 25, 35, 100],
    labels=["Under 18", "18-25", "26-35", "Above 35"]
)
age_groups = df["Age_Group"].value_counts().reindex(
    ["Under 18", "18-25", "26-35", "Above 35"]
)

# Dashboard colors
blue = "#17477D"
pink = "#E83E8C"
green = "#36AE55"
orange = "#FF9B26"
purple = "#A66BC5"
colors = [pink, "#287CE0", "#17191E", "#1675B9"]

# Create dashboard
fig = plt.figure(figsize=(16, 10), facecolor="#F4F8FC")
gs = fig.add_gridspec(
    3, 3,
    height_ratios=[0.65, 1.5, 1.5],
    hspace=0.18,
    wspace=0.12
)

# Header
ax_title = fig.add_subplot(gs[0, :])
ax_title.set_facecolor(blue)
ax_title.set_xticks([])
ax_title.set_yticks([])
for spine in ax_title.spines.values():
    spine.set_visible(False)

ax_title.text(
    0.5, 0.65, "Social Media Usage Analysis",
    ha="center", va="center",
    fontsize=25, fontweight="bold", color="white"
)
ax_title.text(
    0.5, 0.28,
    "Understanding How People in India Use Instagram, Facebook, X and LinkedIn",
    ha="center", va="center", fontsize=12, color="white"
)

# KPI cards
cards = [
    ("Total Users", str(len(df)), "#E7F4FC"),
    ("Average Daily Usage", f'{df["Daily_Hours"].mean():.1f} hours',
     "#F3E9FA"),
    ("Average Age", f'{df["Age"].mean():.1f} years', "#E3F5EC"),
    ("Most Used Platform", platform_users.idxmax(), "#FFF6DF")
]

for i, (label, value, color) in enumerate(cards):
    ax = fig.add_subplot(gs[0, i]) if False else None

# Add KPI cards below header using figure coordinates
for i, (label, value, color) in enumerate(cards):
    x = 0.035 + i * 0.24
    card = FancyBboxPatch(
        (x, 0.715), 0.22, 0.12,
        boxstyle="round,pad=0.01",
        transform=fig.transFigure,
        facecolor=color, edgecolor="none"
    )
    fig.patches.append(card)
    fig.text(x + 0.02, 0.795, label,
             fontsize=12, color=blue, weight="bold")
    fig.text(x + 0.02, 0.745, value,
             fontsize=19, color=blue, weight="bold")

# Helper for chart panels
def panel(ax, title):
    ax.set_facecolor("white")
    ax.set_title(title, loc="left", fontsize=13,
                 color=blue, fontweight="bold", pad=10)
    for spine in ax.spines.values():
        spine.set_edgecolor("#D7E8F8")
        spine.set_linewidth(1.3)
    ax.grid(axis="y", alpha=0.15)

# Platform-wise users
ax1 = fig.add_subplot(gs[1, 0])
panel(ax1, "Platform-wise Users")
platform_order = ["Instagram", "Facebook", "X", "LinkedIn"]
bars = ax1.bar(
    platform_order,
    [platform_users.get(p, 0) for p in platform_order],
    color=colors
)
ax1.set_ylabel("Number of Users")
ax1.set_ylim(0, 4.5)
ax1.bar_label(bars, padding=3, fontsize=11)
ax1.tick_params(axis="x", labelsize=9)

# Gender distribution
ax2 = fig.add_subplot(gs[1, 1])
panel(ax2, "Gender Distribution")
gender_order = ["Male", "Female"]
gender_values = [
    gender_users.get(g, 0) for g in gender_order
]
ax2.pie(
    gender_values,
    labels=None,
    autopct="%1.0f%%",
    startangle=90,
    colors=["#287CE0", pink],
    textprops={"fontsize": 12, "color": "white"}
)
ax2.legend(gender_order, loc="center left",
           bbox_to_anchor=(0.9, 0.5), frameon=False)

# Average daily usage
ax3 = fig.add_subplot(gs[1, 2])
panel(ax3, "Average Daily Usage (Hours)")
usage_values = [daily_usage.get(p, 0) for p in platform_order]
bars = ax3.bar(platform_order, usage_values, color=colors)
ax3.set_ylabel("Hours")
ax3.set_ylim(0, 5)
ax3.bar_label(bars, fmt="%.1f", padding=3, fontsize=11)
ax3.tick_params(axis="x", labelsize=9)

# Age group analysis
ax4 = fig.add_subplot(gs[2, 0])
panel(ax4, "Age Group Analysis")
age_order = ["Under 18", "18-25", "26-35", "Above 35"]
age_values = [age_groups.get(a, 0) for a in age_order]
bars = ax4.bar(
    age_order, age_values,
    color=[purple, green, orange, "#22B5B8"]
)
ax4.set_ylabel("Number of Users")
ax4.set_ylim(0, 5)
ax4.bar_label(bars, padding=3, fontsize=11)
ax4.tick_params(axis="x", labelsize=9)

# Platform-wise average age
ax5 = fig.add_subplot(gs[2, 1])
panel(ax5, "Platform-wise Average Age")
ax5.axis("off")

table_data = [
    [p, f"{average_age.get(p, 0):.1f}"]
    for p in platform_order
]
table = ax5.table(
    cellText=table_data,
    colLabels=["Platform", "Average Age"],
    cellLoc="center",
    loc="center",
    colWidths=[0.55, 0.45]
)
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 2.2)

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor("#D7E8F8")
    if row == 0:
        cell.set_facecolor("#E4F2FC")
        cell.set_text_props(weight="bold", color=blue)
    else:
        cell.set_facecolor("white")

# Key insights
ax6 = fig.add_subplot(gs[2, 2])
panel(ax6, "Key Insights")
ax6.axis("off")

male_percent = gender_users.get("Male", 0) / len(df) * 100
female_percent = gender_users.get("Female", 0) / len(df) * 100
most_used = platform_users.idxmax()
most_used_hours = daily_usage.idxmax()
oldest_platform = average_age.idxmax()

insights = [
    f"{most_used} has the highest number of users "
    f"({platform_users.max()} users).",
    f"Males: {male_percent:.0f}%, "
    f"Females: {female_percent:.0f}%.",
    f"The 18-25 age group has "
    f"{age_groups.get('18-25', 0)} users.",
    f"{most_used_hours} users spend the most time daily "
    f"({daily_usage.max():.1f} hours on average).",
    f"{oldest_platform} has the highest average age "
    f"({average_age.max():.0f} years)."
]

y = 0.88
for insight in insights:
    ax6.text(0.03, y, "✓", color=green,
             fontsize=14, fontweight="bold",
             transform=ax6.transAxes)
    ax6.text(0.12, y, insight, fontsize=9.5,
             color="#263746", wrap=True,
             transform=ax6.transAxes, va="center")
    y -= 0.18

fig.text(
    0.65, 0.025,
    "Note: These results are from sample data, "
    "not actual Indian user statistics.",
    fontsize=9, color="#536879", style="italic"
)

plt.subplots_adjust(
    left=0.04, right=0.97, top=0.95, bottom=0.07
)
plt.savefig("social_media_dashboard.png", dpi=200,
            bbox_inches="tight")
plt.show()
