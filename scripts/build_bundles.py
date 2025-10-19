#!/usr/bin/env python3
"""
OPML Bundle Builder and Validator

This script:
1. Validates all OPML files in the repository
2. Reads bundle configuration files from the bundles/ directory
3. Merges OPML files according to bundle configurations
4. Generates combined OPML files for distribution
"""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List

import yaml


class OPMLValidator:
    """Validates OPML files for correctness and free content."""

    @staticmethod
    def validate_opml(file_path: Path) -> tuple[bool, str]:
        """
        Validate an OPML file.

        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()

            # Check if it's a valid OPML file
            if root.tag != "opml":
                return False, f"Root element is '{root.tag}', expected 'opml'"

            # Check for required structure
            head = root.find("head")
            body = root.find("body")

            if head is None:
                return False, "Missing required <head> element"

            if body is None:
                return False, "Missing required <body> element"

            # Count RSS feeds
            rss_count = len(root.findall(".//outline[@type='rss']"))

            if rss_count == 0:
                return False, "No RSS feeds found in file"

            print(f"✓ {file_path.name}: Valid OPML with {rss_count} feeds")
            return True, ""

        except ET.ParseError as e:
            return False, f"XML parsing error: {str(e)}"
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"


class BundleBuilder:
    """Builds OPML bundles from configuration files."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.bundles_dir = base_dir / "bundles"
        self.output_dir = base_dir / "dist"

    def load_bundle_config(self, config_file: Path) -> Dict[str, Any]:
        """Load a bundle configuration file."""
        with open(config_file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def merge_opml_files(
        self, source_files: List[str], bundle_name: str, bundle_desc: str
    ) -> ET.Element:
        """
        Merge multiple OPML files into a single OPML structure.

        Args:
            source_files: List of OPML file paths relative to base_dir
            bundle_name: Name for the bundle
            bundle_desc: Description for the bundle

        Returns:
            ET.Element: Root element of merged OPML
        """
        # Create root OPML structure
        opml = ET.Element("opml", version="2.0")
        head = ET.SubElement(opml, "head")
        title = ET.SubElement(head, "title")
        title.text = bundle_name

        body = ET.SubElement(opml, "body")

        # Process each source file
        for source_file in source_files:
            source_path = self.base_dir / source_file

            if not source_path.exists():
                print(f"⚠ Warning: Source file not found: {source_file}")
                continue

            try:
                tree = ET.parse(source_path)
                source_body = tree.getroot().find("body")

                if source_body is not None:
                    # Copy all outline elements from source to merged body
                    for outline in source_body:
                        body.append(outline)

            except Exception as e:
                print(f"⚠ Warning: Failed to process {source_file}: {str(e)}")

        return opml

    def build_bundle(self, config_file: Path) -> bool:
        """
        Build a bundle from its configuration file.

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            config = self.load_bundle_config(config_file)

            bundle_name = config.get("name", "Unnamed Bundle")
            bundle_desc = config.get("description", "")
            output_file = config.get("output", "bundle.opml.xml")
            source_files = config.get("sources", [])

            print(f"\n📦 Building bundle: {bundle_name}")
            print(f"   Output: {output_file}")
            print(f"   Sources: {len(source_files)} files")

            # Merge OPML files
            merged_opml = self.merge_opml_files(source_files, bundle_name, bundle_desc)

            # Create output directory if it doesn't exist
            self.output_dir.mkdir(exist_ok=True)

            # Write output file
            output_path = self.output_dir / output_file
            tree = ET.ElementTree(merged_opml)
            ET.indent(tree, space="    ")
            tree.write(output_path, encoding="UTF-8", xml_declaration=True)

            # Count feeds in output
            feed_count = len(merged_opml.findall(".//outline[@type='rss']"))
            print(f"   ✓ Created with {feed_count} feeds")

            return True

        except Exception as e:
            print(f"   ✗ Failed to build bundle: {str(e)}")
            return False

    def build_all_bundles(self) -> bool:
        """
        Build all bundles found in the bundles directory.

        Returns:
            bool: True if all bundles built successfully
        """
        if not self.bundles_dir.exists():
            print(f"✗ Bundles directory not found: {self.bundles_dir}")
            return False

        bundle_configs = list(self.bundles_dir.glob("*.yaml"))

        if not bundle_configs:
            print(f"✗ No bundle configuration files found in {self.bundles_dir}")
            return False

        print(f"\n🔨 Building {len(bundle_configs)} bundle(s)...")

        success = True
        for config_file in bundle_configs:
            if not self.build_bundle(config_file):
                success = False

        return success


def main():
    parser = argparse.ArgumentParser(description="Build and validate OPML bundles")
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate OPML files without building bundles",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Only build bundles without validation",
    )

    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent

    print("=" * 60)
    print("OPML Bundle Builder and Validator")
    print("=" * 60)

    all_valid = True

    # Validation phase
    if not args.build_only:
        print("\n🔍 Validating OPML files...")

        validator = OPMLValidator()
        opml_files = list(base_dir.glob("*.opml.xml"))

        if not opml_files:
            print("✗ No OPML files found in repository")
            return 1

        for opml_file in opml_files:
            is_valid, error_msg = validator.validate_opml(opml_file)
            if not is_valid:
                print(f"✗ {opml_file.name}: {error_msg}")
                all_valid = False

        if not all_valid:
            print("\n✗ Validation failed. Please fix the errors above.")
            return 1

        print(f"\n✓ All {len(opml_files)} OPML files are valid!")

    # Build phase
    if not args.validate_only:
        builder = BundleBuilder(base_dir)

        if not builder.build_all_bundles():
            print("\n✗ Some bundles failed to build")
            return 1

        print("\n✓ All bundles built successfully!")
        print(f"   Output directory: {builder.output_dir}")

    print("\n" + "=" * 60)
    print("✓ Process completed successfully!")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())
