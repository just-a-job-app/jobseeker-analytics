"use client";

import type { ThemeProviderProps } from "next-themes";

import * as React from "react";
import { HeroUIProvider } from "@heroui/system";
import { useRouter } from "next/navigation";
import { ThemeProvider as NextThemesProvider } from "next-themes";
import { ToastProvider } from "@heroui/toast";
import { usePostHog } from "posthog-js/react";
import { usePathname, useSearchParams } from "next/navigation";
import { useEffect, Suspense } from "react";
import posthog from "posthog-js";
import { PostHogProvider as PHProvider } from "posthog-js/react";

export function PostHogProvider({ children }: { children: React.ReactNode }) {
	const posthogKey = process.env.NEXT_PUBLIC_POSTHOG_KEY;
	const [isInitialized, setIsInitialized] = React.useState(false);

	const getCookie = (name: string): string | null => {
		if (typeof document === "undefined") return null;
		const nameEQ = `${name}=`;
		const cookies = document.cookie.split(";");
		for (let cookie of cookies) {
			cookie = cookie.trim();
			if (cookie.startsWith(nameEQ)) {
				return decodeURIComponent(cookie.substring(nameEQ.length));
			}
		}
		return null;
	};

	useEffect(() => {
		if (posthogKey) {
			// Check for GPC signal
			const hasGPCSignal = () => {
				// Check navigator.globalPrivacyControl (standard GPC signal)
				if ("globalPrivacyControl" in navigator) {
					return (navigator as Navigator & { globalPrivacyControl: boolean }).globalPrivacyControl === true;
				}
				return false;
			};

			// Check if user has given consent via the jaja-consent cookie
			const consentCookie = getCookie("jaja-consent");
			const hasConsent = consentCookie === "true";

			// Only initialize PostHog if user has given consent and GPC is not enabled
			if (hasConsent && !hasGPCSignal()) {
				posthog.init(posthogKey, {
					api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || "https://us.i.posthog.com",
					person_profiles: "identified_only",
					capture_pageview: false, // Disable automatic pageview capture, as we capture manually
					opt_out_capturing_by_default: false,
					respect_dnt: true // Also respect Do Not Track signals
				});
				setIsInitialized(true);
			} else if (hasGPCSignal() || consentCookie === "false") {
				// Opt out if GPC signal is present or user has explicitly declined
				posthog.opt_out_capturing();
			}
		}
	}, [posthogKey]);

	// If no PostHog key is configured or not initialized, return children without PHProvider
	if (!posthogKey || !isInitialized) {
		return <>{children}</>;
	}

	return (
		<PHProvider client={posthog}>
			<SuspendedPostHogPageView />
			{children}
		</PHProvider>
	);
}

function PostHogPageView() {
	const pathname = usePathname();
	const searchParams = useSearchParams();
	const posthog = usePostHog();

	// Track pageviews
	useEffect(() => {
		if (pathname && posthog) {
			let url = window.origin + pathname;
			if (searchParams.toString()) {
				url = url + "?" + searchParams.toString();
			}

			posthog.capture("$pageview", { $current_url: url });
		}
	}, [pathname, searchParams, posthog]);

	return null;
}

// Wrap PostHogPageView in Suspense to avoid the useSearchParams usage above
// from de-opting the whole app into client-side rendering
// See: https://nextjs.org/docs/messages/deopted-into-client-rendering
function SuspendedPostHogPageView() {
	return (
		<Suspense fallback={null}>
			<PostHogPageView />
		</Suspense>
	);
}

export interface ProvidersProps {
	children: React.ReactNode;
	themeProps?: ThemeProviderProps;
}

declare module "@react-types/shared" {
	interface RouterConfig {
		routerOptions: NonNullable<Parameters<ReturnType<typeof useRouter>["push"]>[1]>;
	}
}

export function Providers({ children, themeProps }: ProvidersProps) {
	const router = useRouter();

	return (
		<HeroUIProvider navigate={router.push}>
			<ToastProvider
				placement="top-center"
				toastProps={{
					timeout: 2000
				}}
			/>
			<NextThemesProvider {...themeProps}>{children}</NextThemesProvider>
		</HeroUIProvider>
	);
}
