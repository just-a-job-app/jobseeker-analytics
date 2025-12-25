import posthog from "posthog-js";

// Initialize PostHog client for the frontend
posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY!, {
	api_host: "/ingest",
	ui_host: "https://us.posthog.com",
	defaults: "2025-05-24",
	capture_exceptions: true, // Enable capturing exceptions via Error Tracking
	debug: process.env.NODE_ENV === "development"
});
