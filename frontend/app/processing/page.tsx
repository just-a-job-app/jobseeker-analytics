"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { addToast, Progress } from "@heroui/react";

import Spinner from "../../components/spinner";

import { checkAuth } from "@/utils/auth";

const ProcessingPage = () => {
	const router = useRouter();
	const apiUrl = process.env.NEXT_PUBLIC_API_URL!;
	const [progress, setProgress] = useState(0);
	const [showCancelMessage, setShowCancelMessage] = useState(false);
	const [isCancelling, setIsCancelling] = useState(false);
	const [intervalId, setIntervalId] = useState<NodeJS.Timeout | null>(null);

	useEffect(() => {
		const process = async () => {
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

			// Set up timer to show cancel message after 10 minutes
			const cancelTimer = setTimeout(
				() => {
					setShowCancelMessage(true);
				},
				10 * 60 * 1000
			); // 10 minutes in milliseconds

			const interval = setInterval(async () => {
				try {
					const res = await fetch(`${apiUrl}/processing`, {
						method: "GET",
						credentials: "include"
					});

					const result = await res.json();
					const total = Number(result.total_emails);
					const processed = Number(result.processed_emails);
					console.log(`Progress update: ${processed}/${total} - ${result.message}`);

					if (!total || isNaN(total)) {
						setProgress(100);
					} else {
						setProgress(100 * (processed / total));
					}
					if (result.message === "Processing complete") {
						clearInterval(interval);
						clearTimeout(cancelTimer);
						// Force a full page refresh to ensure new user status is checked
						window.location.href = "/dashboard";
					} else if (result.message === "Processing cancelled") {
						clearInterval(interval);
						clearTimeout(cancelTimer);
						addToast({
							title: "Processing was cancelled",
							color: "warning"
						});
						// Force a full page refresh to ensure new user status is checked
						window.location.href = "/dashboard";
					}
				} catch {
					clearTimeout(cancelTimer);
					router.push("/logout");
				}
			}, 3000);

			setIntervalId(interval);
			return () => {
				clearInterval(interval);
				clearTimeout(cancelTimer);
			};
		};

		process();
	}, [router]);

	const handleCancel = async () => {
		setIsCancelling(true);
		try {
			const response = await fetch(`${apiUrl}/cancel-fetch-emails`, {
				method: "POST",
				credentials: "include"
			});

			if (response.ok) {
				if (intervalId) {
					clearInterval(intervalId);
				}
				addToast({
					title: "Processing cancelled successfully",
					color: "success"
				});
				// Force a full page refresh to ensure new user status is checked
				window.location.href = "/dashboard";
			} else {
				const result = await response.json();
				addToast({
					title: result.detail || "Failed to cancel processing",
					color: "danger"
				});
			}
		} catch (error) {
			addToast({
				title: "Error cancelling processing",
				color: "danger"
			});
		} finally {
			setIsCancelling(false);
		}
	};

	return (
		<div className="flex flex-col items-center justify-center h-full">
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
				{showCancelMessage && (
					<p className="text-sm text-gray-500 mt-2">
						Taking too long?{" "}
						<button
							className="underline hover:text-gray-700 disabled:opacity-50"
							disabled={isCancelling}
							onClick={handleCancel}
						>
							{isCancelling ? "Cancelling..." : "Cancel the process"}
						</button>
					</p>
				)}
			</div>
		</div>
	);
};

export default ProcessingPage;
