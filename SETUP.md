# Self-Updating GitHub Profile README Setup

This directory contains everything needed for a self-updating GitHub profile README, inspired by [Simon Willison's approach](https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/).

## What It Does

Your profile README will automatically update every hour with:
- 📝 Recent blog posts from your Jekyll blog
- 🚀 Your latest GitHub repositories
- 💻 Your recent commits across all repos

## Setup Instructions

### 1. Create the Profile Repository

GitHub profile READMEs must be in a repository with the exact same name as your username:

```bash
# On GitHub, create a new repository named: jbwashington
# Initialize it with a README (or don't, we'll push ours)
```

### 2. Clone and Set Up the Repository

```bash
# Clone your new profile repo
cd ~/Developer
git clone https://github.com/jbwashington/jbwashington.git
cd jbwashington

# Copy all files from profile-readme directory
cp -r /Users/jbwashington/Developer/personal/jbwashington.github.io/profile-readme/* .
cp -r /Users/jbwashington/Developer/personal/jbwashington.github.io/profile-readme/.github .
```

### 3. Test Locally (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the build script
python build_readme.py

# Check that README.md was updated
cat README.md
```

### 4. Push to GitHub

```bash
git add .
git commit -m "Initial commit: self-updating profile README"
git push origin main  # or 'master' depending on your default branch
```

### 5. Enable GitHub Actions

1. Go to https://github.com/jbwashington/jbwashington
2. Click on the **Actions** tab
3. If prompted, enable GitHub Actions for the repository
4. The workflow will run automatically:
   - Every hour at 32 minutes past
   - On every push
   - Can be triggered manually via "Run workflow" button

### 6. Verify It Works

After a few minutes:
1. Check the **Actions** tab to see if the workflow ran successfully
2. Visit your profile: https://github.com/jbwashington
3. You should see your README with populated content!

## Customization

### Update the README Header

Edit `README.md` to customize:
- Your name and intro text
- Add links to social profiles
- Add skills, technologies, or other static content
- Keep the `<!-- marker starts/ends -->` comments intact!

### Modify Data Sources

Edit `build_readme.py` to:
- Change the number of items displayed (currently 5 each)
- Add new sections (TILs, projects, etc.)
- Change data sources or APIs

### Change Update Frequency

Edit `.github/workflows/build.yml`:
- `cron: '32 * * * *'` - Hourly at :32
- `cron: '0 0 * * *'` - Daily at midnight
- `cron: '0 */6 * * *'` - Every 6 hours

## Troubleshooting

### Blog posts not appearing?

- Verify your blog feed exists: https://jbwashington.github.io/feed.xml
- Check that the feed is valid XML
- Look at GitHub Actions logs for errors

### Rate limiting?

The script uses the `GITHUB_TOKEN` automatically provided by GitHub Actions, which has higher rate limits. If you run locally a lot, you may hit rate limits.

### Manual trigger?

Visit https://github.com/jbwashington/jbwashington/actions, click on "Build README" workflow, then click "Run workflow" button.

## Files Overview

```
jbwashington/                    # Your profile repo
├── README.md                    # The profile README (auto-updated)
├── build_readme.py             # Python script that updates README
├── requirements.txt             # Python dependencies
├── .github/
│   └── workflows/
│       └── build.yml           # GitHub Actions workflow
└── SETUP.md                    # This file (optional to keep)
```

## Learn More

- [GitHub Profile README Docs](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme)
- [Simon Willison's Original Article](https://simonwillison.net/2020/Jul/10/self-updating-profile-readme/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
