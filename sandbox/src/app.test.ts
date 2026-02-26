import request from "supertest";
import { app } from "./app";

describe("GET /", () => {
  it("returns 200 with status ok", async () => {
    const res = await request(app).get("/");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: "ok" });
  });
});
