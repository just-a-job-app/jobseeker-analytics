import fs from "fs";

import { test, expect } from "@playwright/test";

test.describe("Dashboard Tests", () => {
	const DASHBOARD_URL = "http://localhost:3000/preview/dashboard";

	test.beforeEach(async ({ page }) => {
		await page.goto(DASHBOARD_URL);
	});

	test("Renders the dashboard with title", async ({ page }) => {
		await expect(page.getByRole("heading", { name: "Preview Dashboard" })).toBeVisible();
	});

	test("Displays response rate card and chart", async ({ page }) => {
		await expect(page.getByTestId("response-rate-card")).toBeVisible();
		await expect(page.getByTestId("response-rate-chart")).toBeVisible();
	});

	test("Displays table with correct columns", async ({ page }) => {
		await expect(page.getByRole("columnheader", { name: "Company" })).toBeVisible();
		await expect(page.getByRole("columnheader", { name: "Status" })).toBeVisible();
		await expect(page.getByRole("columnheader", { name: "Received" })).toBeVisible();
		await expect(page.getByRole("columnheader", { name: "Job Title" })).toBeVisible();
		await expect(page.getByRole("columnheader", { name: "Subject" })).toBeVisible();
		await expect(page.getByRole("columnheader", { name: "Sender" })).toBeVisible();
		await expect(page.getByRole("columnheader", { name: "Actions" })).toBeVisible();
	});

	test("Displays data in table when loaded", async ({ page }) => {
		await expect(page.getByRole("rowheader", { name: "FutureVision" })).toBeVisible();
		await expect(page.getByRole("rowheader", { name: "ZenTech" })).toBeVisible();
	});

	test("Correct sorting by Company (A-Z)", async ({ page }) => {
		await page.getByTestId("Sort By").click();
		await page.getByRole("menuitemradio", { name: "Company (A-Z)" }).click();

		// Verify first row is BrightMinds
		const firstRow = page.locator("tbody tr").first();
		await expect(firstRow.getByRole("rowheader")).toHaveText("BrightMinds");
	});

	test("Correct sorting by Date Received (Newest First)", async ({ page }) => {
		await page.getByTestId("Sort By").click();
		await page.getByRole("menuitemradio", { name: "Date Received (Newest First)" }).click();

		// Verify first row is the most recent date
		const dateCells = page.locator("tbody tr td:nth-child(3)");
		const dates = await dateCells.allTextContents();
		const parsedDates = dates.map((d) => new Date(d).getTime());
		expect(parsedDates[0]).toBeGreaterThan(parsedDates[1]);
	});

	test("Shows delete confirmation modal", async ({ page }) => {
		await page.getByRole("row", { name: "FutureVision" }).getByRole("button").click();
		await expect(page.getByText("Confirm Removal")).toBeVisible();
		await expect(page.getByText("Are you sure you want to remove this row?")).toBeVisible();
		await expect(page.getByRole("button", { name: "Cancel" })).toBeVisible();
		await expect(page.getByRole("button", { name: "Yes, remove it" })).toBeVisible();
	});

	test("Download Sankey button is rendered", async ({ page }) => {
		const downloadSankeyButton = await page.locator("button", { hasText: "Download Sankey" });
		await expect(downloadSankeyButton).toBeVisible();
	});

	test("Sankey button triggers file download", async ({ page }) => {
		const [download] = await Promise.all([
			page.waitForEvent("download"),
			page.locator('button:has-text("Sankey")').click()
		]);

		const downloadPath = await download.path();
		console.log("Sankey file download path:", downloadPath);
		expect(downloadPath).toBeDefined();

		const fileExists = fs.existsSync(downloadPath);
		console.log("File exists:", fileExists);
		expect(fileExists).toBe(true);
	});

	test("Download CSV button is rendered", async ({ page }) => {
		const downloadCsvButton = await page.locator("button", { hasText: "Download CSV" });
		await expect(downloadCsvButton).toBeVisible();
	});

	test("CSV button triggers file download", async ({ page }) => {
		const [download] = await Promise.all([
			page.waitForEvent("download"),
			page.locator('button:has-text("Download CSV")').click()
		]);

		const downloadPath = await download.path();
		console.log("CSV file download path:", downloadPath);
		expect(downloadPath).toBeDefined();

		const fileExists = fs.existsSync(downloadPath);
		console.log("File exists:", fileExists);
		expect(fileExists).toBe(true);
	});
});
