/** @type {import('next').NextConfig} */
const nextConfig = {
	output: "standalone",
	// Ensure experimental features are removed
	experimental: {
		// Remove any experimental features
	},
	async headers() {
		return [
			{
				source: "/robots.txt",
				headers: [
					{
						key: "Content-Security-Policy",
						value: "default-src 'none'"
					}
				]
			}
		];
	}
};

module.exports = nextConfig;
