import request from "supertest";
import express from "express";
import jwt from "jsonwebtoken";
import { authMiddleware } from "./middleware";
import { authRouter } from "./login";

const app = express();
app.use(express.json());
app.use("/auth", authRouter);

const secret = process.env.JWT_SECRET || "dev-secret-change-in-production";

app.get("/protected", authMiddleware, (_req, res) => {
  res.json({ status: "ok" });
});

describe("auth middleware", () => {
  it("allows valid token", async () => {
    const token = jwt.sign({ sub: "user-1" }, secret, { expiresIn: "1h" });
    const res = await request(app)
      .get("/protected")
      .set("Authorization", `Bearer ${token}`);
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: "ok" });
  });

  it("rejects expired token with 401", async () => {
    const token = jwt.sign({ sub: "user-1" }, secret, { expiresIn: 0 });
    const res = await request(app)
      .get("/protected")
      .set("Authorization", `Bearer ${token}`);
    expect(res.status).toBe(401);
  });

  it("rejects missing token with 401", async () => {
    const res = await request(app).get("/protected");
    expect(res.status).toBe(401);
  });

  it("rejects invalid token with 401", async () => {
    const res = await request(app)
      .get("/protected")
      .set("Authorization", "Bearer invalid-token");
    expect(res.status).toBe(401);
  });
});
