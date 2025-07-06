"use client";
import { BarChart, Bar, XAxis, YAxis, Cell, ResponsiveContainer, Tooltip, CartesianGrid } from "recharts";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { addToast } from "@heroui/react";

interface ResponseData {
	title: string;
	rate: number;
}

const BLUE_COLOR = "#3b82f6";

export default function JobTitleResponseChart() {
	const router = useRouter();
	const [activeIndex, setActiveIndex] = useState<number | null>(null);
	const [data, setData] = useState<ResponseData[]>([]);
	const [isDarkMode, setIsDarkMode] = useState(false);

	const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

	useEffect(() => {
		const checkDarkMode = () => {
			setIsDarkMode(document.documentElement.classList.contains("dark"));
		};

		checkDarkMode();

		const observer = new MutationObserver(checkDarkMode);
		observer.observe(document.documentElement, { attributes: true, attributeFilter: ["class"] });

		return () => observer.disconnect();
	}, []);

	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await fetch(`${apiUrl}/get-response-rate`, {
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

				if (result.length === 0) {
					console.warn("Empty response");
				} else {
					setData(result);
				}
			} catch {
				addToast({
					title: "Connection Error",
					description: "Failed to fetch response rate data",
					color: "danger"
				});
			}
		};

		fetchData();
	}, [router]);

	return (
		<div className="bg-gray-100 dark:bg-gray-800 p-6 shadow-md rounded-lg" data-testid="response-rate-chart">
			<div className="flex justify-between items-center mb-6">
				<h2 className="text-gray-700 dark:text-gray-300 text-base md:text-xl font-semibold">
					Response Rate based on Job Titles
				</h2>
			</div>

			<div className="h-[250px] overflow-x-auto">
				<div className="min-w-[600px] h-full">
					<ResponsiveContainer height="100%" width="100%">
						<BarChart
							data={data}
							margin={{ top: 5, right: 20, left: 0, bottom: 70 }}
							onMouseLeave={() => setActiveIndex(null)}
						>
							<defs>
								<linearGradient id="barGradient" x1="0" x2="0" y1="0" y2="1">
									<stop offset="0%" stopColor="#60a5fa" /> {/* Lighter blue */}
									<stop offset="100%" stopColor={BLUE_COLOR} /> {/* Your exact blue */}
								</linearGradient>
							</defs>

							<YAxis
								axisLine={{ stroke: "#334155" }}
								domain={[0, 100]}
								tick={{ fill: "#94a3b8", fontSize: 12 }}
								tickLine={{ stroke: "#334155" }}
								type="number"
							/>

							<CartesianGrid horizontal={true} stroke="#1e293b" strokeDasharray="3 3" vertical={false} />

							<XAxis
								angle={-45}
								axisLine={{ stroke: "#334155" }}
								dataKey="title"
								height={30}
								interval={0}
								textAnchor="end"
								tick={{ fill: isDarkMode ? "#e0e0e0" : "#616161", fontSize: 12 }}
								tickLine={{ stroke: "#334155" }}
								type="category"
							/>

							<Tooltip
								contentStyle={{
									background: "#1e293b",
									borderColor: BLUE_COLOR, // Blue border to match
									borderRadius: "6px",
									color: "#f8fafc"
								}}
								cursor={{ fill: "rgba(59, 130, 246, 0.1)" }} // Blue tint
								formatter={(value: number) => [`${value}%`, "Response Rate"]}
								itemStyle={{
									color: "#f8fafc" // Ensures tooltip items (formatter output) are white
								}}
							/>

							<Bar
								animationDuration={1000}
								dataKey="rate"
								name="Response Rate"
								radius={[4, 4, 0, 0]}
								onMouseEnter={(_, index) => setActiveIndex(index)}
							>
								{data.map((entry, index) => (
									<Cell
										key={`cell-${index}`}
										fill={index === activeIndex ? "url(#barGradient)" : BLUE_COLOR}
										stroke={index === activeIndex ? "#93c5fd" : "none"} // Light blue border on hover
										strokeWidth={index === activeIndex ? 2 : 0}
									/>
								))}
							</Bar>
						</BarChart>
					</ResponsiveContainer>
				</div>
			</div>
		</div>
	);
}
