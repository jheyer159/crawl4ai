import os
import sys
import pytest
import asyncio

# Add the parent directory to the Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir)

from crawl4ai.async_webcrawler import AsyncWebCrawler
from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy

@pytest.mark.asyncio
async def test_stream_crawl_basic():
    async with AsyncWebCrawler(verbose=True) as crawler:
        url = "https://www.example.com"
        result = await crawler.crawler_strategy.stream_crawl(url=url, config={})
        assert result.success
        assert result.html
        assert result.status_code == 200

@pytest.mark.asyncio
async def test_stream_crawl_infinite_scroll():
    async with AsyncWebCrawler(verbose=True) as crawler:
        url = "https://www.infinite-scroll.com/demo/full-page/"
        result = await crawler.crawler_strategy.stream_crawl(url=url, config={})
        assert result.success
        assert result.html
        assert result.status_code == 200

@pytest.mark.asyncio
async def test_stream_crawl_with_js():
    async with AsyncWebCrawler(verbose=True) as crawler:
        js_code = "document.body.innerHTML = '<h1>Modified by JS</h1>';"
        url = "https://www.example.com"
        result = await crawler.crawler_strategy.stream_crawl(url=url, config={"js_code": js_code})
        assert result.success
        assert "<h1>Modified by JS</h1>" in result.html

@pytest.mark.asyncio
async def test_stream_crawl_with_custom_headers():
    async with AsyncWebCrawler(verbose=True) as crawler:
        custom_headers = {"X-Test-Header": "TestValue"}
        url = "https://httpbin.org/headers"
        result = await crawler.crawler_strategy.stream_crawl(url=url, config={"headers": custom_headers})
        assert result.success
        assert "X-Test-Header" in result.html
        assert "TestValue" in result.html

@pytest.mark.asyncio
async def test_stream_crawl_with_screenshot():
    async with AsyncWebCrawler(verbose=True) as crawler:
        url = "https://www.example.com"
        result = await crawler.crawler_strategy.stream_crawl(url=url, config={"screenshot": True})
        assert result.success
        assert result.screenshot
        assert isinstance(result.screenshot, str)
        assert len(result.screenshot) > 0

# Entry point for debugging
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
