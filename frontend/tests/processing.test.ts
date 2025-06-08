import { test, expect } from "@playwright/test";

test.describe("Processing Tests", () => {
	const PROCESSING_URL = "http://localhost:3000/preview/processing";

	test.beforeEach(async ({ page }) => {
		await page.goto(PROCESSING_URL);
	});

	test("Spinner is visible", async ({ page }) => {
		const spinner = await page.locator('[data-testid="Spinner"]');
		await expect(spinner).toBeVisible();
	});

	test("Progress bar is visible", async ({ page }) => {
		const progressBar = await page.locator('[role="progressbar"]');
		await expect(progressBar).toBeVisible();
	});

	test("Progress bar goes from 0 to 100 and remains in the range of 0-100", async ({ page }) => {
		const progressBar = page.locator('[role="progressbar"]');

		let previousValue = await progressBar.getAttribute("aria-valuenow");
		console.log("Initial progress value:", previousValue);
		await expect(previousValue).toBe("0");

		for (let i = 0; i < 9; i++) {
			await page.waitForTimeout(500);
			const currentValue = await progressBar.getAttribute("aria-valuenow");
			console.log(`Progress value at step ${i}:`, currentValue);

			expect(Number(currentValue)).toBeGreaterThanOrEqual(0);
			expect(Number(currentValue)).toBeLessThanOrEqual(100);

			if (i > 0) {
				expect(Number(currentValue)).toBeGreaterThan(Number(previousValue));
			}

			previousValue = currentValue;
		}
	});
});
