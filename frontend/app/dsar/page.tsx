import type { Metadata } from "next";

import React from "react";

export const metadata: Metadata = {
	title: "Data Subject Access Request | JustAJobApp",
	description: "Submit a data subject access request to understand what personal data we have about you."
};

export default function DSARPage() {
	return (
		<main className="container mx-auto px-4 py-8 max-w-6xl">
			<h1 className="text-3xl font-bold text-gray-900 dark:text-gray-100 mb-6">Data Subject Access Request</h1>

			<div className="prose prose-gray dark:prose-invert max-w-none mb-8">
				<p className="text-gray-700 dark:text-gray-300">
					You have the right to request information about the personal data we hold about you. Please use the
					form below to submit your data subject access request. We will respond to your request within the
					timeframes required by applicable privacy laws.
				</p>
			</div>

			<div className="w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
				<iframe
					className="w-full min-h-screen border-0"
					loading="lazy"
					sandbox="allow-scripts allow-forms allow-same-origin allow-popups"
					src="https://app.termly.io/dsar/a8dc31e4-d96a-461e-afe0-abdec759bc97"
					title="Data Subject Access Request Form"
				>
					<p className="p-4 text-gray-600 dark:text-gray-400">
						Your browser does not support iframes. Please visit{" "}
						<a
							className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 underline"
							href="https://app.termly.io/dsar/a8dc31e4-d96a-461e-afe0-abdec759bc97"
							rel="noopener noreferrer"
							target="_blank"
						>
							this link
						</a>{" "}
						to access the Data Subject Access Request form.
					</p>
				</iframe>
			</div>
		</main>
	);
}
