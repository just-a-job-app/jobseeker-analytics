/** @type {import('next').NextConfig} */
const nextConfig = {
	output: "standalone",
	// Ensure experimental features are removed
	experimental: {
		// Remove any experimental features
	},

	// Add PostHog rewrites
	async rewrites() {
		return [
			{
				source: "/ingest/static/:path*",
				destination: "https://us-assets.i.posthog.com/static/:path*"
			},
			{
				source: "/ingest/:path*",
				destination: "https://us.i.posthog.com/:path*"
			}
		];
	},

	// Required to support PostHog trailing slash API requests
	skipTrailingSlashRedirect: true
};

module.exports = nextConfig;
