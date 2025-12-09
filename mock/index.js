const jsonServer = require("json-server");
const server = jsonServer.create();
const router = jsonServer.router("db.json");
const middlewares = jsonServer.defaults();

server.use(middlewares);

server.use("/api", (req, res, next) => {
  next();
});

router.render = (req, res) => {
  const data = res.locals.data;
  const url = new URL(req.originalUrl, "http://localhost");

  // List responses (arrays) => wrap in { results, count, page }
  if (Array.isArray(data) && req.method === "GET") {
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
      page: page,
      page_size: pageSize,
    });
  } else {
    // For single item (GET /api/users/1), POST, PUT, etc.
    res.json(data);
  }
};

server.use("/api", router);

const PORT = 4444;
server.listen(PORT, () => {
  console.log(`JSON Server is running on http://localhost:${PORT}/api`);
});
