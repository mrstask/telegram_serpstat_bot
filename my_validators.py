from urllib.parse import urlparse
import validators
from settings import serpstat_regions


def validate_serpstat_key(key: str):
    if len(key) == 32 and key.isalnum():
        return True


def validate_domain(domain: str):
    if urlparse(domain).hostname:
        domain = urlparse(domain).hostname
        return validators.domain(domain)
    if validators.domain(domain):
        return domain


def validate_regions(regions: str):
    for region in regions.split(','):
        if region.strip() not in serpstat_regions:
            return region
