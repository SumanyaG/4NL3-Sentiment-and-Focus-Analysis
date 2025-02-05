The dataset is taken from asapsports.com, with the data focusing on responses given by the interviewees.

The data was collected by scraping interview transcripts from ASAP Sports, a website that provides official press conference transcripts for major sports events, including the NBA and WNBA Drafts and Finals. The [scraping_script.py](https://github.com/SumanyaG/4NL3-Sentiment-and-Focus-Analysis/blob/main/Phase_1/Web_Scraping/scraping_script.py) program given, a list of event URLs, scrapes the event data for each URL. These pages contain links to interviews conducted for each event. The scraper navigates through these pages, extracts the URLs of individual interviews, and then parses their content.

For each interview, the script retrieves the event name and date from the webpage's title. The interview text is then processed to distinguish between speakers and their statements. The script identifies questions and removes them to focus on direct quotes from players, coaches, and other any other interviewees. Since some names in the transcripts may not be properly formatted, the script includes logic to validate and clean speaker names, ensuring consistency. Additionally, a function corrects encoding errors that sometimes occur in text extracted from web sources.

Once the data is collected, it is stored in the interviews.csv file containing four key fields: event name, date, speaker, and quote. This structured format makes it easy to analyze the dataset. Afterwards, the data_splitting.py program further processes the data by splitting it into eight datasets with overlapping segments. This ensures that certain interview quotes appear in multiple subsets while maintaining diversity across datasets.

To achieve the overlapping split, the data_splitting.py program first calculates a base size for each dataset and determines an overlap size (15% of the base size). It then randomly selects a subset of quotes to be part of the overlap group and distributes the rest among the datasets. This allows for some redundancy across sets, which can be useful for validation and to determine the annotator agreement.

Overall, the data collection process ensures that structured interview data is extracted from ASAP Sports, cleaned for accuracy, and efficiently organized into manageable subsets. The final datasets can then be used for sentiment evaluation models.

A data point will be considered a single paragraph of a response to an interview question by a player or coach.

The events that are considered will be 2024 WNBA Draft, 2024 WNBA Finals, 2024 NBA Draft, 2024 NBA All Star Game, 2024 All Star Media Day and 2024 All Star Rising Stars Practice