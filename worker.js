const UPSTREAM_FEED =
  "https://github.com/Loungechill/WilliamsOliverABC/releases/download/feed-latest/feed.xml";

export default {
  async fetch(request) {
    const requestUrl = new URL(request.url);

    if (requestUrl.pathname !== "/" && requestUrl.pathname !== "/feed.xml") {
      return new Response("Not found", { status: 404 });
    }

    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method not allowed", {
        status: 405,
        headers: { Allow: "GET, HEAD" },
      });
    }

    const upstreamUrl = new URL(UPSTREAM_FEED);
    upstreamUrl.searchParams.set(
      "cache_bucket",
      String(Math.floor(Date.now() / 300_000)),
    );

    const upstream = await fetch(upstreamUrl, {
      redirect: "follow",
      headers: {
        "User-Agent": "WilliamsOliverABC-Cloudflare-Worker/1.0",
      },
      cf: {
        cacheEverything: true,
        cacheTtl: 300,
      },
    });

    if (!upstream.ok) {
      return new Response(
        `Upstream feed is unavailable: HTTP ${upstream.status}`,
        {
          status: 502,
          headers: { "Content-Type": "text/plain; charset=utf-8" },
        },
      );
    }

    const headers = new Headers();
    headers.set("Content-Type", "application/xml; charset=utf-8");
    headers.set("Content-Disposition", 'inline; filename="feed.xml"');
    headers.set("Cache-Control", "public, max-age=300");

    for (const headerName of ["etag", "last-modified", "content-length"]) {
      const value = upstream.headers.get(headerName);

      if (value) {
        headers.set(headerName, value);
      }
    }

    return new Response(request.method === "HEAD" ? null : upstream.body, {
      status: 200,
      headers,
    });
  },
};

