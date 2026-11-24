import cloudscraper
from scrapy.http import HtmlResponse


class CustomCloudflareMiddleware:

    cloudflare_scraper = cloudscraper.create_scraper()

    def process_response(self, request, response, spider):
        request_url = request.url
        response_status = response.status
        if response_status not in (403, 503):
            return response

        spider.logger.info(
            "Cloudflare detected. Using cloudscraper on URL: %s", request_url
        )
        cflare_response = self.cloudflare_scraper.get(request_url)
        if cflare_response.status_code in (403, 503):
            allowed_statuses = request.meta.get("handle_httpstatus_list", [])
            if cflare_response.status_code not in allowed_statuses:
                request.meta["handle_httpstatus_list"] = [
                    *allowed_statuses,
                    cflare_response.status_code,
                ]

        return HtmlResponse(
            url=cflare_response.url,
            status=cflare_response.status_code,
            body=cflare_response.content,
            encoding=cflare_response.encoding or "utf-8",
            request=request,
        )
