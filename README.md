# Github Scraper
A personal tool for scraping meta data from Github website, for academic purpose. ( Using selenium and bs4. )

* Releases
* Contributors
* Stars
* Forks
* Tags ( Not neacassarily provided in all repositories, So may turn up blank )

If selenium is not initialised the basic python requests module will be used, which does not enforce a page load. A check method is in place to ensure all the data is properly gathered in the pull request, else the request is skipped. 

When a complete round is over. The program restarts on all the requests that were missed in the first round. It continues until all the repos are finished.

## Instructions

1) Use 'pip install -r requirements.txt' to install requirements or Use the already prepared virtual environment (.venv)
2) Populate the repository names in the file 'list' each in a new line.
3) Use 'python main.py' to run the scripts and collect data.

## Find your data in data/'data'

