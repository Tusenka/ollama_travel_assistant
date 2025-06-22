import re

from fastapi import Request


async def get_external_ip(request: Request) -> str:
    headers_to_check = [
        "CF-Connecting-IP",  # Cloudflare
        "X-Forwarded-For",  # Прокси-серверы
        "X-Real-IP",  # Nginx
    ]

    ip = None
    for header in headers_to_check:
        ip = request.headers.get(header)
        if ip:
            break
    return await sanitize_full_ip(
        ip.split(",")[0].strip() if ip else request.client.host
    )  # fallback


async def sanitize_full_ip(ip: str) -> str:
    return re.sub(r"[^\dA-Za-z.]", "-", ip)
