import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";

const JWT_SECRET = process.env.JWT_SECRET || "dev-secret-change-in-production";

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing or invalid Authorization header" });
  }
  const token = authHeader.slice(7);
  try {
    const decoded = jwt.verify(token, JWT_SECRET) as { sub: string; exp: number };
    const now = Math.floor(Date.now() / 1000);
    if (decoded.exp <= now) {
      return res.status(401).json({ error: "Token expired" });
    }
    (req as Request & { user?: string }).user = decoded.sub;
    next();
  } catch {
    return res.status(401).json({ error: "Invalid token" });
  }
}
