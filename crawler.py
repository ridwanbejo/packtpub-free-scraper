"""
URL: https://www.packtpub.com/packt/offers/free-learning
DOM: $("div.dotd-title").html().replace("<h2>", "").replace("</h2>", "").trim()
"""

import scrapy
import subprocess
from datetime import datetime

# slack webhook for crawler to send the book information
CRAWLER_WEBHOOK = "https://hooks.slack.com/services/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"

class PacktpubFreeLearningCrawler(scrapy.Spider):
	name = "packtpub_free_learning_crawler"
	start_urls = ["https://www.packtpub.com/packt/offers/free-learning",]

	def parse(self, response):
		BOOK_TITLE_SELECTOR = "div.dotd-main-book-summary > div"

		print "\nBEGIN THE SCRAPING!\n"

		responses = response.css(BOOK_TITLE_SELECTOR)

		book_title = responses[1].extract() \
									.replace("<h2>", "") \
									.replace("</h2>", "") \
									.replace('<div class="dotd-title">', "") \
									.replace("</div>", "") \
									.strip()

		book_body = responses[2].extract()\
									.replace('<div>', "") \
									.replace("</div>", "") \
									.strip()

		book_body = book_body + "\n" + responses[3].extract()\
									.replace('<div>', "") \
									.replace("</div>", "") \
									.replace("<ul>", "") \
									.replace("</ul>", "") \
									.replace("<li>", "- ") \
									.replace("</li>", "\n") \
									.strip()

		scraping_datetime = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
		book_info = "[%s] This is a book from Packtpub Free Learning: *%s* \n\nThe book is contain about: \n\n%s" % (scraping_datetime, book_title.upper(), book_body)

		print book_info

		# send the book title to slack channel
		subprocess.call("curl -X POST -H 'Content-type: application/json' --data '{\"text\":\"%s\"}' %s" % (book_info, CRAWLER_WEBHOOK), shell=True)


		print "\nEND THE SCRAPING...\n"