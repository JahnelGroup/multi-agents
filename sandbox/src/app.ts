import express from "express";

const app = express();
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({ status: "ok" });
});

if (require.main === module) {
  app.listen(3000, () => {
    console.log("Sandbox listening on port 3000");
  });
}

export { app };
