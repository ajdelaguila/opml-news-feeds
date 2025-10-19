# Quick Reference Guide

## 🚀 Quick Start

### Local Build
```bash
# Make script executable (first time only)
chmod +x build.sh

# Build all bundles
./build.sh

# Validate only
./build.sh --validate-only

# Build without validation
./build.sh --build-only
```

### Using Python Directly
```bash
# Install dependencies
pip install -r requirements.txt

# Full build
python3 scripts/build_bundles.py

# Validate only
python3 scripts/build_bundles.py --validate-only

# Build only
python3 scripts/build_bundles.py --build-only
```

## 📦 Output

All bundles are created in `dist/`:
- `all-news-feeds.opml.xml` (138 feeds)
- `all-en-news-feeds.opml.xml` (78 feeds)
- `all-es-news-feeds.opml.xml` (32 feeds)
- `all-ro-news-feeds.opml.xml` (28 feeds)

## 🔄 Release Process

1. Make changes to OPML files or bundle configs
2. Test locally: `./build.sh`
3. Commit: `git commit -am "Update feeds"`
4. Push: `git push origin main`
5. GitHub Actions creates release automatically

## 📝 Adding Feeds

Edit the appropriate category file:
```xml
<outline text="Source Name" type="rss" xmlUrl="https://example.com/feed.xml"/>
```

**Remember:** Escape ampersands! Use `&amp;` not `&`

## 🎯 Creating Custom Bundles

Create `bundles/my-bundle.yaml`:
```yaml
name: "My Custom Bundle"
description: "Description here"
output: "my-bundle.opml.xml"
sources:
  - tech-en.opml.xml
  - science-en.opml.xml
```

Next build will include it!

## 🐛 Common Issues

**XML Parse Error?**
- Check for unescaped `&` characters
- Use `&amp;` in URLs and text

**Missing feeds in bundle?**
- Verify source file paths in bundle YAML
- Check that source files exist

**Build script fails?**
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python3 --version` (need 3.11+)

## 📊 Checking Results

```bash
# View dist directory
ls -lh dist/

# Count feeds in a bundle
grep 'type="rss"' dist/all-news-feeds.opml.xml | wc -l

# Validate an OPML file manually
python3 -c "import xml.etree.ElementTree as ET; ET.parse('dist/all-news-feeds.opml.xml')"
```

## 🔐 GitHub Actions

The workflow runs on every push to `main`:
- Location: `.github/workflows/build-and-release.yml`
- Triggers: Push to main, or manual dispatch
- Outputs: GitHub Release with bundles

View runs: `https://github.com/<owner>/<repo>/actions`

## 📋 File Locations

```
Project Root
├── bundles/              # Bundle configurations
├── scripts/              # Build scripts
├── dist/                 # Generated bundles (git-ignored)
├── *.opml.xml           # Source OPML files
├── build.sh             # Convenience build script
├── requirements.txt      # Python dependencies
└── .github/workflows/    # GitHub Actions
```
