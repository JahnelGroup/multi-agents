import request from "supertest";
import express from "express";
import { authRouter } from "./login";

const app = express();
app.use(express.json());
app.use("/auth", authRouter);

describe("POST /auth/login", () => {
  it("returns JWT token on valid credentials", async () => {
    const res = await request(app)
      .post("/auth/login")
      .send({ email: "user@example.com", password: "password123" });
    expect(res.status).toBe(200);
    expect(res.body).toHaveProperty("token");
    expect(typeof res.body.token).toBe("string");
  });

  it("returns 401 on invalid credentials", async () => {
    const res = await request(app)
      .post("/auth/login")
      .send({ email: "user@example.com", password: "wrong" });
    expect(res.status).toBe(401);
    expect(res.body.error).toContain("Invalid");
  });

  it("returns 400 when email or password missing", async () => {
    const res = await request(app)
      .post("/auth/login")
      .send({ email: "user@example.com" });
    expect(res.status).toBe(400);
  });
});
