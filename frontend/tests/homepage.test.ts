import { test, expect } from "@playwright/test";

test.describe("Homepage Tests", () => {
	const HOMEPAGE_URL = "http://localhost:3000";

	test.beforeEach(async ({ page }) => {
		await page.goto(HOMEPAGE_URL);
	});

	test("Google Login button is visible (Desktop)", async ({ page }) => {
		await page.setViewportSize({ width: 1280, height: 800 });
		await page.goto("http://localhost:3000");
	});

	test("Email input box is visible", async ({ page }) => {
		const emailInput = page.locator("input[type='email']");
		await expect(emailInput).toBeVisible();
	});

	test("Opt-in checkbox is visible", async ({ page }) => {
		const optInCheckbox = page.locator(
			'input[aria-label="Opt in to receive updates by email about Just a Job App"]'
		);
		await expect(optInCheckbox).toBeVisible();
	});

	test("reCAPTCHA box is visible", async ({ page }) => {
		const recaptchaIframe = page.locator("iframe[src*='recaptcha']");
		await expect(recaptchaIframe).toBeVisible();
	});

	test("Subscribe button is visible", async ({ page }) => {
		const subscribeButton = page.locator("button", { hasText: "Subscribe" });
		await expect(subscribeButton).toBeVisible();
		const button = page.locator('[data-testid="GoogleLogin"]');
		await expect(button).toBeVisible();
	});

	test("Discord card is visible and clickable", async ({ page }) => {
		const discordCard = page.locator("button:has-text('Just a Job App Community on Discord')");
		await expect(discordCard).toBeVisible();

		await discordCard.click();
		await expect(page).toHaveURL("https://discord.com/invite/gsdpMchCam");
	});

	test("Never Search Alone card is visible and clickable", async ({ page }) => {
		await page.setViewportSize({ width: 1280, height: 800 });
		const neverSearchAloneCard = page.locator('button:has-text("Never Search Alone - phyl.org")');
		await expect(neverSearchAloneCard).toBeVisible();

		await neverSearchAloneCard.click();
		await expect(page).toHaveURL(/phyl\.org/);
	});
});
