import { useState } from "react";
import { Button, Card, Textarea, Input, Tabs, Tab } from "@heroui/react";

import { MessageSquareIcon, BugIcon } from "@/components/icons";

interface FeedbackSidebarProps {
	className?: string;
}

export default function FeedbackSidebar({ className = "" }: FeedbackSidebarProps) {
	const [activeTab, setActiveTab] = useState("feedback");
	const [feedback, setFeedback] = useState("");
	const [issueTitle, setIssueTitle] = useState("");
	const [issueDescription, setIssueDescription] = useState("");
	const [isSubmitting, setIsSubmitting] = useState(false);
	const [submitStatus, setSubmitStatus] = useState<"idle" | "success" | "error">("idle");

	const handleFeedbackSubmit = async () => {
		if (!feedback.trim()) return;

		setIsSubmitting(true);
		setSubmitStatus("idle");

		try {
			const response = await fetch("/api/feedback", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ message: feedback })
			});

			if (!response.ok) throw new Error("Failed to submit feedback");

			setSubmitStatus("success");
			setFeedback("");
		} catch (error) {
			setSubmitStatus("error");
		} finally {
			setIsSubmitting(false);
		}
	};

	const handleIssueSubmit = async () => {
		if (!issueTitle.trim() || !issueDescription.trim()) return;

		setIsSubmitting(true);
		setSubmitStatus("idle");

		try {
			const response = await fetch("/api/issues", {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					title: issueTitle,
					description: issueDescription
				})
			});

			if (!response.ok) throw new Error("Failed to submit issue");

			setSubmitStatus("success");
			setIssueTitle("");
			setIssueDescription("");
		} catch (error) {
			setSubmitStatus("error");
		} finally {
			setIsSubmitting(false);
		}
	};

	return (
		<Card className={`p-4 ${className}`}>
			<Tabs
				aria-label="Feedback Options"
				selectedKey={activeTab}
				onSelectionChange={(key) => setActiveTab(key as string)}
			>
				<Tab
					key="feedback"
					title={
						<div className="flex items-center gap-2">
							<MessageSquareIcon size={16} />
							<span>Feedback</span>
						</div>
					}
				>
					<div className="mt-4 space-y-4">
						<Textarea
							label="Your Feedback"
							minRows={4}
							placeholder="Tell us what you think..."
							value={feedback}
							onChange={(e) => setFeedback(e.target.value)}
						/>
						<Button
							className="w-full"
							color="primary"
							isLoading={isSubmitting}
							onPress={handleFeedbackSubmit}
						>
							Submit Feedback
						</Button>
						{submitStatus === "success" && (
							<p className="text-green-500 text-sm">Thank you for your feedback!</p>
						)}
						{submitStatus === "error" && (
							<p className="text-red-500 text-sm">Failed to submit feedback. Please try again.</p>
						)}
					</div>
				</Tab>

				<Tab
					key="issue"
					title={
						<div className="flex items-center gap-2">
							<BugIcon size={16} />
							<span>Report Issue</span>
						</div>
					}
				>
					<div className="mt-4 space-y-4">
						<Input
							label="Issue Title"
							placeholder="Brief description of the issue"
							value={issueTitle}
							onChange={(e) => setIssueTitle(e.target.value)}
						/>
						<Textarea
							label="Issue Description"
							minRows={4}
							placeholder="Please describe the issue in detail..."
							value={issueDescription}
							onChange={(e) => setIssueDescription(e.target.value)}
						/>
						<Button className="w-full" color="primary" isLoading={isSubmitting} onPress={handleIssueSubmit}>
							Submit Issue
						</Button>
						{submitStatus === "success" && (
							<p className="text-green-500 text-sm">Issue reported successfully!</p>
						)}
						{submitStatus === "error" && (
							<p className="text-red-500 text-sm">Failed to submit issue. Please try again.</p>
						)}
					</div>
				</Tab>
			</Tabs>
		</Card>
	);
}
