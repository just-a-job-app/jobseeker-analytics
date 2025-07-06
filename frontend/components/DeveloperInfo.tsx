import { useState } from "react";
import { Button, Card, Input } from "@heroui/react";
import { addToast } from "@heroui/toast";

import { CodeIcon, EmailIcon, ExternalLinkIcon, CalendarIcon } from "@/components/icons";

const DeveloperInfo = () => {
	const [email, setEmail] = useState("");
	const [isSubmitting, setIsSubmitting] = useState(false);

	const handleSetupRequest = async () => {
		if (!email || !email.includes("@")) {
			addToast({
				title: "Please enter your email first",
				color: "danger"
			});
			return;
		}

		setIsSubmitting(true);

		try {
			const response = await fetch("/api/subscribe", {
				method: "POST",
				headers: {
					"Content-Type": "application/json"
				},
				body: JSON.stringify({
					email,
					formType: "setup"
				})
			});

			const data = await response.json();

			if (data.success) {
				addToast({
					title: "Setup session requested!",
					description: "Check your email for next steps.",
					color: "success"
				});
				setEmail("");
			} else {
				addToast({
					title: "Something went wrong",
					description: data.message || "Please try again later.",
					color: "danger"
				});
			}
		} catch (error) {
			console.error("Error requesting setup session:", error);
			addToast({
				title: "Connection error",
				description: "Please check your network and try again.",
				color: "danger"
			});
		} finally {
			setIsSubmitting(false);
		}
	};

	return (
		<Card className="p-6 md:p-8" id="developerInfoCard">
			<div className="space-y-4">
				<div className="flex items-center gap-2 text-purple-600 font-semibold">
					<span className="bg-purple-100 text-purple-800 p-1 rounded-full">
						<CodeIcon size={16} />
					</span>
					Option 2: Run Locally
				</div>

				<h3 className="text-2xl font-bold">Use the app right away on your computer</h3>
				<p className="text-default-500">
					Don't want to wait? You can install the application directly on your personal computer by following
					these steps:
				</p>

				{/* Removed the background div that was causing issues */}
				<div className="space-y-6 pt-2">
					<div className="space-y-3 border-l-4 border-purple-500 pl-4">
						<h4 className="font-semibold">1. For beginners</h4>
						<p className="text-sm text-default-500">
							If you're not familiar with git, let us guide you through the installation process. Request
							a setup session and our team will help you get started.
						</p>
						<div>
							<Input
								fullWidth
								className="mb-2"
								id="request-setup-session-email-input"
								placeholder="Your email address"
								type="email"
								value={email}
								onChange={(e) => setEmail(e.target.value)}
							/>
							<Button
								className="mt-2 w-full bg-purple-600 hover:bg-purple-700"
								color="primary"
								id="request-setup-session-button"
								isDisabled={isSubmitting}
								startContent={<CalendarIcon size={16} />}
								onPress={handleSetupRequest}
							>
								{isSubmitting ? "Requesting..." : "Book Setup Session"}
							</Button>
						</div>
					</div>

					<div className="space-y-3 border-l-4 border-default-300 dark:border-default-600 pl-4">
						<h4 className="font-semibold">2. For experienced developers</h4>
						<p className="text-sm text-default-500">
							If you're familiar with git, the CONTRIBUTING.md file in our repository contains setup
							instructions.
						</p>
						<Button
							startContent={<CodeIcon size={16} />}
							variant="bordered"
							onPress={() =>
								window.open(
									"https://github.com/lnovitz/jobseeker-analytics/blob/main/CONTRIBUTING.md",
									"_blank"
								)
							}
						>
							View on GitHub
						</Button>
					</div>
				</div>

				<div className="border-t border-default-200 dark:border-default-700 pt-4 mt-6">
					<h4 className="font-semibold mb-2">Support & Feedback</h4>
					<div className="space-y-2">
						<a
							aria-label="Join our Discord server"
							className="flex items-center gap-2 text-sm text-primary hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
							href="https://discord.gg/gsdpMchCam"
							rel="noopener noreferrer"
							target="_blank"
						>
							<ExternalLinkIcon size={16} />
							Join our Discord
						</a>
						<a
							aria-label="Email help@justajobapp.com for support"
							className="flex items-center gap-2 text-sm text-primary hover:text-primary-600 dark:hover:text-primary-400 transition-colors"
							href="mailto:help@justajobapp.com"
						>
							<EmailIcon size={16} />
							Email help@justajobapp.com
						</a>
					</div>
				</div>
			</div>
		</Card>
	);
};

export default DeveloperInfo;
