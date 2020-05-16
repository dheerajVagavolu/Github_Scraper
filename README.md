# Github Scraper
A personal tool for scraping meta data from Github website, for academic purpose.

* Releases
* Contributors
* Stars
* Forks
* Tags ( Not neacassarily provided in all repositories, So may turn up blank )

I used Requests module in python, due to unavailibility of GUI. This made it difficult to integrate selenium. Change the requests module with whatever library required. The code is easily changeable.
Requests doesnt let you see the data which is loaded using javascript, since it is a simple http request. To counter this I enforced a condition for to check if the page has all the data. if not force another http requests. Which may take a lot of time to get hits.

## Instructions

1) Use 'pip install -r requirements.txt' to install requirements
2) List the repository names in the file 'list' each in a new line.
3) Use 'python main.py' to run the scripts and collect data.

## Find your data in data/'data'

