"use client";

import React, { useState, useEffect } from "react";
import { Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, useDisclosure, Button } from "@heroui/react";
import { useRouter } from "next/navigation";
import { addToast } from "@heroui/toast";

import JobApplicationsDashboard, { Application } from "@/components/JobApplicationsDashboard";
import ResponseRateCard from "@/components/response_rate_card_preview";
import UniqueOpenRateChart from "@/components/response_rate_chart_preview";
import { mockData } from "@/utils/mockData";

export default function PreviewDashboard() {
	const { isOpen, onOpen, onClose } = useDisclosure();
	const [data, setData] = useState<Application[]>([]);
	const [loading, setLoading] = useState(true);
	const [downloading, setDownloading] = useState(false);

	const [currentPage, setCurrentPage] = useState(1);
	const [totalPages, setTotalPages] = useState(1);

	const router = useRouter();
	const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

	useEffect(() => {
		setLoading(true);
		const dataTimeout = setTimeout(() => {
			setData(mockData);
			setTotalPages(Math.ceil(mockData.length / 10));
			setLoading(false);
		}, 1500);

		const openTimeout = setTimeout(() => {
			onOpen();
		}, 10000);

		return () => {
			clearTimeout(dataTimeout);
			clearTimeout(openTimeout);
		};
	}, [onOpen]);

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

	// Handle CSV download
	async function downloadCsv() {
		setDownloading(true);
		// Mock CSV generation (no api call)
		const mockCsvContent =
			"Company,Status,Received,Job Title,Subject,Sender\n" +
			mockData
				.map(
					(item) =>
						`${item.company_name},${item.application_status},${new Date(item.received_at).toLocaleDateString()},${item.job_title},${item.subject},${item.email_from}`
				)
				.join("\n");

		const blob = new Blob([mockCsvContent], { type: "text/csv" });
		const link = document.createElement("a");
		const url = URL.createObjectURL(blob);
		link.href = url;
		link.download = `job_applications_${new Date().toISOString().split("T")[0]}.csv`;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		URL.revokeObjectURL(url);
		setDownloading(false);
	}

	// Handle Sankey download
	async function downloadSankey() {
		setDownloading(true);
		// Mock Sankey generation (no api call)
		// Download frontend/public/sankey_diagram.png
		const link = document.createElement("a");
		link.href = "/sankey_diagram.png";
		link.download = `sankey_diagram_${new Date().toISOString().split("T")[0]}.png`;
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		setDownloading(false);
	}

	const PromoModal = (
		<Modal backdrop="blur" isOpen={isOpen} size="xl" onClose={onClose}>
			<ModalContent>
				{(onClose) => (
					<>
						<ModalHeader className="flex flex-col gap-1">
							Enjoying the preview? Join the waitlist!
						</ModalHeader>
						<ModalBody>
							<p>
								By joining the waitlist, you'll receive updates on new features and an invitation to
								signup when we launch outside of beta.
							</p>
						</ModalBody>
						<ModalFooter>
							<Button color="danger" variant="light" onPress={onClose}>
								Close
							</Button>
							<Button color="primary" onPress={() => router.push("/")}>
								Sign Up Now
							</Button>
						</ModalFooter>
					</>
				)}
			</ModalContent>
		</Modal>
	);

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

	const previewResponseRateContent = (
		<>
			{PromoModal}
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
			responseRate={previewResponseRateContent}
			title="Preview Dashboard"
			totalPages={totalPages}
			onDownloadCsv={downloadCsv}
			onDownloadSankey={downloadSankey}
			onNextPage={nextPage}
			onPrevPage={prevPage}
			onRemoveItem={handleRemoveItem}
		/>
	);
}
