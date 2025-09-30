import "@/styles/globals.css";
import { Metadata, Viewport } from "next";
import clsx from "clsx";
import { Inter } from "next/font/google";
import { cookies } from "next/headers";

import { Providers, PostHogProvider } from "./providers";

import { siteConfig } from "@/config/site";
import { fontSans } from "@/config/fonts";
import FeedbackButton from "@/components/FeedbackButton";
import { Navbar } from "@/components/navbar";

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
	themeColor: [
		{ media: "(prefers-color-scheme: light)", color: "white" },
		{ media: "(prefers-color-scheme: dark)", color: "black" }
	]
};

export default async function RootLayout({ children }: { children: React.ReactNode }) {
	const cookieStore = await cookies();

	// Get Authorization cookie directly
	const authCookie = cookieStore.get("Authorization") || cookieStore.get("__Secure-Authorization");
	let isAuthenticated = false;
	let hasVisited = false;
	let hasPrevAuth = false;

	if (authCookie?.value) {
		hasVisited = true; // Has Authorization cookie = has visited
		hasPrevAuth = true; // Has Authorization cookie = has ever authenticated

		// Check if user is currently authenticated (not logged out)
		isAuthenticated = authCookie.value !== "logged_out";
	}

	return (
		<html suppressHydrationWarning lang="en">
			<head />
			<body
				className={clsx("min-h-screen bg-background font-sans antialiased", fontSans.variable, inter.className)}
			>
				<PostHogProvider>
					<Providers themeProps={{ attribute: "class", defaultTheme: "dark" }}>
						<div className="relative flex h-screen flex-col">
							<Navbar
								hasPrevAuth={hasPrevAuth}
								isAuthenticated={isAuthenticated}
								isFirstVisit={!hasVisited}
							/>
							<main className="container mx-auto flex-grow max-w-7xl px-6 pt-16">{children}</main>
							<FeedbackButton />
						</div>
					</Providers>
				</PostHogProvider>
			</body>
		</html>
	);
}
