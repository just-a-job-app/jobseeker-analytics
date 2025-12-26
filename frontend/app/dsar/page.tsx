import type { Metadata } from "next";

import React from "react";
import { Card, Button } from "@heroui/react";

export const metadata: Metadata = {
	title: "Data Subject Access Request | JustAJobApp",
	description: "Submit a data subject access request to understand what personal data we have about you."
};

export default function DSARPage() {
	return (
		<main className="container mx-auto px-4 py-8 max-w-2xl">
			<h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-6">Data Subject Access Request</h1>

			<div className="mb-8">
				<p className="text-gray-700 dark:text-gray-300 mb-4">
					Under applicable privacy laws (CCPA, GDPR, and other state privacy laws), you have the right to:
				</p>
				<ul className="list-disc list-inside space-y-2 text-gray-700 dark:text-gray-300 ml-2">
					<li>Request access to the personal data we hold about you</li>
					<li>Request correction of inaccurate information</li>
					<li>Request deletion of your personal data (subject to legal obligations)</li>
					<li>Request to limit use of sensitive personal information</li>
					<li>Opt-out of targeted advertising or data sales</li>
				</ul>
			</div>

			<Card className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-gray-800 dark:to-gray-900 border border-blue-200 dark:border-gray-700">
				<div className="p-8">
					<h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">Submit a Privacy Request</h2>

					<p className="text-gray-700 dark:text-gray-300 mb-6">
						To submit a Data Subject Access Request, deletion request, correction request, or any other
						privacy-related inquiry, please email us directly. We will verify your identity and respond to
						your request within the timeframes required by applicable privacy laws (typically 45 days).
					</p>

					<div className="bg-white dark:bg-gray-800 rounded-lg p-4 mb-6 border border-gray-200 dark:border-gray-700">
						<p className="text-sm font-mono text-gray-800 dark:text-gray-200 break-all">
							<strong>Email:</strong>{" "}
							<a
								className="text-blue-600 dark:text-blue-400 hover:underline"
								href="mailto:privacy@justajobapp.com"
							>
								privacy@justajobapp.com
							</a>
						</p>
					</div>

					<div className="mb-6">
						<p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
							<strong>In your email, please include:</strong>
						</p>
						<ul className="list-disc list-inside space-y-2 text-sm text-gray-600 dark:text-gray-400 ml-2">
							<li>Your full name and email address associated with your JustAJobApp account</li>
							<li>The type of request (access, deletion, correction, etc.)</li>
							<li>A brief description of your request</li>
							<li>Any relevant details to help us locate your data</li>
						</ul>
					</div>

					<Button
						as="a"
						className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium w-full"
						href="mailto:privacy@justajobapp.com?subject=Privacy%20Request%20-%20JustAJobApp"
						size="lg"
					>
						Send Privacy Request Email
					</Button>
				</div>
			</Card>

			<div className="mt-8 p-6 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
				<h3 className="text-lg font-semibold mb-3 text-gray-900 dark:text-white">Authorized Agents</h3>
				<p className="text-sm text-gray-700 dark:text-gray-300 mb-2">
					If you wish to designate an authorized agent to submit a request on your behalf, you may do so by
					contacting us at{" "}
					<a className="text-blue-600 dark:text-blue-400 hover:underline" href="mailto:privacy@justajobapp.com">
						privacy@justajobapp.com
					</a>
					. We may require written proof of the agent's permission and verification of your identity.
				</p>
			</div>
		</main>
	);
}
