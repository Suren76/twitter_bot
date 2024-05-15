from twitter_scraper_selenium import scrape_profile

microsoft = scrape_profile(twitter_username="ton_blockchain", browser="firefox", output_format="json", tweets_count=10, directory=".")
print(microsoft)
