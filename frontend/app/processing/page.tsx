"use client";
import { useEffect, useState, useRef } from "react";
import { useRouter } from "next/navigation";
import {
	addToast,
	Button,
	DatePicker,
	Progress,
	Modal,
	ModalBody,
	ModalContent,
	ModalFooter,
	ModalHeader,
	CalendarDate
} from "@heroui/react";

import Spinner from "../../components/spinner";

import { checkAuth } from "@/utils/auth";

const ProcessingPage = () => {
	const router = useRouter();
	const apiUrl = process.env.NEXT_PUBLIC_API_URL!;
	const [progress, setProgress] = useState(0);
	const [showModal, setShowModal] = useState(false);
	const [selectedDate, setSelectedDate] = useState<CalendarDate | null>(null);
	const [isSaving, setIsSaving] = useState(false);

	// Ref to store interval id for cleanup/restart
	const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

	const startProcessing = async () => {
		const isAuthenticated = await checkAuth(apiUrl);
		if (!isAuthenticated) {
			addToast({
				title: "You need to be logged in to access this page.",
				color: "warning"
			});
			router.push("/");
			return;
		}

		const interval = setInterval(async () => {
			try {
				const res = await fetch(`${apiUrl}/processing`, {
					method: "GET",
					credentials: "include"
				});

					const result = await res.json();
					const total = Number(result.total_emails);
					const processed = Number(result.processed_emails);
					if (!total || isNaN(total)) {
						setProgress(100);
					} else {
						setProgress(100 * (processed / total));
					}
					if (result.message === "Processing complete") {
						clearInterval(interval);
						router.push("/dashboard");
					}
				} catch {
					router.push("/logout");
				}
			}, 3000);
		};

	useEffect(() => {
		startProcessing();
		return () => {
			if (intervalRef.current) clearInterval(intervalRef.current);
		};
		// eslint-disable-next-line react-hooks/exhaustive-deps
	}, [router]);

	async function resetDate() {
		if (!selectedDate) return alert("Please select a start date");

		//console.log("Resetting date to:", selectedDate);
		setIsSaving(true);
		// Stop the current email fetching process
		try {
			const res = await fetch(`${apiUrl}/stop-fetch-emails`, {
				method: "POST",
				credentials: "include"
			});
			if (!res.ok) {
				throw new Error("Failed to stop email fetching");
			}
			// Change the start date
			await changeStartDate(selectedDate);
			// Delete all emails for the user
			const delRes = await fetch(`${apiUrl}/delete-emails`, {
				method: "DELETE",
				credentials: "include"
			});
			if (!delRes.ok) {
				throw new Error("Failed to delete emails");
			}
			// Restart the process
			if (intervalRef.current) clearInterval(intervalRef.current);
			setShowModal(false);
			setProgress(0);
			await startProcessing();
		} catch (error) {
			addToast({
				title: "Error resetting process",
				description: error instanceof Error ? error.message : "Unknown error",
				color: "danger"
			});
		} finally {
			setIsSaving(false);
		}
	}

	async function changeStartDate(selectedDate: CalendarDate | null) {
		if (!selectedDate) return;
		const formattedDate = `${selectedDate.year}-${String(selectedDate.month).padStart(2, "0")}-${String(selectedDate.day).padStart(2, "0")}`;

		const response = await fetch(`${apiUrl}/change-start-date`, {
			method: "PUT",
			headers: { "Content-Type": "application/x-www-form-urlencoded" },
			body: new URLSearchParams({ new_start_date: formattedDate.toString() }),
			credentials: "include"
		});

		if (!response.ok) throw new Error("Failed to change start date");
		console.log("Start date changed successfully:", formattedDate);
		addToast({
			title: "Start date changed successfully",
			description: `Your job search start date has been set to ${formattedDate}.`,
			color: "success"
		});
		setSelectedDate(null); // Clear the selected date after saving
	}

	return (
		<div className="flex flex-col items-center justify-center h-full">
			<Modal isOpen={showModal} onOpenChange={setShowModal}>
				<ModalContent>
					<ModalHeader>Select Your Job Search Start Date</ModalHeader>
					<ModalBody>
						<DatePicker value={selectedDate} onChange={setSelectedDate} />
					</ModalBody>
					<ModalFooter>
						<Button color="primary" isLoading={isSaving} onPress={resetDate}>
							Reset
						</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
			<div className="flex flex-col items-center justify-center">
				<h1 className="text-3xl font-semibold mb-4">We are hard at work!</h1>
				<Spinner />
				<div className="mb-3" />
				<Progress
					aria-label="Downloading..."
					className="max-w-md"
					showValueLabel={true}
					size="md"
					value={progress}
				/>
				<div className="mb-3" />
				<p className="text-lg mt-4">
					Eating rejections for dinner. You will be redirected to your dashboard soon.
				</p>
				<p className="text-sm text-gray-500 mt-2">
					Taking too long?{" "}
					<a onClick={() => setShowModal(true)}>
						<u>Reset the date</u>
					</a>
				</p>
			</div>
		</div>
	);
};

export default ProcessingPage;
