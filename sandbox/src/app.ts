import express from "express";
import { authRouter } from "./auth/login";
import { notificationsRouter } from "./notifications/routes";

const app = express();
app.use(express.json());

app.get("/", (_req, res) => {
  res.json({ status: "ok" });
});

app.use("/auth", authRouter);
app.use("/notifications", notificationsRouter);

if (require.main === module) {
  app.listen(3000, () => {
    console.log("Sandbox listening on port 3000");
  });
}

export { app };
