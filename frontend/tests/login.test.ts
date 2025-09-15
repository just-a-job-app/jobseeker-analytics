import { test, expect } from "@playwright/test";

const HOMEPAGE_URL = "http://localhost:3000";
const API_ME = "**/me";

test.describe("Login and navbar conditional rendering", () => {
  test("footer login button is always visible", async ({ page }) => {
    await page.goto(HOMEPAGE_URL);
    const footerLogin = page.locator("footer").getByRole("button", { name: "Login with Google" });
    await expect(footerLogin).toBeVisible();
  });

  test("navbar shows Login for returning user with valid session (and hides Request Early Access)", async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem("hasLoggedInBefore", "1");
    });
    await page.route(API_ME, (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ user_id: "abc" }) })
    );

    await page.goto(HOMEPAGE_URL);

    const navbar = page.locator("nav");
    await expect(navbar.getByRole("button", { name: "Login with Google" })).toBeVisible();
    await expect(navbar.getByRole("button", { name: "Request Early Access" })).toHaveCount(0);
  });

  test("navbar does not show Login for brand-new user (no flag); waitlist visible", async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.removeItem("hasLoggedInBefore");
    });
    await page.route(API_ME, (route) => route.fulfill({ status: 401 }));

    await page.goto(HOMEPAGE_URL);

    const navbar = page.locator("nav");
    await expect(navbar.getByRole("button", { name: "Login with Google" })).toHaveCount(0);
    await expect(navbar.getByRole("button", { name: "Request Early Access" })).toBeVisible();
  });

  test("navbar clears returning flag when session expired; login not shown after check", async ({ page }) => {
    await page.addInitScript(() => {
      window.localStorage.setItem("hasLoggedInBefore", "1");
    });
    await page.route(API_ME, (route) => route.fulfill({ status: 401 }));

    const meDone = page.waitForResponse((res) => res.url().includes("/me"));
    await page.goto(HOMEPAGE_URL);
    await meDone;

    // Wait until the app processes the 401 and updates UI/localStorage
    await expect(page.locator("nav").getByRole("button", { name: "Login with Google" })).toHaveCount(0);
    await expect(page.locator("nav").getByRole("button", { name: "Request Early Access" })).toBeVisible();

    await expect.poll(async () => {
      return await page.evaluate(() => window.localStorage.getItem("hasLoggedInBefore"));
    }).toBeNull();
  });

  test("footer login navigates to backend /login", async ({ page }) => {
    await page.goto(HOMEPAGE_URL);
    const footerLogin = page.locator("footer").getByRole("button", { name: "Login with Google" });
    await expect(footerLogin).toBeVisible();

    await footerLogin.click();
    await page.waitForURL("**/accounts.google.com/**");
    const currentURL = page.url();
    expect(currentURL).toMatch(/https:\/\/accounts\.google\.com/);
  });

  test("navbar login navigates to backend /login", async ({ page }) => {
    await page.addInitScript(() => { window.localStorage.setItem("hasLoggedInBefore", "1");});
    await page.route(API_ME, (route) =>
      route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify({ user_id: "abc" }) })
    );
	    
    await page.goto(HOMEPAGE_URL);
    const navbarLogin = page.locator("nav").getByRole("button", { name: "Login with Google" });
    await expect(navbarLogin).toBeVisible();

    await navbarLogin.click();
    await page.waitForURL("**/accounts.google.com/**");
    const currentURL = page.url();
    expect(currentURL).toMatch(/https:\/\/accounts\.google\.com/);
  });
});
