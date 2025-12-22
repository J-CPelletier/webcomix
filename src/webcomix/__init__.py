import warnings
from scrapy.exceptions import ScrapyDeprecationWarning

# Ignore deprecation warnings related to canonicalize_url
# Since it's related to scrapy-splash
warnings.filterwarnings(
    "ignore",
    message=".*canonicalize_url.*",
    category=ScrapyDeprecationWarning
)
