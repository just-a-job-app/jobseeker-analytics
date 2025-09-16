"use client";

import { useState } from "react";
import { Button } from "@heroui/react";

import Footer from "@/components/Footer";

export default function LandingClient() {
	const [showImagePopup, setShowImagePopup] = useState(false);
	const [popupImageSrc, setPopupImageSrc] = useState("");

	return (
		<div className="flex flex-col min-h-screen">
			<main className="flex-grow bg-gradient-to-b from-background to-background/95">
				<div className="container mx-auto px-4 py-6">
					<div className="text-center">
						<h1 className="text-2xl font-bold tracking-tight sm:text-3xl bg-clip-text text-transparent bg-gradient-to-r pb-6 from-amber-600 to-emerald-600">
							9 out of 10 applications are met with rejection or silence.
						</h1>
						<p className="text-4xl font-bold tracking-tight sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r pb-6 from-amber-600 to-emerald-600">
							We're building the platform to make yours the one they can't ignore.
						</p>
						<p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
							We're creating a new tool for ambitious professionals, combining a smart application tracker
							with a game that gets you real feedback. Our private beta is currently full, but you can
							request early access to our next release.
						</p>
						<div className="mt-10 flex items-center justify-center gap-x-6">
							<Button
								as="a"
								className="bg-amber-600 text-white hover:bg-amber-700"
								href="#waitlist"
								size="lg"
								variant="solid"
								onPress={() => {
									// Add fireworks animation to waitlist section
									const waitlistSection = document.getElementById("waitlist");
									if (waitlistSection) {
										// Import the function dynamically to avoid circular dependencies
										import("@/components/Footer").then((module) => {
											const { createFireworkEffect } = module;
											waitlistSection.classList.add("golden-sparkle-border");
											createFireworkEffect(waitlistSection);
											setTimeout(() => {
												waitlistSection.classList.remove("golden-sparkle-border");
											}, 2000);
										});
									}
								}}
							>
								Request Early Access
							</Button>
						</div>
						<p className="mt-4 text-sm text-gray-500">
							Sign up to be first in line when we open more spots.
						</p>
					</div>
				</div>
			</main>

			{/* Social Proof Bar */}
			<div className="bg-white dark:bg-gray-900 py-12">
				<div className="mx-auto max-w-7xl px-6 lg:px-8">
					<div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
						<div className="flex flex-col items-center">
							<svg
								className="h-10 w-10 mb-2 text-gray-700 dark:text-gray-300"
								fill="none"
								stroke="currentColor"
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth="2"
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22" />
							</svg>
							<h3 className="text-lg font-semibold">Featured on GitHub</h3>
							<p className="text-sm text-gray-600 dark:text-gray-400">
								As seen on their official YouTube channel with over 500,000 subscribers.
							</p>
						</div>
						<div className="flex flex-col items-center">
							<svg
								className="h-10 w-10 mb-2 text-amber-500"
								fill="currentColor"
								stroke="currentColor"
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth="1"
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
							>
								<polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
							</svg>
							<h3 className="text-lg font-semibold">Trusted by Developers</h3>
							<p className="text-sm text-gray-600 dark:text-gray-400">
								A 42% increase in GitHub stars after our feature, validating our approach.
							</p>
						</div>
						<div className="flex flex-col items-center">
							<svg
								className="h-10 w-10 mb-2 text-emerald-500"
								fill="none"
								stroke="currentColor"
								strokeLinecap="round"
								strokeLinejoin="round"
								strokeWidth="2"
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
								<circle cx="9" cy="7" r="4" />
								<path d="M23 21v-2a4 4 0 0 0-3-3.87" />
								<path d="M16 3.13a4 4 0 0 1 0 7.75" />
							</svg>
							<h3 className="text-lg font-semibold">Join The Waitlist</h3>
							<p className="text-sm text-gray-600 dark:text-gray-400">
								300+ professionals have already signed up organically to get early access.
							</p>
						</div>
					</div>
				</div>
			</div>

			{/* The rest of the landing content remains unchanged below */}

			{/* Problem/Agitation Section */}
			<div className="container mx-auto px-4 py-24 sm:py-32">
				<div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
					<div>
						{/* Chart image with click functionality */}
						<div
							className="bg-gray-200 dark:bg-gray-700 h-80 w-full rounded-lg flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity"
							onClick={() => {
								setPopupImageSrc("homepage/Problem2.png");
								setShowImagePopup(true);
							}}
						>
							<div className="relative">
								<img
									alt="Chart showing Applications Per Hire tripling"
									className="max-h-80 max-w-full object-contain"
									src="homepage/Problem.png"
								/>
								<div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-20 opacity-0 hover:opacity-100 transition-opacity">
									<svg
										className="h-12 w-12 text-white"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
										xmlns="http://www.w3.org/2000/svg"
									>
										<path
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v6m4-3H6"
											strokeLinecap="round"
											strokeLinejoin="round"
											strokeWidth={2}
										/>
									</svg>
								</div>
							</div>
						</div>
					</div>
					<div>
						<h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
							The Job Search is Officially Broken. It's Not Just You.
						</h2>
						<p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
							Does this sound familiar? You spend hours tailoring your resume and writing the perfect
							cover letter, only to send it into a black hole. Days turn into weeks. The only reply is a
							generic rejection email, or worse, complete silence.
						</p>
						<p className="mt-4 text-lg leading-8 text-gray-600 dark:text-gray-300">
							You're not imagining it. The game has changed:
						</p>
						<ul className="mt-6 space-y-4 text-gray-600 dark:text-gray-300">
							<li>
								<strong className="font-semibold text-gray-900 dark:text-white">
									It's 3x more competitive:
								</strong>{" "}
								The number of applications per hire has tripled since early 2021. (Source: AshbyHQ)
							</li>
							<li>
								<strong className="font-semibold text-gray-900 dark:text-white">
									It's overwhelming:
								</strong>{" "}
								Our research shows 77% of job seekers use over three different tools to manage a process
								64% already find frustrating.
							</li>
							<li>
								<strong className="font-semibold text-gray-900 dark:text-white">
									It's leading to burnout:
								</strong>{" "}
								64% of applicants report feeling exhausted and stuck. (Source: Huntr)
							</li>
						</ul>
						<p className="mt-6 text-lg leading-8 text-gray-600 dark:text-gray-300">
							You're left wondering, "Is my experience not good enough?" when the real problem is you're
							playing a game with no rules and no scoreboard.
						</p>
					</div>
				</div>
			</div>

			{/* The rest of the sections, CTA, waitlist, and footer */}
			<div className="bg-white dark:bg-gray-900 py-24 sm:py-32">
				<div className="mx-auto max-w-7xl px-6 lg:px-8">{/* ... existing content unchanged ... */}</div>
			</div>

			<section id="waitlist" className="max-w-4xl mx-auto py-16">
				<div className="bg-gradient-to-r from-amber-50 to-emerald-50 dark:from-amber-950/30 dark:to-emerald-950/30 rounded-xl p-8 border border-amber-200 dark:border-amber-800/50 text-center transition-all">
					<h2 className="text-3xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-amber-600 to-emerald-600 dark:from-amber-500 dark:to-emerald-400">
						Get the Unfair Advantage in Your Job Search
					</h2>
					<p className="text-lg text-gray-700 dark:text-gray-300 mb-8 leading-relaxed">
						Join 300+ ambitious professionals on the priority list. We'll give you early access to the tools
						that turn your hidden achievements into your next big opportunity. Your search is 100%
						confidential.
					</p>
					<div className="flex justify-center mb-8">
						<div className="dark:opacity-70" style={{ position: "relative", overflow: "auto" }}>
							<iframe
								src="https://app.formbricks.com/s/cmf667qha4ahcyg01nu13lsgo?embed=true&source=JustAJobAppLandingPageEmbed"
								style={{ width: "400px", height: "270px", border: 0 }}
								className="rounded-md dark:border dark:border-gray-700"
							/>
						</div>
					</div>
				</div>
			</section>
			<Footer />

			{/* Image Popup Overlay */}
			{showImagePopup && (
				<div
					className="fixed inset-0 bg-black bg-opacity-80 z-50 flex items-center justify-center p-4"
					onClick={() => setShowImagePopup(false)}
				>
					<div className="relative w-full max-w-6xl">
						<button
							className="absolute -top-12 right-0 text-white hover:text-amber-500 focus:outline-none"
							onClick={(e) => {
								e.stopPropagation();
								setShowImagePopup(false);
							}}
						>
							<svg
								className="h-8 w-8"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M6 18L18 6M6 6l12 12"
									strokeLinecap="round"
									strokeLinejoin="round"
									strokeWidth={2}
								/>
							</svg>
						</button>
						<div className="bg-white flex justify-center dark:bg-gray-800 p-6 rounded-lg shadow-2xl overflow-hidden">
							<img
								alt="Enlarged image"
								className="h-auto"
								src={popupImageSrc}
								style={{ maxHeight: "90vh" }}
								onClick={(e) => e.stopPropagation()}
							/>
						</div>
					</div>
				</div>
			)}
		</div>
	);
}
