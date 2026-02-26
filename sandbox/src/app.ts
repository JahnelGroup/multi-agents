import express from "express";
import { authRouter } from "./auth/login";
import { authMiddleware } from "./auth/middleware";

const app = express();
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({ status: "ok" });
});

app.use("/auth", authRouter);
app.get("/protected", authMiddleware, (_req, res) => {
  res.json({ status: "ok" });
});

if (require.main === module) {
  app.listen(3000, () => {
    console.log("Sandbox listening on port 3000");
  });
}

export { app };
