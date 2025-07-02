"use client";

import React, { useEffect, useState } from "react";
import { Card } from "@heroui/card";

interface SankeyDiagramProps {
	data: any[];
}

export default function SankeyDiagram({ data }: SankeyDiagramProps) {
	const [sankeyData, setSankeyData] = useState<any>(null);

	useEffect(() => {
		if (!data || data.length === 0) return;

		// Count unique company-job combinations and track statuses
		const uniqueApplications = new Set();
		const uniqueStatusCounts: { [key: string]: number } = {};
		
		data.forEach((email) => {
			// Create unique identifier for company-job combination
			const company = email.company_name?.trim() || "Unknown";
			const jobTitle = email.job_title?.trim() || "Unknown Position";
			const uniqueKey = `${company}-${jobTitle}`;
			
			// Track status
			const status = email.application_status?.trim() || "Unknown";
			
			// Track unique applications by status
			if (!uniqueApplications.has(uniqueKey)) {
				uniqueApplications.add(uniqueKey);
				uniqueStatusCounts[status] = (uniqueStatusCounts[status] || 0) + 1;
			}
		});

		// Prepare Sankey data
		const numUniqueApplications = uniqueApplications.size;
		const numOffers = uniqueStatusCounts["Offer made"] || 0;
		const numRejected = uniqueStatusCounts["Rejection"] || 0;
		const numInterview = uniqueStatusCounts["Interview invitation"] || 0;
		const numAvailability = uniqueStatusCounts["Availability request"] || 0;
		const numAssessment = uniqueStatusCounts["Assessment sent"] || 0;
		const numNoResponse = uniqueStatusCounts["Action required from company"] || 0;
		const numGhosted = uniqueStatusCounts["Applied"] || 0;

		setSankeyData({
			total: numUniqueApplications,
			offers: numOffers,
			rejected: numRejected,
			interviews: numInterview,
			availability: numAvailability,
			assessments: numAssessment,
			noResponse: numNoResponse,
			ghosted: numGhosted
		});
	}, [data]);

	if (!sankeyData || sankeyData.total === 0) {
		return null;
	}

	// SVG dimensions
	const width = 1200;
	const height = 400;
	const nodeWidth = 30;
	const nodePadding = 20;
	
	// Calculate positions
	const sourceX = 200;
	const targetX = width - 200;
	const centerY = height / 2;
	
	// Define target nodes with consistent colors
	const targets = [
		{ name: `Offers`, value: sankeyData.offers, color: "#16a34a" },
		{ name: `Rejected`, value: sankeyData.rejected, color: "#dc2626" },
		{ name: `Interviews`, value: sankeyData.interviews, color: "#06b6d4" },
		{ name: `Availability`, value: sankeyData.availability, color: "#10b981" },
		{ name: `Assessments`, value: sankeyData.assessments, color: "#eab308" },
		{ name: `Awaiting`, value: sankeyData.noResponse, color: "#6b7280" },
		{ name: `Ghosted`, value: sankeyData.ghosted, color: "#94a3b8" }
	].filter(t => t.value > 0);
	
	// Calculate vertical positions for targets
	const totalHeight = targets.length * 40 + (targets.length - 1) * nodePadding;
	const startY = (height - totalHeight) / 2;
	
	let currentY = startY;
	const links = targets.map((target, index) => {
		const linkHeight = (target.value / sankeyData.total) * 200;
		const targetY = currentY + 20;
		currentY += 40 + nodePadding;
		
		return {
			...target,
			targetY,
			linkHeight
		};
	});

	return (
		<Card className="p-6">
			<h3 className="text-lg font-semibold mb-4">Application Flow</h3>
			<div className="w-full overflow-x-auto">
				<svg width={width} height={height} viewBox={`-50 0 ${width + 100} ${height}`} className="w-full h-auto max-w-full" preserveAspectRatio="xMidYMid meet">
					{/* Source node */}
					<rect
						x={sourceX}
						y={centerY - 100}
						width={nodeWidth}
						height={200}
						fill="#3b82f6"
					/>
					<text
						x={sourceX - 10}
						y={centerY}
						textAnchor="end"
						dominantBaseline="middle"
						className="text-xs font-semibold"
						fill="#9ca3af"
					>
						Unique Applications ({sankeyData.total})
					</text>
					
					{/* Links and target nodes */}
					{links.map((link, index) => {
						const sourceY = centerY;
						const linkPath = `
							M ${sourceX + nodeWidth} ${sourceY - link.linkHeight/2}
							C ${(sourceX + targetX) / 2} ${sourceY - link.linkHeight/2},
							  ${(sourceX + targetX) / 2} ${link.targetY - link.linkHeight/2},
							  ${targetX} ${link.targetY - link.linkHeight/2}
							L ${targetX} ${link.targetY + link.linkHeight/2}
							C ${(sourceX + targetX) / 2} ${link.targetY + link.linkHeight/2},
							  ${(sourceX + targetX) / 2} ${sourceY + link.linkHeight/2},
							  ${sourceX + nodeWidth} ${sourceY + link.linkHeight/2}
							Z
						`;
						
						return (
							<g key={index}>
								{/* Link */}
								<path
									d={linkPath}
									fill={link.color}
									fillOpacity={0.3}
									stroke={link.color}
									strokeWidth={1}
								/>
								
								{/* Target node */}
								<rect
									x={targetX}
									y={link.targetY - 20}
									width={nodeWidth}
									height={40}
									fill={link.color}
								/>
								
								{/* Label with value */}
								<text
									x={targetX + nodeWidth + 10}
									y={link.targetY}
									dominantBaseline="middle"
									className="text-xs"
									fill="#9ca3af"
								>
									{link.name} ({link.value})
								</text>
							</g>
						);
					})}
				</svg>
			</div>
		</Card>
	);
}