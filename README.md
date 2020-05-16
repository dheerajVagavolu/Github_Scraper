# Git_Scrape
Scraping meta data from Github website. 

* Releases
* Contributors
* Stars
* Forks
* Tags

I used Requests module, due to unavailibility of GUI. Couldnt use selenium. Change the requests module with whatever library required. The code is easily altered that way
Requests doesnt let you see the data which loaded using javascript. It is a simple http request. To counter this I enforced a condition for forcing the page to load. Which may take a lot of time to get hits.


## Instructions

1) Use 'pip install -r requirements.txt' to install requirements
2) List the repository names in the file 'list'
3) Use 'python main.py' to run the scripts and collect data.

## Find your data in data/'data'

