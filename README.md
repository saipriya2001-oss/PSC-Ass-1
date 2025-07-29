Web Crawler with Search and Unit Testing
This project is a simple web crawler written in Python. It crawls a website, indexes the text content of its pages, and allows keyword-based search over the crawled pages. The project also includes unit tests to ensure functionality.
Features
- Recursively crawls internal links of a given website
- Indexes text content of each visited page
- Allows keyword-based search across all crawled pages
- Ignores external links (only crawls within the same domain)
- Gracefully handles connection and parsing errors
- Includes unit tests using Python's `unittest` and `unittest.mock`
Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library
