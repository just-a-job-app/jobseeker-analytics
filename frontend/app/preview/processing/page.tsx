"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { addToast, Progress } from "@heroui/react";

import Spinner from "../../../components/spinner";

export default function PreviewProcessing() {
	const router = useRouter();
	const [progress, setProgress] = useState(0);

	useEffect(() => {
		addToast({
			title: "Previewing the app...",
			description: "We are processing our sample data",
			color: "warning",
			timeout: 5000
		});

		// Set an interval to update progress and a timeout to redirect after 5 seconds
		const interval = setInterval(() => {
			setProgress((prev) => (prev >= 100 ? 100 : prev + 10));
		}, 500);

		// Redirect after 5 seconds
		const timeout = setTimeout(() => {
			clearInterval(interval);
			router.push("/preview/dashboard");
		}, 5000);

		return () => {
			clearInterval(interval);
			clearTimeout(timeout);
		};
	}, [router]);

	return (
		<div className="flex flex-col items-center justify-center h-full">
			<div className="flex flex-col items-center justify-center">
				<h1 className="text-3xl font-semibold mb-4">We are processing your job!</h1>
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
					Your job is being processed. You will be redirected to the download page once it&#39;s ready.
				</p>
			</div>
		</div>
	);
}
