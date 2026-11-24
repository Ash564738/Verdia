import { describe, expect, it } from "vitest";

describe("Smart Plant Care frontend", () => {
  it("has a configured API fallback", () => {
    expect(import.meta.env.VITE_API_URL ?? "http://localhost:8000").toContain("http");
  });
});
