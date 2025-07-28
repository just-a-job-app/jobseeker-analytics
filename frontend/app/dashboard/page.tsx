"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { addToast } from "@heroui/toast";
import React from "react";
import { Sankey, ResponsiveContainer, Tooltip } from "recharts";

import JobApplicationsDashboard, { Application } from "@/components/JobApplicationsDashboard";
import ResponseRateCard from "@/components/response_rate_card";
import UniqueOpenRateChart from "@/components/response_rate_chart";
import { checkAuth } from "@/utils/auth";

interface SankeyData {
	nodes: { name: string }[];
	links: { source: number; target: number; value: number }[];
}

export default function Dashboard() {
	const router = useRouter();
	const [data, setData] = useState<Application[]>([]);
	const [loading, setLoading] = useState(true);
	const [downloading, setDownloading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [currentPage, setCurrentPage] = useState(1);
	const [totalPages, setTotalPages] = useState(1);
	const [sankeyData, setSankeyData] = useState<SankeyData | null>(null);
	const [searchTerm, setSearchTerm] = useState("");
	const [filteredData, setFilteredData] = useState<Application[]>([]);
	const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

	useEffect(() => {
		const fetchData = async () => {
			try {
				// Check if user is logged in
				const isAuthenticated = await checkAuth(apiUrl);
				if (!isAuthenticated) {
					addToast({
						title: "You need to be logged in to access this page.",
						color: "warning"
					});
					router.push("/");
					return;
				}

				// Fetch applicaions (if user is logged in)
				const response = await fetch(`${apiUrl}/get-emails?page=${currentPage}`, {
					method: "GET",
					credentials: "include" // Include cookies for session management
				});

				if (!response.ok) {
					if (response.status === 404) {
						setError("No applications found");
					} else {
						throw new Error(`HTTP error! status: ${response.status}`);
					}
				}

				const result = await response.json();
				setTotalPages(result.totalPages);

				setData(result);
			} catch {
				setError("Failed to load applications");
			} finally {
				setLoading(false);
			}
		};

		fetchData();
	}, [apiUrl, router, currentPage]);

	useEffect(() => {
		// Fetch Sankey data
		const fetchSankey = async () => {
			try {
				const response = await fetch(`${apiUrl}/get-sankey-data`, {
					method: "GET",
					credentials: "include"
				});
				if (response.ok) {
					const result = await response.json();
					setSankeyData(result);
				}
			} catch {
				// ignore for now
			}
		};
		fetchSankey();
	}, [apiUrl, router, currentPage]);

	// Filter data based on search term
	useEffect(() => {
		if (searchTerm.trim() === "") {
			setFilteredData(data);
		} else {
			const filtered = data.filter((item) => item.company_name.toLowerCase().includes(searchTerm.toLowerCase()));
			setFilteredData(filtered);
		}
	}, [data, searchTerm]);

	const nextPage = () => {
		if (currentPage < totalPages) {
			setCurrentPage(currentPage + 1);
		}
	};

	const prevPage = () => {
		if (currentPage > 1) {
			setCurrentPage(currentPage - 1);
		}
	};

	async function downloadCsv() {
		setDownloading(true);
		try {
			const response = await fetch(`${apiUrl}/process-csv`, {
				method: "GET",
				credentials: "include"
			});

			if (!response.ok) {
				let description = "Something went wrong. Please try again.";

				if (response.status === 429) {
					description = "Download limit reached. Please wait before trying again.";
				} else {
					description = "Please try again or contact help@justajobapp.com if the issue persists.";
				}

				addToast({
					title: "Failed to download CSV",
					description,
					color: "danger"
				});

				return;
			}

			// Create a download link to trigger the file download
			const blob = await response.blob();
			const link = document.createElement("a");
			const url = URL.createObjectURL(blob);
			link.href = url;
			link.download = `job_applications_${new Date().toISOString().split("T")[0]}.csv`;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			URL.revokeObjectURL(url);
		} catch {
			addToast({
				title: "Something went wrong",
				description: "Please try again",
				color: "danger"
			});
		} finally {
			setDownloading(false);
		}
	}

	if (error) {
		return (
			<div className="p-6 flex flex-col items-center justify-center min-h-[50vh]">
				<p className="text-red-600 mb-4">{error}</p>
				<button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={() => window.location.reload()}>
					Retry
				</button>
			</div>
		);
	}

	async function downloadSankey() {
		setDownloading(true);
		try {
			const response = await fetch(`${apiUrl}/process-sankey`, {
				method: "GET",
				credentials: "include"
			});

			if (!response.ok) {
				let description = "Something went wrong. Please try again.";

				if (response.status === 429) {
					description = "Download limit reached. Please wait before trying again.";
				} else {
					description = "Please try again or contact help@justajobapp.com if the issue persists.";
				}

				addToast({
					title: "Failed to download Sankey Diagram",
					description,
					color: "danger"
				});

				return;
			}

			// Create a download link to trigger the file download
			const blob = await response.blob();
			const link = document.createElement("a");
			const url = URL.createObjectURL(blob);
			link.href = url;
			link.download = `sankey_diagram_${new Date().toISOString().split("T")[0]}.png`;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			URL.revokeObjectURL(url);
		} catch {
			addToast({
				title: "Something went wrong",
				description: "Please try again",
				color: "danger"
			});
		} finally {
			setDownloading(false);
		}
	}

	const handleRemoveItem = async (id: string) => {
		try {
			// Make a DELETE request to the backend
			const response = await fetch(`${apiUrl}/delete-email/${id}`, {
				method: "DELETE",
				credentials: "include" // Include cookies for authentication
			});

			if (!response.ok) {
				throw new Error("Failed to delete the item");
			}

			// If the deletion is successful, update the local state
			setData((prevData) => prevData.filter((item) => item.id !== id));

			addToast({
				title: "Item removed successfully",
				color: "success"
			});
		} catch (error) {
			addToast({
				title: "Failed to remove item",
				description: "Please try again or contact support.",
				color: "danger"
			});
		}
	};

	const responseRateContent = (
		<>
			<div className="flex flex-col gap-4 mt-4 mb-6 md:flex-row">
				<div className="w-full md:w-[30%]">
					<ResponseRateCard />
				</div>
				<div className="md:w-[70%]">
					<UniqueOpenRateChart />
				</div>
			</div>
		</>
	);

	const sankeyChartContent =
		sankeyData && sankeyData.nodes && sankeyData.nodes.length > 0 ? (
			<div className="bg-gray-100 dark:bg-gray-800 p-6 shadow-md rounded-lg">
				<div className="flex items-center justify-between mb-4">
					<h2 className="text-gray-700 dark:text-gray-300 text-base md:text-xl font-semibold">
						My Job Search
					</h2>
					<button
						className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
						disabled={downloading}
						onClick={downloadSankey}
					>
						{downloading ? "Downloading..." : "Download PNG"}
					</button>
				</div>
				<div className="h-[450px] w-full relative">
					<ResponsiveContainer height="100%" width="100%">
						<Sankey
							data={sankeyData}
							link={{ stroke: "#cbd5e1", strokeOpacity: 0.4 }}
							margin={{ top: 10, bottom: 30, left: 10, right: 10 }} // Smaller margins
							node={(props) => {
								const isSource = props.x < 50;
								const nodeName = props.payload.name;
								const status = nodeName.split(" (")[0];

								const getStatusColor = (status: string) => {
									const normalized = status.toLowerCase();
									switch (normalized) {
										case "applications":
											return "#3b82f6"; // Blue for source
										case "offer made":
											return "#10b981";
										case "rejection":
											return "#ef4444";
										case "interview invitation":
											return "#06b6d4";
										case "assessment sent":
											return "#8b5cf6";
										case "availability request":
											return "#f59e0b";
										case "application confirmation":
											return "#3b82f6";
										case "information request":
											return "#6b7280";
										case "inbound request":
											return "#10b981";
										case "action required":
											return "#84cc16";
										case "hiring freeze":
											return "#8b5cf6";
										case "withdrew application":
											return "#ec4899";
										default:
											return "#8884d8";
									}
								};

								return (
									<g>
										<rect
											fill={getStatusColor(status)}
											fillOpacity={0.8}
											height={props.height}
											stroke={getStatusColor(status)}
											width={props.width}
											x={props.x}
											y={props.y}
										/>
										<text
											dominantBaseline="middle"
											fill="#333"
											fontSize={12}
											textAnchor={isSource ? "start" : "end"}
											x={isSource ? props.x + props.width + 8 : props.x - 8}
											y={props.y + props.height / 2}
										>
											{props.payload.name}
										</text>
									</g>
								);
							}}
							nodePadding={24}
						>
							<Tooltip
								content={({ active, payload }) => {
									if (active && payload && payload.length) {
										const { sourceNode, targetNode, value } = payload[0].payload;
										return (
											<div className="bg-white p-2 rounded shadow">
												<div>
													<strong>
														{sourceNode?.name} → {targetNode?.name}
													</strong>
												</div>
												<div>Count: {value}</div>
											</div>
										);
									}
									return null;
								}}
							/>
						</Sankey>
					</ResponsiveContainer>
					<div className="absolute bottom-2 left-2 text-xs text-gray-500 opacity-70">
						{(() => {
							// Calculate date range from the data
							if (data && data.length > 0) {
								const dates = data
									.map((item) => (item.received_at ? new Date(item.received_at) : null))
									.filter((date) => date !== null);

								if (dates.length > 0) {
									const minDate = new Date(Math.min(...dates.map((d) => d.getTime())));
									const maxDate = new Date(Math.max(...dates.map((d) => d.getTime())));

									const formatDate = (date: Date) => {
										const month = date.toLocaleDateString("en-US", { month: "long" });
										const year = date.getFullYear();
										return { month, year };
									};

									const minFormatted = formatDate(minDate);
									const maxFormatted = formatDate(maxDate);

									let dateRange;
									if (minFormatted.year === maxFormatted.year) {
										dateRange = `${minFormatted.month} - ${maxFormatted.month} ${maxFormatted.year}`;
									} else {
										dateRange = `${minFormatted.month} ${minFormatted.year} - ${maxFormatted.month} ${maxFormatted.year}`;
									}

									return `JustAJobApp.com • ${dateRange}`;
								}
							}
							return "JustAJobApp.com";
						})()}
					</div>
				</div>
			</div>
		) : null;

	return (
		<JobApplicationsDashboard
			currentPage={currentPage}
			data={filteredData}
			downloading={downloading}
			loading={loading}
			responseRate={responseRateContent}
			sankeyChart={sankeyChartContent}
			searchTerm={searchTerm}
			totalPages={totalPages}
			onDownloadCsv={downloadCsv}
			onDownloadSankey={downloadSankey}
			onNextPage={nextPage}
			onPrevPage={prevPage}
			onRemoveItem={handleRemoveItem}
			onSearchChange={setSearchTerm}
		/>
	);
}
