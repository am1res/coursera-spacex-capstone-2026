# SpaceX historical launch analysis

AI-assisted research coursework prepared for Amir Saulebekov for the IBM Applied Data Science Capstone. All eight notebooks contain actual local execution outputs. The final Coursera presentation is withheld for the scheduled November 1 submission.

## Contents

- `notebooks/01_api_collection_fallback.ipynb`: recorded live API timeout, official JSON normalization, explicit frozen enrichment fallback, Falcon 9 filtering and payload handling.
- `notebooks/02_web_scraping_completed.ipynb`: actual extraction of 121 numbered Falcon 9 records from the specified historical Wikipedia revision.
- `notebooks/03_data_wrangling_completed.ipynb`: launch counts, orbit/outcome summaries and the course target definition.
- `notebooks/04_sql_eda_completed.ipynb`: all ten requested SQLite queries and results.
- `notebooks/05_visual_eda_completed.ipynb`: six EDA plots and one-hot feature engineering.
- `notebooks/06_folium_analytics_completed.ipynb`: launch-site and outcome maps plus approximate distances to visible reference features.
- `notebooks/07_dash_dashboard_completed.ipynb`: runnable dashboard source and local HTTP check.
- `notebooks/08_classification_completed.ipynb`: four classifiers, ten-fold grid searches, holdout scores and confusion matrices.
- `spacex_dashboard.py`: site and payload filters for historical landing labels.
- `model_frozen_snapshot.py`: supplementary analysis with preprocessing fitted inside training folds and LandingPad excluded.
- `execution-evidence.json`: executed cell counts and error counts.

## Run

Install `requirements.txt` in a Python environment. Open notebooks from the `notebooks/` directory so their relative dataset paths resolve. Run `python spacex_dashboard.py` from the repository root and open http://127.0.0.1:8055/. The course data and standalone maps are included for reproducibility. Run `python fetch_wikipedia_snapshot.py` before executing the scraping notebook.

## Findings and limits

The modeling dataset has 90 flights dated 2010–2020, with 60 positive and 30 negative course labels. The official SQL snapshot has 101 rows. The official geographic snapshot has 56 flights and four historical site labels. These populations must not be silently combined.

The live SpaceX API timed out. Notebook 1 uses the provided official JSON and enriched CSV and does not claim the original per-endpoint enrichment calls succeeded. The CSV already contains imputed payload mass, so the original missing-payload distribution cannot be reconstructed from it.

The requested classification exercise standardizes all rows before the train/test split, which leaks preprocessing information. Its 18-flight holdout is small. The supplementary script demonstrates a separate fold-safe analysis and excludes LandingPad; its feature set and scores differ. Neither analysis predicts current reliability, launch prices or causal site/payload effects.

Map distances use Haversine calculations and approximate reference points selected from visible OpenStreetMap features. They are straight-line distances, not road routes or guaranteed exact nearest-feature distances.

## Sources and attribution

IBM course starter notebooks retain their original authorship and copyright notices. Public course datasets come from https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/ and the course SQL lab. Original work here fills the tasks and adds research disclosures and analysis.

The scraping notebook uses the revision requested by the course (download it with fetch_wikipedia_snapshot.py): https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922 . Wikipedia text is attributable to its contributors under its displayed Creative Commons Attribution-ShareAlike license. The downloaded HTML retains attribution and license links. The full article HTML is not checked into this repository. Maps retain © OpenStreetMap contributors and Leaflet attribution.
