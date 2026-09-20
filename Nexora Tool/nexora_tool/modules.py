import json
import re
from urllib.parse import quote

import requests


class NexoraError(Exception):
    pass


def _fetch_json(url):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def lookup_ip(ip):
    """Return public IP metadata from public services."""
    if not re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", ip):
        raise NexoraError("Invalid IPv4 address format.")

    urls = {
        "ipwhois": f"https://ipwho.is/{ip}",
        "ipapi": f"https://ipapi.co/{ip}/json/",
    }

    results = {}
    for name, url in urls.items():
        data = _fetch_json(url)
        if data:
            results[name] = data

    if not results:
        return {
            "status": "No public metadata available for this IP.",
            "query": ip,
        }

    return {
        "query": ip,
        "sources": results,
    }


def lookup_telegram(username):
    """Check Telegram public profile and URL availability."""
    clean = username.strip().lstrip("@")
    if not clean:
        raise NexoraError("Telegram username is empty.")

    profile = f"https://t.me/{clean}"
    result = {
        "username": clean,
        "profile_url": profile,
        "search_queries": [
            f"site:t.me {clean}",
            f"site:telegram.org {clean}",
            f"{clean} Telegram",
        ],
    }

    try:
        r = requests.get(profile, timeout=10)
        result["http_status"] = r.status_code
        result["exists_publicly"] = r.status_code in (200, 302, 403)
    except Exception as exc:
        result["error"] = str(exc)

    return result


def lookup_domain(domain):
    """Return domain metadata using public DNS records endpoints."""
    domain = domain.strip().lower().replace("https://", "").replace("http://", "")
    if not domain:
        raise NexoraError("Domain is empty.")

    endpoints = {
        "dns_google": f"https://dns.google/resolve?name={domain}&type=A",
        "cloudflare": f"https://cloudflare-dns.com/dns-query?name={domain}&type=A",
    }

    records = {}
    for name, url in endpoints.items():
        try:
            response = requests.get(url, timeout=12, headers={"accept": "application/json"})
            if response.ok:
                records[name] = response.json()
        except Exception:
            continue

    if not records:
        return {
            "domain": domain,
            "status": "No public DNS data returned.",
        }

    return {
        "domain": domain,
        "records": records,
    }


def search_name(name):
    """Generate search queries and public-search URLs for a person name."""
    text = name.strip()
    if not text:
        raise NexoraError("Person name is empty.")

    encoded = quote(text)
    return {
        "name": text,
        "queries": [
            f"site:linkedin.com/in \"{text}\"",
            f"site:facebook.com \"{text}\"",
            f"site:twitter.com \"{text}\"",
            f"site:instagram.com \"{text}\"",
            f"\"{text}\" OR \"{text.split()[0]}\"",
        ],
        "search_urls": {
            "google": f"https://www.google.com/search?q={encoded}",
            "bing": f"https://www.bing.com/search?q={encoded}",
            "duckduckgo": f"https://duckduckgo.com/?q={encoded}",
        },
    }


def validate_phone(phone):
    """Validate a phone number format and prepare search hints."""
    digits = re.sub(r"\D", "", phone)
    if len(digits) < 7:
        raise NexoraError("Phone number is too short to be valid.")

    return {
        "input": phone,
        "digits_only": digits,
        "likely_e164": "+" + digits if not digits.startswith("+") else digits,
        "search_hints": [
            f"site:linkedin.com \"{phone}\"",
            f"site:facebook.com \"{phone}\"",
            f"\"{phone}\"",
        ],
    }


def validate_email(email):
    """Validate an email address format."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(pattern, email.strip()):
        raise NexoraError("Email format is invalid.")

    domain = email.strip().split("@")[-1]
    return {
        "email": email.strip(),
        "domain": domain,
        "search_urls": {
            "google": f"https://www.google.com/search?q={quote(email.strip())}",
            "bing": f"https://www.bing.com/search?q={quote(email.strip())}",
        },
    }


def quick_osint_probe(query):
    """Infer the type of query and dispatch to the relevant module."""
    q = query.strip()
    if not q:
        raise NexoraError("Query is empty.")

    if re.fullmatch(r"\d{1,3}(?:\.\d{1,3}){3}", q):
        return lookup_ip(q)
    if q.startswith("@") or re.fullmatch(r"[A-Za-z0-9_]{3,32}", q):
        return lookup_telegram(q)
    if "." in q and " " not in q:
        return lookup_domain(q)
    return search_name(q)
