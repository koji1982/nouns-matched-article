#!/bin/bash
export PYTHONPATH=/code
export MECABRC=/etc/mecabrc
cd /code/scraping/components
echo "`date` scrapy crawling started" >> /code/crawling.log
/opt/conda/envs/article_env/bin/scrapy crawl article_spider
echo "`date` scrapy crawling finished" >> /code/crawling.log