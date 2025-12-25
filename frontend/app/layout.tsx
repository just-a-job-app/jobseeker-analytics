import "@/styles/globals.css";
import { Metadata, Viewport } from "next";
import clsx from "clsx";
import { Inter } from "next/font/google";
import Script from "next/script";

import { Providers, PostHogProvider } from "./providers";

import { siteConfig } from "@/config/site";
import { fontSans } from "@/config/fonts";
import ConditionalFeedbackButton from "@/components/ConditionalFeedbackButton";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
	title: {
		default: siteConfig.name,
		template: `%s - ${siteConfig.name}`
	},
	description: siteConfig.description,
	icons: {
		icon: "/favicon.svg"
	}
};

export const viewport: Viewport = {
	width: "device-width",
	initialScale: 1,
	maximumScale: 1,
	userScalable: false,
	themeColor: [
		{ media: "(prefers-color-scheme: light)", color: "white" },
		{ media: "(prefers-color-scheme: dark)", color: "black" }
	]
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
	return (
		<html suppressHydrationWarning lang="en">
			<body
				className={clsx("min-h-screen bg-background font-sans antialiased", fontSans.variable, inter.className)}
			>
				<PostHogProvider>
					<Providers themeProps={{ attribute: "class", defaultTheme: "dark" }}>
						<div className="relative flex h-screen flex-col">
							<main className="container mx-auto flex-grow max-w-7xl px-6 pt-16">{children}</main>
							<ConditionalFeedbackButton />
						</div>
					</Providers>
				</PostHogProvider>
				<Script
					src="https://app.termly.io/resource-blocker/6adf3d96-4f08-4972-b58b-0e62e4e81785?autoBlock=on"
					strategy="afterInteractive"
				/>
			</body>
		</html>
	);
}
