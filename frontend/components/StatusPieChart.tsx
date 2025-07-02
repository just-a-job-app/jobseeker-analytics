"use client";

import React, { useEffect, useState } from "react";
import { Card } from "@heroui/card";

interface StatusPieChartProps {
	data: any[];
}

export default function StatusPieChart({ data }: StatusPieChartProps) {
	const [chartData, setChartData] = useState<any[]>([]);

	useEffect(() => {
		if (!data || data.length === 0) return;

		// Count statuses
		const statusCounts: { [key: string]: number } = {};
		data.forEach((item) => {
			const status = item.application_status?.trim() || "Unknown";
			statusCounts[status] = (statusCounts[status] || 0) + 1;
		});

		// Convert to chart data format
		const pieData = Object.entries(statusCounts)
			.map(([status, count]) => ({
				name: status,
				value: count,
				percentage: ((count / data.length) * 100).toFixed(1)
			}))
			.sort((a, b) => b.value - a.value);

		setChartData(pieData);
	}, [data]);

	// Define colors for each status
	const getStatusColor = (status: string) => {
		const colorMap: { [key: string]: string } = {
			"Rejection": "#dc2626",
			"Interview invitation": "#06b6d4",
			"Offer made": "#16a34a",
			"Applied": "#94a3b8",
			"Assessment sent": "#eab308",
			"Availability request": "#10b981",
			"Information request": "#14b8a6",
			"Action required from company": "#6b7280",
			"Did not apply - inbound request": "#9333ea",
			"Hiring freeze notification": "#f97316",
			"Withdrew application": "#ec4899",
			"False positive": "#f59e0b"
		};
		return colorMap[status] || "#94a3b8";
	};

	if (!chartData || chartData.length === 0) {
		return null;
	}

	// Calculate SVG dimensions
	const width = 400;
	const height = 400;
	const radius = Math.min(width, height) / 2 - 40;
	const centerX = width / 2;
	const centerY = height / 2;

	// Create pie chart paths
	let currentAngle = -Math.PI / 2; // Start from top
	const paths = chartData.map((item, index) => {
		const startAngle = currentAngle;
		const angle = (item.value / data.length) * 2 * Math.PI;
		currentAngle += angle;
		const endAngle = currentAngle;

		// Calculate path
		const x1 = centerX + radius * Math.cos(startAngle);
		const y1 = centerY + radius * Math.sin(startAngle);
		const x2 = centerX + radius * Math.cos(endAngle);
		const y2 = centerY + radius * Math.sin(endAngle);

		const largeArc = angle > Math.PI ? 1 : 0;

		const pathData = [
			`M ${centerX} ${centerY}`,
			`L ${x1} ${y1}`,
			`A ${radius} ${radius} 0 ${largeArc} 1 ${x2} ${y2}`,
			`Z`
		].join(" ");

		// Calculate label position
		const labelAngle = startAngle + angle / 2;
		const labelRadius = radius * 0.7;
		const labelX = centerX + labelRadius * Math.cos(labelAngle);
		const labelY = centerY + labelRadius * Math.sin(labelAngle);

		return {
			path: pathData,
			color: getStatusColor(item.name),
			label: item.value > data.length * 0.03 ? `${item.percentage}%` : "", // Only show label if > 3%
			labelX,
			labelY,
			name: item.name,
			value: item.value,
			percentage: item.percentage
		};
	});

	return (
		<Card className="p-6">
			<h3 className="text-lg font-semibold mb-4">Application Status Distribution</h3>
			<div className="flex flex-col lg:flex-row items-center gap-8">
				{/* Pie Chart */}
				<div className="relative flex-shrink-0">
					<svg width={width} height={height}>
						{paths.map((item, index) => (
							<g key={index}>
								<path
									d={item.path}
									fill={item.color}
									stroke="white"
									strokeWidth="1"
									className="hover:opacity-80 transition-opacity cursor-pointer"
								/>
								{item.label && (
									<text
										x={item.labelX}
										y={item.labelY}
										textAnchor="middle"
										dominantBaseline="middle"
										className="fill-white text-sm font-semibold pointer-events-none"
									>
										{item.label}
									</text>
								)}
							</g>
						))}
					</svg>
				</div>

				{/* Legend - Two Columns */}
				<div className="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-2 w-full">
					{paths.map((item, index) => (
						<div key={index} className="flex items-center gap-2 text-sm">
							<div
								className="w-4 h-4 rounded flex-shrink-0"
								style={{ backgroundColor: item.color }}
							/>
							<span className="flex-1 truncate">{item.name}</span>
							<span className="font-semibold whitespace-nowrap">{item.value} ({item.percentage}%)</span>
						</div>
					))}
				</div>
			</div>
		</Card>
	);
}