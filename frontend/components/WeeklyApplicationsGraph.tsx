"use client";

import React, { useEffect, useState } from "react";
import { Card } from "@heroui/card";

interface WeeklyApplicationsGraphProps {
	data: any[];
}

export default function WeeklyApplicationsGraph({ data }: WeeklyApplicationsGraphProps) {
	const [weeklyData, setWeeklyData] = useState<any[]>([]);

	useEffect(() => {
		if (!data || data.length === 0) return;

		// Group by week tracking unique company-job combinations
		const weeklyMap: { [key: string]: Set<string> } = {};
		
		data.forEach((item) => {
			const date = new Date(item.received_at);
			// Get start of week (Monday)
			const dayOfWeek = date.getDay();
			const diff = date.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
			const startOfWeek = new Date(date.setDate(diff));
			startOfWeek.setHours(0, 0, 0, 0);
			
			const weekKey = startOfWeek.toISOString().split('T')[0];
			
			// Create unique identifier for company-job combination
			const company = item.company_name?.trim() || "Unknown";
			const jobTitle = item.job_title?.trim() || "Unknown Position";
			const uniqueKey = `${company}-${jobTitle}`;
			
			if (!weeklyMap[weekKey]) {
				weeklyMap[weekKey] = new Set();
			}
			weeklyMap[weekKey].add(uniqueKey);
		});

		// Convert to array and sort
		const sortedWeeks = Object.entries(weeklyMap)
			.map(([week, uniqueApps]) => ({
				week,
				count: uniqueApps.size,
				label: new Date(week).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
			}))
			.sort((a, b) => a.week.localeCompare(b.week));

		setWeeklyData(sortedWeeks);
	}, [data]);

	if (!weeklyData || weeklyData.length === 0) {
		return null;
	}

	// Calculate chart dimensions
	const width = 1200;
	const height = 350;
	const padding = { top: 20, right: 60, bottom: 80, left: 60 };
	const chartWidth = width - padding.left - padding.right;
	const chartHeight = height - padding.top - padding.bottom;

	// Calculate scales
	const maxCount = Math.max(...weeklyData.map(d => d.count));
	const yScale = (value: number) => chartHeight - (value / maxCount) * chartHeight;
	const xScale = (index: number) => (index / (weeklyData.length - 1)) * chartWidth;

	// Create path for line
	const linePath = weeklyData
		.map((item, index) => {
			const x = xScale(index);
			const y = yScale(item.count);
			return index === 0 ? `M ${x} ${y}` : `L ${x} ${y}`;
		})
		.join(" ");

	// Create Y-axis labels
	const yAxisLabels = [];
	const yLabelCount = 5;
	for (let i = 0; i <= yLabelCount; i++) {
		const value = Math.round((maxCount / yLabelCount) * i);
		const y = yScale(value);
		yAxisLabels.push({ value, y });
	}

	return (
		<Card className="p-6">
			<h3 className="text-lg font-semibold mb-4">Weekly Job Applications</h3>
			<div className="w-full overflow-x-auto">
				<svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} className="w-full h-auto max-w-full" preserveAspectRatio="xMidYMid meet">
					<g transform={`translate(${padding.left}, ${padding.top})`}>
						{/* Y-axis */}
						<line
							x1={0}
							y1={0}
							x2={0}
							y2={chartHeight}
							stroke="#e5e7eb"
							strokeWidth="2"
						/>
						
						{/* X-axis */}
						<line
							x1={0}
							y1={chartHeight}
							x2={chartWidth}
							y2={chartHeight}
							stroke="#e5e7eb"
							strokeWidth="2"
						/>

						{/* Y-axis labels */}
						{yAxisLabels.map((label, index) => (
							<g key={index}>
								<line
									x1={0}
									y1={label.y}
									x2={chartWidth}
									y2={label.y}
									stroke="#f3f4f6"
									strokeWidth="1"
								/>
								<text
									x={-10}
									y={label.y}
									textAnchor="end"
									dominantBaseline="middle"
									className="text-sm fill-gray-600"
								>
									{label.value}
								</text>
							</g>
						))}

						{/* Bars */}
						{weeklyData.map((item, index) => {
							const x = xScale(index);
							const y = yScale(item.count);
							const barWidth = chartWidth / weeklyData.length * 0.6;
							const barX = x - barWidth / 2;

							return (
								<g key={index}>
									{/* Bar */}
									<rect
										x={barX}
										y={y}
										width={barWidth}
										height={chartHeight - y}
										fill="#3b82f6"
										fillOpacity="0.3"
										className="hover:fill-opacity-50 transition-all"
									/>
									
									{/* Data point */}
									<circle
										cx={x}
										cy={y}
										r="5"
										fill="#1e40af"
										className="hover:r-7 transition-all"
									/>
									
									{/* Value label */}
									<text
										x={x}
										y={y - 10}
										textAnchor="middle"
										className="text-sm font-semibold fill-gray-700"
									>
										{item.count}
									</text>
									
									{/* X-axis label */}
									<text
										x={x}
										y={chartHeight + 20}
										textAnchor="middle"
										className="text-xs fill-gray-600"
										transform={`rotate(-45 ${x} ${chartHeight + 25})`}
									>
										{item.label}
									</text>
								</g>
							);
						})}

						{/* Line */}
						<path
							d={linePath}
							fill="none"
							stroke="#2563eb"
							strokeWidth="3"
						/>
					</g>
				</svg>
			</div>
			
			{/* Summary */}
			<div className="mt-4 text-sm text-gray-600">
				<p>Total unique applications: {weeklyData.reduce((sum, week) => sum + week.count, 0)} over {weeklyData.length} weeks</p>
				<p>Average per week: {(weeklyData.reduce((sum, week) => sum + week.count, 0) / weeklyData.length).toFixed(1)}</p>
			</div>
		</Card>
	);
}