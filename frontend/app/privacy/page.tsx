import React from "react";

const PrivacyPolicyPage = () => {
	return (
		<main className="container mx-auto px-4 py-8 text-gray-800 dark:text-gray-200">
			<h1 className="text-4xl font-bold mb-4">Privacy Notice</h1>
			<p className="text-base mb-8 italic">Effective Date: December 25, 2025</p>

			{/* GUIDING PRINCIPLES */}
			<section className="mb-8">
				<p>
					This Privacy Notice for <strong>JustAJobApp LLC</strong> (doing business as{" "}
					<strong>JustAJobApp</strong>) establishes the protocols for the collection, storage, and processing
					of personal information when using our services, including the web application hosted at{" "}
					<a className="text-blue-600 underline" href="https://justajobapp.com">
						justajobapp.com
					</a>
					. Our operations prioritize transparency and data minimization. We do not request personal
					information unless required for core service functionality, i.e.{" "}
					<strong>increasing job search productivity</strong>.
				</p>
			</section>

			{/* CATEGORIES OF PERSONAL INFORMATION WE COLLECT */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">
				Categories of Personal Information We Collect
			</h2>
			<p className="text-sm mb-4">
				The table below shows the categories of personal information we have collected in the past twelve (12)
				months. For a comprehensive inventory of all personal information we process, please refer to the
				section "Notice at Collection: Categories of Information."
			</p>
			<div className="overflow-x-auto mb-6">
				<table className="min-w-full border border-gray-300 text-sm">
					<thead className="bg-gray-100 dark:bg-gray-800">
						<tr>
							<th className="border p-2 text-left">Category</th>
							<th className="border p-2 text-left">Examples</th>
							<th className="border p-2 text-left">Collected</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td className="border p-2 font-semibold">A. Identifiers</td>
							<td className="border p-2">
								Email address and refresh token used for OAuth 2.0 authentication, IP addresses logged
								for security monitoring.
							</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">
								B. Personal Information (California Customer Records)
							</td>
							<td className="border p-2">
								Email address and/or refresh token used for OAuth 2.0 authentication, IP addresses
								logged for security monitoring, employment application history (company name, job title)
							</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">C. Protected Classification Characteristics</td>
							<td className="border p-2">
								Gender, age, date of birth, race, ethnicity, national origin, marital status,
								demographic data
							</td>
							<td className="border p-2">NO</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">D. Commercial Information</td>
							<td className="border p-2">
								Subscription status, transaction timestamps, and payment metadata processed via Stripe
								for premium access.
							</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">E. Biometric Information</td>
							<td className="border p-2">Fingerprints, voiceprints</td>
							<td className="border p-2">NO</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">F. Internet or Network Activity</td>
							<td className="border p-2">
								Clickstream data, feature usage logs, and Session Replays (visual interaction logs)
								captured via PostHog.
							</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">G. Geolocation Data</td>
							<td className="border p-2">Device location</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">H. Audio, Electronic, Sensory Information</td>
							<td className="border p-2">
								Visual Session Replays of website interactions captured via PostHog to analyze UI/UX
								friction points.
							</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">I. Professional or Employment Information</td>
							<td className="border p-2">
								Job titles, hiring company names, and application status extracted from processed
								emails.
							</td>
							<td className="border p-2">YES</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">J. Education Information</td>
							<td className="border p-2">Student records, directory information</td>
							<td className="border p-2">NO</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">K. Inferences Drawn from Personal Information</td>
							<td className="border p-2">
								Inferences about preferences, characteristics, behavior, and interests
							</td>
							<td className="border p-2">NO</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">L. Sensitive Personal Information</td>
							<td className="border p-2">
								Gmail mailbox contents; specifically, the metadata of messages identified by the{" "}
								<a
									className="text-blue-600 underline"
									href="https://github.com/JustAJobApp/jobseeker-analytics/blob/main/backend/email_query_filters/applied_email_filter.yaml"
								>
									applied_email_filter.yaml
								</a>{" "}
								logic. Account login information.
							</td>
							<td className="border p-2">YES</td>
						</tr>
					</tbody>
				</table>
			</div>

			<h3 className="text-xl font-semibold mb-3 mt-6">Use and Retention of Sensitive Personal Information</h3>
			<p className="text-sm mb-4">
				We only collect sensitive personal information as defined by applicable privacy laws for purposes
				allowed by law or with your consent. Sensitive personal information may be used or disclosed to a
				service provider or contractor for additional, specified purposes. You may have the right to limit the
				use or disclosure of your sensitive personal information. We do not collect or process sensitive
				personal information for the purpose of inferring characteristics about you.
			</p>
			<p className="text-sm mb-4">
				We will use and retain the collected personal information as needed to provide the Services or for:
			</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>Category A (Identifiers):</strong> As long as the user has an account with us
				</li>
				<li>
					<strong>Category F (Internet Activity):</strong> As long as the user has an account with us
				</li>
				<li>
					<strong>Category G (Geolocation):</strong> As long as the user has an account with us
				</li>
				<li>
					<strong>Category I (Professional Information):</strong> As long as the user has an account with us
				</li>
				<li>
					<strong>Category L (Sensitive Personal Information):</strong> As long as the user has an account
					with us
				</li>
			</ul>
			{/* 1. CALIFORNIA NOTICE AT COLLECTION */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">
				1. Notice at Collection: Categories of Information
			</h2>
			<div className="overflow-x-auto">
				<table className="min-w-full border border-gray-300 mb-4 text-sm">
					<thead className="bg-gray-100 dark:bg-gray-800">
						<tr>
							<th className="border p-2 text-left">Category</th>
							<th className="border p-2 text-left">Business Purpose</th>
							<th className="border p-2 text-left">Retention Period</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td className="border p-2 font-semibold">Category A: Identifiers</td>
							<td className="border p-2">
								Account authentication, security monitoring, and session management.
							</td>
							<td className="border p-2">Duration of active account.</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">
								Category D: Commercial Information (Transaction Records)
							</td>
							<td className="border p-2">Subscription processing via Stripe.</td>
							<td className="border p-2">7 Years (IRS record-keeping).</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">Category G: Geolocation Data</td>
							<td className="border p-2">
								Device location tracking for user analytics and session management.
							</td>
							<td className="border p-2">Duration of active account.</td>
						</tr>
						<tr>
							<td className="border p-2 font-semibold">
								Category L: Sensitive Personal Information (Mailbox Contents)
							</td>
							<td className="border p-2">Automated job tracking and status extraction.</td>
							<td className="border p-2">Duration of active account.</td>
						</tr>
					</tbody>
				</table>
			</div>

			{/* 2. THIRD-PARTY DISCLOSURES */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">2. Third-Party Service Providers</h2>
			<p className="mb-4 text-sm">
				We utilize specific third-party vendors to maintain our infrastructure. These parties are contractually
				prohibited from processing your data for any purpose other than those instructed by JustAJobApp LLC:
			</p>
			<div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm mb-6">
				<div className="p-3 border rounded bg-gray-50 dark:bg-gray-900">
					<p className="font-bold">Core Infrastructure</p>
					<ul className="list-disc list-inside">
						<li>
							<strong>Cloud:</strong> AWS, Google Cloud Platform
						</li>
						<li>
							<strong>Payments:</strong> Stripe
						</li>
						<li>
							<strong>Auth:</strong> Google OAuth 2.0
						</li>
						<li>
							<strong>Analytics:</strong> PostHog (with consent gating)
						</li>
					</ul>
				</div>
				<div className="p-3 border rounded bg-gray-50 dark:bg-gray-900">
					<p className="font-bold">Communication & AI</p>
					<ul className="list-disc list-inside">
						<li>
							<strong>Messaging:</strong> Systeme.io, ConvertKit, MailerLite
						</li>
						<li>
							<strong>AI Processing:</strong> Google Cloud AI, Google Gemini API
						</li>
						<li>
							<strong>Consent Management:</strong> Lightweight cookie-based system
						</li>
					</ul>
				</div>
			</div>

			{/* 3. CONSENT MANAGEMENT */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">3. Consent Management</h2>
			<p className="text-sm mb-4">
				JustAJobApp uses a lightweight, privacy-first consent management system to respect your preferences:
			</p>
			<ul className="list-disc list-inside space-y-3 ml-4 text-sm">
				<li>
					<strong>Cookie-Based Consent:</strong> We store your consent preference in a cookie named{" "}
					<code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">jaja-consent</code>. This cookie
					expires after 365 days.
				</li>
				<li>
					<strong>Analytics Gating:</strong> PostHog analytics is only initialized when you accept the consent
					banner. If you decline or have not yet responded, analytics will not track your activity.
				</li>
				<li>
					<strong>GPC & Do Not Track Respect:</strong> We honor Global Privacy Control (GPC) and Do Not Track
					(DNT) signals from your browser, automatically opting you out of analytics if detected.
				</li>
				<li>
					<strong>No Third-Party Sharing:</strong> We do not share your data with third parties for targeted
					advertising regardless of your consent choice.
				</li>
			</ul>

			{/* 3. EMAIL SYNCHRONIZATION & REFRESH TOKENS */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">
				4. Specialized Data Processing: Gmail Synchronization
			</h2>
			<p className="mt-2 text-sm">
				JustAJobApp serves as a specialized data processor using the <strong>Google OAuth2 framework</strong>{" "}
				and the <strong>Gmail API</strong>. We utilize the following technical protocols:
			</p>
			<ul className="list-disc list-inside space-y-2 mt-2 ml-4 text-sm">
				<li>
					<strong>Refresh Token Authentication:</strong> The App utilizes secure, encrypted refresh tokens
					rather than account passwords to maintain connectivity.
				</li>
				<li>
					<strong>Background Synchronization:</strong> These tokens allow the App to periodically check for
					updates or new submissions in the background without requiring active user login.
				</li>
				<li>
					<strong>Incremental Synchronization:</strong> We only request messages received after the timestamp
					of your last successfully processed email.
				</li>
			</ul>

			{/* 4. FILTERING & ANALYSIS */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">5. Targeted Data Filtering</h2>
			<p className="mt-2 text-sm">The Gmail API is filtered through three distinct layers to ensure privacy:</p>
			<ul className="list-disc list-inside space-y-3 mt-3 ml-4 text-sm">
				<li>
					<strong>Initial Discovery:</strong> Potential job-related messages are identified based on keywords
					defined in our{" "}
					<a
						className="text-blue-600 underline"
						href="https://github.com/JustAJobApp/jobseeker-analytics/blob/main/backend/email_query_filters/applied_email_filter.yaml"
					>
						applied_email_filter.yaml
					</a>
					.
				</li>
				<li>
					<strong>LLM-Based Analysis:</strong> An analysis layer defined in our{" "}
					<a
						className="text-blue-600 underline"
						href="https://github.com/JustAJobApp/jobseeker-analytics/blob/main/backend/utils/llm_utils.py"
					>
						llm_utils.py
					</a>{" "}
					utilizes programmatic filters to discard newsletters and personal data unrelated to your job search.
				</li>
				<li>
					<strong>Domain-Based Optimization:</strong> As applications are verified, future fetches may rely on
					stored email domains from verified job-related emails to maintain tracking reliability.
				</li>
			</ul>

			{/* 5. UNITED STATES DATA PROCESSING */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">
				6. International Users: United States Processing
			</h2>
			<p className="text-sm">
				JustAJobApp LLC is based in the United States and the Websites are hosted in the United States. If you
				are accessing the Websites from the European Union, Asia, or any other region with laws governing data
				collection and use that differ from U.S. law, please note that you are transferring your personal data
				to the United States.
			</p>
			<p className="mt-2 text-sm">By providing your personal data, you consent to:</p>
			<ul className="list-disc list-inside space-y-2 mt-2 ml-4 text-sm font-medium">
				<li>The use of your personal data for the specific job-tracking purposes identified above.</li>
				<li>The transfer and processing of your personal data in the United States.</li>
			</ul>

			{/* 6. GOOGLE LIMITED USE COMPLIANCE */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-b pb-2">
				7. Compliance to the Google API Services User Data Policy
			</h2>
			<p className="text-sm">
				JustAJobApp's use and transfer of data to any other app of information received from Google’s Accounts
				will adhere to the{" "}
				<a
					className="text-blue-600 underline ml-1"
					href="https://developers.google.com/terms/api-services-user-data-policy"
				>
					Google API Services User Data Policy
				</a>{" "}
				including Limited Use requirements.
			</p>
			<ul className="list-disc list-inside space-y-2 mt-2 font-medium text-sm">
				<li>NO Human Access to your data unless explicitly authorized by you for support.</li>
				<li>NO Data Transfer to third parties for targeted advertising.</li>
				<li>NO Use for AI Training: We do not use Google Workspace data to train generalized AI/ML models.</li>
				<li>
					NO Sale or Share of Data for Minors: JustAJobApp LLC has no actual knowledge that it sells or shares
					the personal information of consumers under 16 years of age.
				</li>
			</ul>
			{/* 8. CALIFORNIA STATUTORY RIGHTS */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-t border-b pt-4 pb-2">
				8. Your California Privacy Rights (CPRA)
			</h2>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm">
				<li>
					<strong>Right to Know:</strong> Disclosure of what data points are collected.
				</li>
				<li>
					<strong>Right to Delete:</strong> Request data purge, subject to IRS guidance.
				</li>
				<li>
					<strong>Right to Correct:</strong> Rectify inaccurate personal information.
				</li>
				<li>
					<strong>Right to Opt-Out:</strong> JustAJobApp does not sell or share data for behavioral
					advertising.
				</li>
				<li>
					<strong>Right to Limit Use:</strong> We restrict mailbox data usage to core service functions.
				</li>
				{/* 7. CALIFORNIA STATUTORY RIGHTS - UPDATED */}
				<li>
					<strong>Global Privacy Control (GPC):</strong> We honor Global Privacy Control (GPC) signals. If our
					system detects a GPC signal from your browser, we will automatically opt you out of the "sharing" of
					your personal information for cross-context behavioral advertising.
				</li>
			</ul>

			<h3 className="text-xl font-semibold mb-3 mt-6">Verification Process for Privacy Requests</h3>
			<p className="text-sm mb-4">
				Under the CPRA, we are required to verify the identity of consumers making privacy requests (including
				requests to know, delete, or correct personal information). When you submit a privacy request, we will
				verify your identity by matching the email address of the requester with the email address on file
				associated with your JustAJobApp account. In some cases, we may require additional verification,
				including a signed declaration under penalty of perjury, to ensure we are processing legitimate requests
				and protecting your account security.
			</p>

			<h3 className="text-xl font-semibold mb-3 mt-6">Authorized Agents</h3>
			<p className="text-sm mb-4">
				California law requires us to allow consumers to designate an authorized agent to make requests on their
				behalf. You may designate an authorized agent to submit a request on your behalf. We may require written
				proof of the agent's permission and verify your identity directly. Please contact us at{" "}
				<a className="text-blue-600 underline" href="mailto:privacy@justajobapp.com">
					privacy@justajobapp.com
				</a>{" "}
				to designate an authorized agent.
			</p>

			{/* 9. ADMINISTRATIVE ACCESS */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-t border-b pt-4 pb-2">9. Administrative Access</h2>
			<p className="mb-6 text-sm">
				Engineers may locate individual emails related to a Job Application only in response to a bug report,
				authorized support request, or security investigation. All production data access must be specifically
				authorized by JustAJobApp LLC.
			</p>
			{/* 10. CHANGES AND UPDATES */}
			<h2 className="text-3xl font-semibold mb-4 mt-8">10. Changes and Updates to this Privacy Policy</h2>
			<p className="text-base">
				We may occasionally update this Privacy Policy. When we do, we will also revise the Effective Date at
				the top of this page. We encourage you to periodically review this Privacy Policy to stay informed about
				how we are protecting the personal information we collect. Your continued use of the Websites
				constitutes your agreement to this Privacy Policy and any updates.
			</p>

			{/* 11. US RESIDENTS PRIVACY RIGHTS */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-t border-b pt-4 pb-2">
				11. Do United States Residents Have Specific Privacy Rights?
			</h2>
			<p className="text-base mb-4">
				<strong>In Short:</strong> If you are a resident of California, Colorado, Connecticut, Delaware,
				Florida, Indiana, Iowa, Kentucky, Maryland, Minnesota, Montana, Nebraska, New Hampshire, New Jersey,
				Oregon, Rhode Island, Tennessee, Texas, Utah, or Virginia, you may have the right to request access to
				and receive details about the personal information we maintain about you and how we have processed it,
				correct inaccuracies, get a copy of, or delete your personal information. You may also have the right to
				withdraw your consent to our processing of your personal information. These rights may be limited in
				some circumstances by applicable law.
			</p>

			{/* 11. ACCESSIBILITY STATEMENT */}
			<h2 className="text-3xl font-semibold mb-4 mt-8">12. Accessibility Statement</h2>
			<p className="text-sm mb-4">
				The CCPA requires that privacy policies be accessible to consumers with disabilities. If you have a
				disability and need to access this notice in an alternative format, please contact us at{" "}
				<a className="text-blue-600 underline" href="mailto:privacy@justajobapp.com">
					privacy@justajobapp.com
				</a>
				.
			</p>

			{/* 13. CONTACT INFORMATION */}
			<h2 className="text-3xl font-semibold mb-4 mt-8 border-t pt-4">13. Contact Information</h2>
			<div className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg">
				<p className="font-bold">JustAJobApp LLC</p>
				<p>2108 N St, STE N</p>
				<p>Sacramento, CA 95816</p>
				<p>United States</p>
				<p className="mt-2 font-semibold">
					Privacy Officer:{" "}
					<a className="text-blue-600 underline" href="mailto:privacy@justajobapp.com">
						privacy@justajobapp.com
					</a>
				</p>
			</div>
		</main>
	);
};

export default PrivacyPolicyPage;
