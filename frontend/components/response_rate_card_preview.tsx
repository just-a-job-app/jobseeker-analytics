"use client";
import { useState, useEffect } from "react";

import { mockData } from "../utils/mockData";

import { ClockIcon } from "@/components/icons";

export default function ResponseRateCardPreview() {
	const [lastUpdated, setLastUpdated] = useState<string>("");
	const [value, setValue] = useState<number | null>(null);

	useEffect(() => {
		const totalApplications = mockData.length;
		const respondedApplications = mockData.filter((app) => app.application_status !== "No Response").length;

		const responseRate = totalApplications > 0 ? Math.round((respondedApplications / totalApplications) * 100) : 0;
		setValue(responseRate);

		const lastUpdatedDate = new Date();
		setLastUpdated(formatDate(lastUpdatedDate));
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
			<h3 className="text-xl font-medium text-gray-700 dark:text-gray-300 mb-4">% Response Rate</h3>
			<div className="flex gap-2 text-base text-gray-500 dark:text-gray-400">
				<ClockIcon className="self-center" />
				<span>Last Updated: {lastUpdated}</span>
			</div>
		</div>
	);
}
