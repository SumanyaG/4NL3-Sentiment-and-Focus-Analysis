This folder contains all relevant files for the project's annotation set-up. This includes:
- **scraping_script.py**: Python script that scrapes data from the website and stores it as CSV files.
- **interviews.csv**: CSV file containing scraped data points from each interview.
- **data_splitting.py**: Python script to split the CSV dataset into 8 separate sets of equal size with 15% overlap.
- **overlap_data.csv**: CSV file containing randomly selected overlap data duplicated across all 7 datasets.
- **datasets**: folder containing, **interview{i}.csv** where i = {1...8}: CSV files that have been split into 8 separate datasets.
- **data-backup**: folder containing expanded data that is not relevant to annotators but has been stored as backup.

For information about data sources, refer to the [Team Proposal](https://github.com/SumanyaG/4NL3-Sentiment-and-Focus-Analysts/blob/main/Project_Proposal/TeamProposal.pdf) document.

Resources:
- [GeeksforGeeks - Web Scraping Tutorial](https://www.geeksforgeeks.org/python-web-scraping-tutorial/)
- [ScrapingBee - Web Scraping 101 with Python](https://www.scrapingbee.com/blog/web-scraping-101-with-python/)