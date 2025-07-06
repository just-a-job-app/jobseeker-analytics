"use client";
import { useState, useEffect } from "react";
import { addToast } from "@heroui/react";

import { ClockIcon } from "@/components/icons";

export default function ResponseRateCard() {
	const [lastUpdated, setLastUpdated] = useState<string>("");
	const [value, setValue] = useState(0);

	const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/";

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await fetch(`${apiUrl}/user-response-rate`, {
					method: "GET",
					credentials: "include" // Include cookies for session management
				});

				if (!response.ok) {
					addToast({
						title: "An error occurred while loading the response rate",
						description: "Please try again or contact help@justajobapp.com if the issue persists.",
						color: "danger"
					});
					return;
				}
				const result = await response.json();
				setValue(result?.value ?? 0);
				setLastUpdated(formatDate(new Date()));
			} catch {
				addToast({
					title: "Connection Error",
					description: "Failed to fetch response rate data",
					color: "danger"
				});
			}
		};

		fetchData();
	}, []);

	// Helper function to format the date
	const formatDate = (date: Date): string => {
		const now = new Date();
		const yesterday = new Date();
		yesterday.setDate(now.getDate() - 1);

		const isToday = date.toDateString() === now.toDateString();
		const isYesterday = date.toDateString() === yesterday.toDateString();

		const timeFormatter = new Intl.DateTimeFormat("en-US", {
			hour: "numeric",
			minute: "numeric",
			hour12: true
		});

		if (isToday) {
			return `Today, ${timeFormatter.format(date)}`;
		} else if (isYesterday) {
			return `Yesterday, ${timeFormatter.format(date)}`;
		} else {
			const dateFormatter = new Intl.DateTimeFormat("en-US", {
				month: "short",
				day: "numeric"
			});
			return `${dateFormatter.format(date)}, ${timeFormatter.format(date)}`;
		}
	};

	return (
		<div
			className="flex flex-col justify-center bg-gray-100 dark:bg-gray-800 shadow-md rounded-lg p-7 md:h-[350px]"
			data-testid="response-rate-card"
		>
			<p className="text-8xl font-bold text-blue-600 dark:text-blue-400 mb-1">{value}%</p>
			<h3 className="text-xl font-medium text-gray-700 dark:text-gray-300 mb-4">Response Rate</h3>
			<div className="flex gap-2 text-base text-gray-500 dark:text-gray-400">
				<ClockIcon className="self-center" />
				<span>Last Updated: {lastUpdated}</span>
			</div>
		</div>
	);
}
