import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from io import StringIO
import unittest
from unittest.mock import patch, MagicMock
import sys


class WebCrawler:
    def __init__(self):
        self.visited = set()
        self.index = {}

    def crawl(self, url):
        if url in self.visited:
            return

        try:
            response = requests.get(url)
            self.visited.add(url)

            soup = BeautifulSoup(response.text, 'html.parser')
            text = soup.get_text()
            self.index[url] = text

            for link in soup.find_all('a', href=True):
                href = link['href']
                next_url = urljoin(url, href)
                if urlparse(next_url).netloc == urlparse(url).netloc:
                    self.crawl(next_url)

        except Exception as e:
            print(f"Failed to crawl {url}: {e}")

    def search(self, keyword):
        return [url for url, content in self.index.items() if keyword.lower() in content.lower()]

    def print_results(self, results):
        print("\nSearch Results:")
        if not results:
            print("No matching pages found.")
        for url in results:
            print(url)


def main():
    try:
        start_url = input("Enter the URL to start crawling: ").strip()
        keyword = input("Enter a keyword to search: ").strip()

        crawler = WebCrawler()
        crawler.crawl(start_url)
        results = crawler.search(keyword)
        crawler.print_results(results)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"Error during crawling: {e}")


# ---------------------- Unit Tests ----------------------

class WebCrawlerTests(unittest.TestCase):

    @patch('requests.get')
    def test_crawl_success(self, mock_get):
        sample_html = """
        <html><body>
            <h1>Welcome!</h1>
            <a href="/about">About Us</a>
            <a href="https://www.external.com">External Link</a>
        </body></html>
        """
        mock_response = MagicMock()
        mock_response.text = sample_html
        mock_get.return_value = mock_response

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertIn("https://example.com", crawler.visited)
        self.assertIn("https://example.com/about", crawler.visited)

    @patch('requests.get')
    def test_crawl_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Test Error")

        crawler = WebCrawler()
        crawler.crawl("https://example.com")

        self.assertNotIn("https://example.com", crawler.visited)

    def test_search(self):
        crawler = WebCrawler()
        crawler.index["page1"] = "This has the keyword"
        crawler.index["page2"] = "No match here"

        results = crawler.search("keyword")
        self.assertEqual(results, ["page1"])

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_results(self, mock_stdout):
        crawler = WebCrawler()
        crawler.print_results(["https://test.com/result"])
        output = mock_stdout.getvalue()
        self.assertIn("https://test.com/result", output)
        self.assertIn("Search Results:", output)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])  # Run tests only
    else:
        main()  # Run the crawler
