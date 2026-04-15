<div align="center">
  
  # 🍄 Ultimate Mario GitHub Contribution Graph 🍄

<!-- Tech Stack Badges -->
![Python](https://img.shields.io/badge/python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![SVG](https://img.shields.io/badge/SVG-Dynamic_Animation-ffb000?style=for-the-badge&logo=svg&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

<!-- Workflow & Social Badges -->
[![Generate Mario Contribution Graph](https://img.shields.io/github/actions/workflow/status/sapthesh/Mario-Contribution-Graph/mario-graph.yml?style=for-the-badge&label=Build%20Status)](https://github.com/sapthesh/Mario-Contribution-Graph/actions)
<a href="https://hits.sh/github.com/sapthesh/Mario-Contribution-Graph/"><img alt="Hits" src="https://hits.sh/github.com/sapthesh/Mario-Contribution-Graph.svg?view=today-total&style=for-the-badge&color=fe7d37"/></a>

---

### 🎮 Turn your GitHub contribution graph into a living, breathing 8-bit Mario level! 

This project uses a Python script and GitHub Actions to fetch your real-time commit history via the GitHub GraphQL API. It then mathematically calculates a parkour path for Mario to jump across your commits, collect coins, and finish the level in style.

[**Explore the Wiki**](https://github.com/sapthesh/Mario-Contribution-Graph/wiki) • [**Report a Bug**](https://github.com/sapthesh/Mario-Contribution-Graph/issues) • [**Security Policy**](https://github.com/sapthesh/Mario-Contribution-Graph/blob/main/SECURITY.md)

</div>

---

## 🚀 See it in Action

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="mario_contribution.svg?v=1">
  <img alt="Mario Contribution Graph" src="mario_contribution.svg?v=1" width="100%">
</picture>

---

## 🌟 Key Features

| Feature | Description |
|---|---|
| 🏃‍♂️ **Parkour Physics** | Mario doesn't just run; he jumps! The script calculates the "peak" of your contributions and paths Mario to hop on top of them. |
| 🪙 **Coin Collection** | Your busiest days (Level 4) spawn spinning coins. Mario "collects" them with pixel-perfect timing as he runs by. |
| 🚩 **Interactive Finish** | Mario rises from a Warp Pipe, parkours across your year, slides down the Flagpole, and enters a Castle to trigger a "LEVEL CLEAR!" |
| ☁️ **Parallax World** | Includes a sky-blue background with drifting clouds and ground bushes for a true 8-bit aesthetic. |
| 🛡️ **Zero-Asset SVG** | 100% Pure SVG code. No external images are used, bypassing all GitHub security proxies (Camo) for instant loading. |

---

## 🛠️ Step-by-Step Setup Guide

Follow these steps to add this animation to your own GitHub profile in minutes.

### 1. Create the Script
In your repository, create a file named `generate_mario.py` and paste the Python code found in this repo.

### 2. Set Up the Automation
Create a file at `.github/workflows/mario-graph.yml` and paste the following:

```yaml
name: Generate Mario Contribution Graph

on:
  schedule:
    - cron: "0 0 * * *" # Runs daily at midnight
  workflow_dispatch:    # Allows manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.x'
      - name: Generate Mario SVG
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_ACTOR: ${{ github.repository_owner }}
        run: python generate_mario.py
      - name: Push SVG
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add mario_contribution.svg
          git commit -m "Update Mario graph" || echo "No changes"
          git push
```

### 3. Grant Permissions
1. Go to **Settings** > **Actions** > **General**.
2. Scroll to **Workflow permissions**.
3. Select **Read and write permissions** and click **Save**.

### 4. Trigger the First Run
Go to the **Actions** tab, select the workflow, and click **Run workflow**. Once finished, the `mario_contribution.svg` file will appear in your repo.

---

## 🖼️ How to Show it on Your Profile

To add the animation to your personal profile `README.md`, use the following code (replace `YOUR_USERNAME` and `YOUR_REPO`):

```html
<div align="center">
  <a href="https://github.com/YOUR_USERNAME/YOUR_REPO">
    <img src="https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/mario_contribution.svg?v=1" width="100%" />
  </a>
</div>
```

---

## 🎨 Customization

Want to tweak the game? Open `generate_mario.py` to adjust:
* **Speed:** Change `animation_duration` (Default is 20s).
* **Character:** Edit the `mario_pixels` array to draw Luigi or your own custom character!
* **Theme:** Modify the CSS in the `svg_elements` list to change the sky or ground colors.

---

## 🤝 Contributing & Support

If you love this project, please consider giving it a ⭐ **Star**! 

For technical details on the pathfinding math or sprite generation, check out the [**Project Wiki**](https://github.com/sapthesh/Mario-Contribution-Graph/wiki). 

---

<div align="center">
  Made with ❤️ and 🍄 by <a href="https://github.com/sapthesh">sapthesh</a>
</div>
