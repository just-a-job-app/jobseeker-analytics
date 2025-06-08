"use client";
import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { addToast } from "@heroui/toast";
import React from "react";

import JobApplicationsDashboard, { Application } from "@/components/JobApplicationsDashboard";
import ResponseRateCard from "@/components/response_rate_card";
import UniqueOpenRateChart from "@/components/response_rate_chart";
import { checkAuth } from "@/utils/auth";

export default function Dashboard() {
	const router = useRouter();
	const [data, setData] = useState<Application[]>([]);
	const [loading, setLoading] = useState(true);
	const [downloading, setDownloading] = useState(false);
	const [error, setError] = useState<string | null>(null);
	const [currentPage, setCurrentPage] = useState(1);
	const [totalPages, setTotalPages] = useState(1);
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
			console.error("Error deleting item:", error);
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

	return (
		<JobApplicationsDashboard
			currentPage={currentPage}
			data={data}
			downloading={downloading}
			loading={loading}
			responseRate={responseRateContent}
			totalPages={totalPages}
			onDownloadCsv={downloadCsv}
			onDownloadSankey={downloadSankey}
			onNextPage={nextPage}
			onPrevPage={prevPage}
			onRemoveItem={handleRemoveItem}
		/>
	);
}
