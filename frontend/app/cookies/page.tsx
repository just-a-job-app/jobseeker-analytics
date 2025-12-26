import React from "react";


export default function CookiePolicyPage() {
	return (
		<main className="container mx-auto px-4 py-8 max-w-4xl text-gray-800 dark:text-gray-200">
			<h1 className="text-4xl font-bold mb-4">Cookie Policy</h1>
			<p className="text-base mb-8 italic">Last updated: December 26, 2025</p>

			<section className="mb-8">
				<p className="mb-4">
					This Cookie Policy explains how <strong>JustAJobApp LLC</strong> uses cookies and similar technologies to
					recognize you when you visit our website at{" "}
					<a className="text-blue-600 underline" href="https://justajobapp.com">
						justajobapp.com
					</a>
					. It explains what these technologies are, why we use them, and your rights to control our use of them.
				</p>
			</section>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">What are cookies?</h2>
			<p className="mb-4 text-sm">
				Cookies are small data files placed on your computer or mobile device when you visit a website. Cookies are
				widely used to make websites work more efficiently and to provide reporting information.
			</p>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">Why do we use cookies?</h2>
			<p className="mb-4 text-sm">
				We use first-party and third-party cookies for several reasons:
			</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>Essential cookies:</strong> Required for technical reasons to operate our website and provide
					core functionality.
				</li>
				<li>
					<strong>Analytics cookies:</strong> Enable us to understand how users interact with our site (via PostHog,
					which respects your consent preferences).
				</li>
				<li>
					<strong>Authentication cookies:</strong> Manage user sessions and secure access to your account.
				</li>
			</ul>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">Our Lightweight Consent System</h2>
			<p className="mb-4 text-sm">
				JustAJobApp uses a lightweight, privacy-first consent management approach instead of third-party consent
				platforms:
			</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>Cookie Name:</strong> <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">jaja-consent</code>
				</li>
				<li>
					<strong>Purpose:</strong> Stores your consent preference for analytics (PostHog).
				</li>
				<li>
					<strong>Duration:</strong> 365 days from acceptance or decline.
				</li>
				<li>
					<strong>Values:</strong> &quot;true&quot; (analytics enabled), &quot;false&quot; (analytics disabled), or absent
					(banner will be shown).
				</li>
				<li>
					<strong>How it works:</strong> When you first visit, a consent banner appears at the bottom of the page. Choose
					&quot;Accept&quot; to enable analytics or &quot;Decline&quot; to disable it.
				</li>
			</ul>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">Analytics Gating with PostHog</h2>
			<p className="mb-4 text-sm">
				PostHog analytics is <strong>only initialized</strong> when the <code className="bg-gray-200 dark:bg-gray-700 px-2 py-1 rounded">jaja-consent</code> cookie equals &quot;true&quot;. If you decline
				consent or have not yet responded to the banner, PostHog will not track your activity. We also respect:
			</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>Global Privacy Control (GPC):</strong> If detected, analytics is automatically disabled.
				</li>
				<li>
					<strong>Do Not Track (DNT):</strong> If enabled in your browser, analytics is automatically disabled.
				</li>
			</ul>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">Types of Cookies We Use</h2>

			<h3 className="text-xl font-semibold mb-3 mt-6">Essential Cookies</h3>
			<p className="text-sm mb-4">Strictly necessary for core functionality:</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>Authorization:</strong> Session authentication (JustAJobApp)
				</li>
				<li>
					<strong>Session:</strong> Temporary session data (JustAJobApp)
				</li>
				<li>
					<strong>_GRECAPTCHA:</strong> Bot protection (Google)
				</li>
				<li>
					<strong>__Secure-Authorization:</strong> Secure authentication (JustAJobApp)
				</li>
				<li>
					<strong>__Host-Authorization:</strong> Host-specific authentication (JustAJobApp)
				</li>
			</ul>

			<h3 className="text-xl font-semibold mb-3 mt-6">Analytics Cookies (Consent Required)</h3>
			<p className="text-sm mb-4">Only stored when you accept consent:</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>ph_..._posthog:</strong> Analytics identifier (PostHog) — only set when consent is &quot;true&quot;
				</li>
			</ul>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">How to Control Cookies</h2>
			<p className="mb-4 text-sm">
				You can control your consent preferences in two ways:
			</p>
			<ul className="list-disc list-inside space-y-2 ml-4 text-sm mb-6">
				<li>
					<strong>Consent Banner:</strong> Use the banner that appears at the bottom of the page. Click &quot;Accept&quot;
					or &quot;Decline&quot; to set your preference.
				</li>
				<li>
					<strong>Browser Controls:</strong> You can also manage cookies through your browser settings. Visit your
					browser&apos;s help section for instructions:
					<ul className="list-circle list-inside ml-6 mt-2 space-y-1">
						<li>
							<a className="text-blue-600 underline" href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener noreferrer">
								Chrome
							</a>
						</li>
						<li>
							<a className="text-blue-600 underline" href="https://support.microsoft.com/en-us/windows/delete-and-manage-cookies-168dab11-0753-043d-7c16-ede5947fc64d" target="_blank" rel="noopener noreferrer">
								Edge & Internet Explorer
							</a>
						</li>
						<li>
							<a className="text-blue-600 underline" href="https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop" target="_blank" rel="noopener noreferrer">
								Firefox
							</a>
						</li>
						<li>
							<a className="text-blue-600 underline" href="https://support.apple.com/en-ie/guide/safari/sfri11471/mac" target="_blank" rel="noopener noreferrer">
								Safari
							</a>
						</li>
					</ul>
				</li>
			</ul>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">Changes to this Policy</h2>
			<p className="mb-4 text-sm">
				We may update this Cookie Policy from time to time to reflect changes in our practices or for legal and
				regulatory reasons. Please revisit this page regularly to stay informed.
			</p>

			<h2 className="text-2xl font-semibold mb-4 border-b pb-2">Contact Us</h2>
			<p className="text-sm mb-4">
				If you have questions about our use of cookies or our consent system, please contact us at:
			</p>
			<div className="bg-gray-100 dark:bg-gray-800 p-6 rounded-lg text-sm">
				<p className="font-bold">JustAJobApp LLC</p>
				<p>2108 N St, STE N</p>
				<p>Sacramento, CA 95816</p>
				<p>United States</p>
				<p className="mt-2">
					Email:{" "}
					<a className="text-blue-600 underline" href="mailto:legal@justajobapp.com">
						legal@justajobapp.com
					</a>
				</p>
			</div>
		</main>
	);
}
