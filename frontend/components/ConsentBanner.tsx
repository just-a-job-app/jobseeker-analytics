"use client";

import React, { useState, useEffect } from "react";
import { Card, Button } from "@heroui/react";

interface ConsentBannerProps {
	onAccept?: () => void;
}

/**
 * Lightweight consent banner using HeroUI components.
 * Reads/writes the 'jaja-consent' cookie to manage user consent for analytics (PostHog).
 * If cookie exists, banner is hidden. Otherwise, displays Accept/Decline buttons.
 */
export const ConsentBanner: React.FC<ConsentBannerProps> = ({ onAccept }) => {
	const [isVisible, setIsVisible] = useState(false);

	useEffect(() => {
		// Check if jaja-consent cookie exists
		const hasConsent = getCookie("jaja-consent");
		setIsVisible(!hasConsent);
	}, []);

	const setCookieValue = (name: string, value: string, days = 365) => {
		const expires = new Date();
		expires.setTime(expires.getTime() + days * 24 * 60 * 60 * 1000);
		const expiresString = `expires=${expires.toUTCString()}`;
		document.cookie = `${name}=${encodeURIComponent(value)}; ${expiresString}; path=/; SameSite=Lax`;
	};

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

	const handleAccept = () => {
		setCookieValue("jaja-consent", "true", 365);
		setIsVisible(false);

		// Trigger PostHog initialization if onAccept callback is provided
		if (onAccept) {
			onAccept();
		} else {
			// Otherwise, reload the page to reinitialize PostHog
			window.location.reload();
		}
	};

	const handleDecline = () => {
		setCookieValue("jaja-consent", "false", 365);
		setIsVisible(false);
	};

	if (!isVisible) {
		return null;
	}

	return (
		<div className="fixed bottom-0 left-0 right-0 z-50 p-4">
			<div className="container mx-auto max-w-7xl">
				<Card className="bg-gray-900 border border-gray-700 dark:bg-gray-900 dark:border-gray-700">
					<div className="p-6">
						<div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
							<div className="flex-1">
								<h3 className="text-lg font-semibold text-white mb-2">Privacy & Analytics Consent</h3>
								<p className="text-sm text-gray-300 leading-relaxed">
									We use analytics (PostHog) to understand how you use our app and improve your
									experience. We respect your privacy and do not share your data with third parties
									for advertising.{" "}
									<a
										className="text-blue-400 hover:text-blue-300 underline transition-colors"
										href="/privacy"
									>
										Learn more
									</a>
									.
								</p>
							</div>

							<div className="flex gap-3 md:flex-shrink-0">
								<Button
									className="bg-gray-700 hover:bg-gray-600 text-white font-medium"
									size="sm"
									variant="flat"
									onPress={handleDecline}
								>
									Decline
								</Button>
								<Button
									className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium"
									size="sm"
									onPress={handleAccept}
								>
									Accept
								</Button>
							</div>
						</div>
					</div>
				</Card>
			</div>
		</div>
	);
};

export default ConsentBanner;
