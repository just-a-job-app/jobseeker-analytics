"use client";

import { useState } from "react";
import { Button } from "@heroui/react";
import Image from "next/image";

import FeedbackSidebar from "@/components/FeedbackSidebar";

export default function FeedbackButton() {
	const [isOpen, setIsOpen] = useState(false);

	return (
		<>
			<Button
				isIconOnly
				aria-label="Feedback"
				className="fixed bottom-4 right-4 z-50"
				onPress={() => setIsOpen(!isOpen)}
			>
				<Image alt="Feedback" height={100} src="/feedback-icon.png" width={100} />
			</Button>
			{isOpen && (
				<div className="fixed bottom-20 right-4 z-50">
					<FeedbackSidebar className="w-80 shadow-xl" />
				</div>
			)}
		</>
	);
}
