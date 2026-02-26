import { Router, Request, Response } from "express";
import jwt from "jsonwebtoken";

const router = Router();
const JWT_SECRET = process.env.JWT_SECRET || "dev-secret-change-in-production";

// In-memory user store for demo (replace with real DB in production)
const users: Record<string, { email: string; password: string }> = {
  "user@example.com": { email: "user@example.com", password: "password123" },
};

router.post("/login", (req: Request, res: Response) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: "Email and password required" });
  }
  const user = users[email];
  if (!user || user.password !== password) {
    return res.status(401).json({ error: "Invalid credentials" });
  }
  const token = jwt.sign(
    { sub: email },
    JWT_SECRET,
    { expiresIn: "1h" }
  );
  return res.json({ token });
});

export { router as authRouter };
