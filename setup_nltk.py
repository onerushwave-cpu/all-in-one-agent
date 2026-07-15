"""Download the NLTK data packages the agent relies on.

Run once after installing requirements:  python setup_nltk.py
"""

import nltk

PACKAGES = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "wordnet",
    "averaged_perceptron_tagger_eng",
]


def main() -> None:
    failed = []
    for package in PACKAGES:
        print(f"Downloading {package}...")
        if not nltk.download(package, quiet=True):
            failed.append(package)

    if failed:
        raise SystemExit(f"Failed to download: {', '.join(failed)}")
    print("All NLTK data packages are ready.")


if __name__ == "__main__":
    main()
