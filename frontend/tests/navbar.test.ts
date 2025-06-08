import { test, expect } from "@playwright/test";

test.describe("Navbar Tests", () => {
	const HOMEPAGE_URL = "http://localhost:3000";

	test.beforeEach(async ({ page }) => {
		await page.goto(HOMEPAGE_URL);
	});

	test("should render navbar properly", async ({ page }) => {
		const navbar = await page.locator("nav");
		await expect(navbar).toBeVisible();
	});

	test("should navigate to home when clicking the brand logo", async ({ page }) => {
		const brandLogo = page.locator('[data-testid="Logo"]');
		await expect(brandLogo).toBeVisible();
		await brandLogo.click();
		await expect(page).toHaveURL("http://localhost:3000");
	});

	test("should contain GitHub link", async ({ page }) => {
		const githubLink = page.locator('a[aria-label="Github"]').first();
		await expect(githubLink).toHaveAttribute("href", /github\.com/);
		await expect(githubLink).toHaveAttribute("target", "_blank");
	});

	test("should have a theme switch button", async ({ page }) => {
		const themeSwitch = page.locator('[data-testid="theme-switch-button"] >> nth=0');
		await expect(themeSwitch).toBeVisible();
	});

	test("should contain Sponsor button with correct link", async ({ page }) => {
		const sponsorButton = await page.locator('[data-testid="Sponsor"]');
		await expect(sponsorButton).toBeVisible();
		await expect(sponsorButton).toHaveAttribute("href", "https://buymeacoffee.com/Just a Job App");
	});

	test("should show login button on the home page", async ({ page }) => {
		const loginButton = page.locator('[data-testid="GoogleLogin"]');
		await expect(loginButton).toBeVisible();
		await expect(loginButton).toHaveText("Login with Google");
		await loginButton.click();
		await page.waitForURL("**/accounts.google.com/**");
		const currentURL = page.url();
		expect(currentURL).toMatch(/https:\/\/accounts\.google\.com/);
	});

	test("should show logout button on success page", async ({ page }) => {
		await page.goto("http://localhost:3000/success");
		const logoutButton = page.locator('[data-testid="GoogleLogout"]');
		await expect(logoutButton).toBeVisible();
		await expect(logoutButton).toHaveText("Logout");
	});

	test("should show navbar hamburger for smaller screens", async ({ page }) => {
		await page.setViewportSize({ width: 375, height: 667 });
		const menuToggle = page
			.locator('button[type="button"] >> span.sr-only:has-text("open navigation menu")')
			.first();
		await expect(menuToggle).toBeVisible();
	});

	test("login button should be visible on the home page for smaller screens", async ({ page }) => {
		await page.setViewportSize({ width: 375, height: 667 });
		const loginButton = page.locator('[data-testid="GoogleLoginSmallScreen"]');
		await expect(loginButton).toBeVisible();
		await expect(loginButton).toHaveText("Login with Google");
		await loginButton.click();
		await page.waitForURL("**/accounts.google.com/**");
		const currentURL = page.url();
		expect(currentURL).toMatch(/https:\/\/accounts\.google\.com/);
	});

	test("logout button should be visible on the success page for smaller screens", async ({ page }) => {
		await page.setViewportSize({ width: 375, height: 667 });
		await page.goto("http://localhost:3000/success");
		const logoutButton = page.locator('[data-testid="GoogleLogoutSmallScreen"]');
		await expect(logoutButton).toBeVisible();
		await expect(logoutButton).toHaveText("Logout");
	});
});
