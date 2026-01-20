const jsonServer = require("json-server");
const server = jsonServer.create();
const router = jsonServer.router("db.json");
const middlewares = jsonServer.defaults();

const PORT = process.env.MOCK_PORT || 4444;
const HOST = process.env.MOCK_HOST || "localhost";

server.use(middlewares);

server.use("/", (req, res, next) => {
  next();
});

router.render = (req, res) => {
  const data = res.locals.data;
  const url = new URL(req.originalUrl, "http://localhost");

  const shouldWrapResponse = req.originalUrl.startsWith("/api");
  const shouldReturnRawResponse = req.originalUrl.startsWith("/raw");
  const shouldReturnNestedResponse = req.originalUrl.startsWith("/nested");

  if (shouldWrapResponse && Array.isArray(data) && req.method === "GET") {
    // List responses (arrays) => wrap in { results, count, page }
    const totalCount = res.getHeader("X-Total-Count");
    const page = Number(url.searchParams.get("_page")) || 1;
    const pageSize = Number(url.searchParams.get("_page"))
      ? Number(url.searchParams.get("_limit"))
        ? Number(url.searchParams.get("_limit"))
        : 10
      : data.length;

    res.json({
      results: data,
      total: totalCount ? Number(totalCount) : data.length,
      _page: page,
      _limit: pageSize,
    });
  } else if (
    shouldReturnRawResponse &&
    Array.isArray(data) &&
    req.method === "GET"
  ) {
    // List responses (arrays) => return raw data
    res.json(data);
  } else if (
    shouldReturnNestedResponse &&
    Array.isArray(data) &&
    req.method === "GET"
  ) {
    // List responses (arrays) => wrap in { results.data[] }
    res.json({
      results: {
        data: [data],
      },
    });
  } else {
    // For single item (GET /api/users/1), POST, PUT, etc.
    res.json(data);
  }
};

server.use("/api", router);
server.use("/nested", router);
server.use("/raw", router);

server.listen(PORT, "0.0.0.0", () => {
  console.log(`JSON Server is running on http://${HOST}:${PORT}/api`);
});
