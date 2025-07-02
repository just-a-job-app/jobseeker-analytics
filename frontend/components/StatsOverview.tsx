"use client";

import React from "react";
import { Card } from "@heroui/card";

interface StatsOverviewProps {
	stats: any;
	loading: boolean;
}

export default function StatsOverview({ stats, loading }: StatsOverviewProps) {
	if (loading) {
		return <div className="p-4">Loading statistics...</div>;
	}

	if (!stats) {
		return null;
	}

	const { overview, status_breakdown, activity, top_companies } = stats;

	return (
		<div className="w-full space-y-6">
			{/* Overview Cards */}
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
				<Card className="p-4">
					<div className="text-sm text-gray-600 dark:text-gray-400">Total Applications</div>
					<div className="text-2xl font-bold">{overview.total_applications}</div>
				</Card>
				<Card className="p-4">
					<div className="text-sm text-gray-600 dark:text-gray-400">Unique Companies</div>
					<div className="text-2xl font-bold">{overview.unique_companies}</div>
				</Card>
				<Card className="p-4">
					<div className="text-sm text-gray-600 dark:text-gray-400">Active Days</div>
					<div className="text-2xl font-bold">{overview.days_active}</div>
				</Card>
			</div>

			{/* Status Breakdown */}
			<Card className="p-6">
				<h3 className="text-lg font-semibold mb-4">Application Status Breakdown</h3>
				<div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Interviews</div>
						<div className="text-xl font-semibold text-cyan-600">{status_breakdown.interviews}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Rejections</div>
						<div className="text-xl font-semibold text-red-600">{status_breakdown.rejections}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Offers</div>
						<div className="text-xl font-semibold text-green-600">{status_breakdown.offers}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Assessments</div>
						<div className="text-xl font-semibold text-yellow-600">{status_breakdown.assessments}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Awaiting Response</div>
						<div className="text-xl font-semibold text-gray-600">{status_breakdown.awaiting_response}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Availability Requests</div>
						<div className="text-xl font-semibold text-emerald-600">{status_breakdown.availability_requests}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Info Requests</div>
						<div className="text-xl font-semibold text-teal-600">{status_breakdown.information_requests}</div>
					</div>
					<div>
						<div className="text-sm text-gray-600 dark:text-gray-400">Inbound Requests</div>
						<div className="text-xl font-semibold text-purple-600">{status_breakdown.inbound_requests}</div>
					</div>
				</div>
			</Card>

			{/* Activity Metrics */}
			<div className="grid grid-cols-1 md:grid-cols-3 gap-4">
				<Card className="p-4">
					<div className="text-sm text-gray-600 dark:text-gray-400">Last 7 Days</div>
					<div className="text-2xl font-bold">{activity.last_7_days}</div>
					<div className="text-xs text-gray-500">applications</div>
				</Card>
				<Card className="p-4">
					<div className="text-sm text-gray-600 dark:text-gray-400">Last 30 Days</div>
					<div className="text-2xl font-bold">{activity.last_30_days}</div>
					<div className="text-xs text-gray-500">applications</div>
				</Card>
				<Card className="p-4">
					<div className="text-sm text-gray-600 dark:text-gray-400">Average Per Week</div>
					<div className="text-2xl font-bold">{activity.avg_per_week}</div>
					<div className="text-xs text-gray-500">applications</div>
				</Card>
			</div>

		</div>
	);
}