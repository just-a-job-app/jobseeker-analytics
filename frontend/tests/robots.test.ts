import { test, expect } from "@playwright/test";

test.describe("Robots.txt Tests", () => {
	const ROBOTS_URL = "http://localhost:3000/robots.txt";

	test("robots.txt should be accessible", async ({ page }) => {
		const response = await page.goto(ROBOTS_URL);
		expect(response?.status()).toBe(200);
	});

	test("robots.txt should have Content-Security-Policy header", async ({ page }) => {
		const response = await page.goto(ROBOTS_URL);
		const headers = response?.headers();
		expect(headers).toHaveProperty("content-security-policy");
		expect(headers?.["content-security-policy"]).toContain("default-src");
	});

	test("robots.txt should contain valid robots directives", async ({ page }) => {
		const response = await page.goto(ROBOTS_URL);
		const content = await response?.text();
		expect(content).toContain("User-agent:");
	});
});
