# News Feed Collection

A curated collection of RSS/Atom news feeds organized by language, topic, and region.

## 📁 Repository Structure

```
news-feed/
├── bundles/              # Bundle configuration files
│   ├── all.yaml         # All feeds
│   ├── all-en.yaml      # English feeds only
│   ├── all-es.yaml      # Spanish feeds only
│   └── all-ro.yaml      # Romanian feeds only
├── scripts/             # Build and validation scripts
│   └── build_bundles.py # Main bundle builder script
├── *.opml.xml          # Individual feed collections by category
└── .github/workflows/   # Automated build and release
```

## 📰 Feed Categories

### Global & International
- **global-briefing.opml.xml** - Major international news sources

### Technology (English)
- **tech-en.opml.xml** - Tech blogs, engineering, AI/ML, cloud, security

### Science (English)
- **science-en.opml.xml** - Scientific publications and research

### Spanish Content
- **tech-es.opml.xml** - Spanish technology news
- **science-es.opml.xml** - Spanish science news
- **spain-free-first.opml.xml** - Spanish national news (free sources)
- **local-madrid.opml.xml** - Madrid local news
- **local-almeria.opml.xml** - Almería local news

### Romanian Content
- **tech-ro.opml.xml** - Romanian technology news
- **science-ro.opml.xml** - Romanian science news
- **romania-free-first.opml.xml** - Romanian national news (free sources)
- **local-bucharest.opml.xml** - Bucharest local news

### Sports
- **football-real-madrid.opml.xml** - Real Madrid and football news

## 🚀 Using the Feed Bundles

### Option 1: Download Pre-built Bundles (Recommended)

Go to the [Releases](../../releases) page and download the latest bundle:

- **all-news-feeds.opml.xml** - Complete collection (all languages)
- **all-en-news-feeds.opml.xml** - English feeds only
- **all-es-news-feeds.opml.xml** - Spanish feeds only
- **all-ro-news-feeds.opml.xml** - Romanian feeds only

### Option 2: Build Locally

```bash
# Install Python dependencies
pip install pyyaml

# Validate all OPML files
python scripts/build_bundles.py --validate-only

# Build all bundles
python scripts/build_bundles.py

# Output will be in the dist/ directory
```

## 🔧 Creating Custom Bundles

1. Create a new YAML file in the `bundles/` directory:

```yaml
name: "My Custom Bundle"
description: "Description of your bundle"
output: "my-bundle.opml.xml"
sources:
  - tech-en.opml.xml
  - science-en.opml.xml
```

2. Run the build script:

```bash
python scripts/build_bundles.py
```

3. Find your bundle in `dist/my-bundle.opml.xml`

## 🤖 Automated Releases

Every push to the `main` branch triggers an automated workflow that:

1. ✅ Validates all OPML files
2. 🔨 Builds all configured bundles
3. 📦 Creates a GitHub release with automatic versioning
4. 🚀 Publishes bundles as release artifacts

**Version Format:** `vYYYY.MM.DD-{git-hash}`

Example: `v2025.10.19-abc1234`

## 📝 Adding New Feeds

1. Add feeds to the appropriate category file (e.g., `tech-en.opml.xml`)
2. Update bundle configurations if needed
3. Commit and push to `main`
4. Automated workflow will validate and release

## 🛠️ Development

### Validate OPML Files

```bash
python scripts/build_bundles.py --validate-only
```

### Build Bundles Only (Skip Validation)

```bash
python scripts/build_bundles.py --build-only
```

### Full Build (Validate + Build)

```bash
python scripts/build_bundles.py
```

## 📋 Requirements

- Python 3.11+
- PyYAML (`pip install pyyaml`)

## 📄 License

This collection is provided as-is for personal use. Individual feeds are subject to their respective sources' terms of service.

## 🤝 Contributing

Contributions are welcome! Please:

1. Ensure feeds are freely accessible (no hard paywalls)
2. Verify RSS/Atom URLs are valid
3. Organize feeds in the appropriate category file
4. Update bundle configurations if adding new categories

## 🔍 Feed Criteria

All feeds in this collection should:

- ✅ Be freely accessible (or have substantial free content)
- ✅ Provide valid RSS/Atom feeds
- ✅ Have consistent publishing schedules
- ✅ Be from reputable sources
