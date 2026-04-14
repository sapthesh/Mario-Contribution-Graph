# 🍄 Ultimate Mario GitHub Contribution Graph

<!-- Tech Stack Badges -->
![Python](https://img.shields.io/badge/python-3.x-blue.svg?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)
![SVG](https://img.shields.io/badge/SVG-Dynamic_Animation-ffb000?style=for-the-badge&logo=svg&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

<!-- Workflow Status Badge (Replace YOUR_USERNAME and YOUR_REPO_NAME) -->
[![Generate Mario Contribution Graph](https://img.shields.io/github/actions/workflow/status/sapthesh/Mario-Contribution-Graph/mario-graph.yml?style=for-the-badge&label=Build%20Status)](https://github.com/sapthesh/Mario-Contribution-Graph/actions)
<a href="https://hits.sh/github.com/sapthesh/Mario-Contribution-Graph/"><img alt="Hits" src="https://hits.sh/github.com/sapthesh/Mario-Contribution-Graph.svg?view=today-total&style=for-the-badge&color=fe7d37"/></a>


Turn your GitHub contribution graph into a living, breathing 8-bit Mario game level! 

This project uses a Python script and GitHub Actions to fetch your real commit history and dynamically generate an animated SVG. It calculates the height of your contribution blocks and mathematically paths Mario to parkour over your commits, collect coins, and finish the level!

### 🌟 Features
* 🏃‍♂️ **Dynamic Parkour Physics:** Mario calculates jumps based on your commit history. If you have a gap, he drops to the ground; if you have a huge streak, he jumps across the top!
* 🪙 **Interactive Coins:** Mario collects glowing, spinning coins over your most active (Level 4) contribution days. The coins instantly pop and fade when he touches them.
* 🏰 **Classic Level Design:** Mario rises out of a Warp Pipe on the left, parkours across your year of code, slides down a Flagpole on the right, and walks into a Castle with a flashing "LEVEL CLEAR!" sign.
* ☁️ **Parallax Scenery:** 8-bit clouds drift infinitely through the background sky.
* 🛡️ **Bypasses GitHub Camo:** 100% Pure SVG Pixel Art. No external `.png` or `.gif` files are used, meaning GitHub's strict image security cannot block it!

---

## 🚀 See it in Action

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="mario_contribution.svg?v=1">
  <img alt="Mario Contribution Graph" src="mario_contribution.svg?v=1">
</picture>

*(Updates automatically every day at midnight!)*

---

## 🛠️ How to Add This to Your Own Profile

Want this on your GitHub profile? Follow these exact steps to set it up in less than 5 minutes.

### Step 1: Create the Python Script
1. In your repository, create a new file named `generate_mario.py` in the root directory.
2. Copy the Python script from this repository and paste it into your new file.
3. Commit the file.

### Step 2: Create the GitHub Actions Workflow
1. In your repository, create a new file at this exact path: `.github/workflows/mario-graph.yml`.
2. Paste the following code into the file:

```yaml
name: Generate Mario Contribution Graph

on:
  schedule:
    - cron: "0 0 * * *" # Runs daily at midnight
  workflow_dispatch:    # Allows you to run it manually

jobs:
  build:
    runs-on: ubuntu-latest
    
    # Grants the bot permission to push the SVG back to your repo
    permissions:
      contents: write
      
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Generate Mario SVG
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GITHUB_ACTOR: ${{ github.repository_owner }}
        run: python generate_mario.py

      - name: Commit and Push SVG
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add mario_contribution.svg
          git commit -m "Update Mario contribution graph" || echo "No changes to commit"
          git push
```

### Step 3: Grant GitHub Actions Permissions
By default, GitHub Actions cannot write new files to your repository. You must enable this:
1. Go to your repository **Settings**.
2. Click on **Actions** > **General** in the left sidebar.
3. Scroll down to the **Workflow permissions** section.
4. Select **Read and write permissions**.
5. Click **Save**.

### Step 4: Run the Action Manually
Generate your first image immediately without waiting for midnight:
1. Go to the **Actions** tab at the top of your repository.
2. Click on **Generate Mario Contribution Graph** on the left side.
3. Click the **Run workflow** dropdown on the right, and click the green **Run workflow** button.
4. Wait about 15 seconds for it to finish and turn green!

### Step 5: Display it on your Profile!
Once the action finishes, a file named `mario_contribution.svg` will be added to your repository. 

To display it, edit your `README.md` and paste this code wherever you want the animation to appear:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="mario_contribution.svg?v=1">
  <img alt="Mario Contribution Graph" src="mario_contribution.svg?v=1">
</picture>
```
*(Note: The `?v=1` at the end of the URL helps bypass GitHub's aggressive image caching so you always see the latest version!)*

---

## 🎨 Customization
If you want to tweak the game, open `generate_mario.py` and look for the variables at the top of the `generate_mario_github_svg` function. You can easily adjust the `mario_scale`, animation speed (`dur="20s"`), or change the CSS colors to match different themes!
