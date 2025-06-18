"use client";

import { useState } from "react";
import { Button, Card, Input } from "@heroui/react";

import { Navbar } from "@/components/navbar";
import Footer from "@/components/Footer";

const Index = () => {
	const [tab, setTab] = useState("waitlist");
	const [email, setEmail] = useState("");
	const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
	const [message, setMessage] = useState("");

	const scrollToOptions = () => {
		const optionsSection = document.getElementById("join-options");
		if (optionsSection) {
			optionsSection.scrollIntoView({ behavior: "smooth" });
		}
	};

	const handleNewsletterSignup = async (e: React.FormEvent, type: "founding" | "updates") => {
		e.preventDefault();
		setStatus("loading");

		try {
			const response = await fetch("/api/subscribe", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ email, type }),
			});

			if (!response.ok) {
				throw new Error("Subscription failed");
			}

			setStatus("success");
			setMessage(
				type === "founding"
					? "Welcome to the founding members group! We'll be in touch soon with early access details."
					: "Thanks for subscribing! You'll receive our monthly progress updates."
			);
			setEmail("");
		} catch (error) {
			setStatus("error");
			setMessage("Something went wrong. Please try again later.");
		}
	};

	return (
		<div className="flex flex-col min-h-screen">
			<main className="flex-grow bg-gradient-to-b from-background to-background/95">
				<Navbar />
				<div className="container mx-auto px-4 py-6 space-y-16">
					{/* Section 1: The Header - The Focused Hook */}
					<section className="max-w-4xl mx-auto text-center py-12">
						<h1 className="text-4xl md:text-6xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-indigo-600 leading-normal">
							Your LinkedIn Profile Says "Seeking New Opportunities." That's a Cry for Help, Not a
							Strategy.
						</h1>
						<p className="text-xl md:text-2xl text-default-500 mb-10 max-w-3xl mx-auto">
							The job search is broken. I have a blueprint for a tool that focuses on what truly
							matters—clarity and human connection—but it's not built yet. I'm looking for frustrated job
							seekers to help me create it.
						</p>
						<Button
							className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-6 text-lg h-auto"
							color="primary"
							onPress={scrollToOptions}
						>
							Help Fix the Job Search
						</Button>
					</section>

					{/* Section 2: The Problem - The Shared Frustration */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">Why Your Job Search Feels Hopeless</h2>
						<div className="prose prose-lg mx-auto text-default-600">
							<p className="text-xl mb-4">It's not your experience. It's the broken process.</p>
							<p className="mb-4">
								You're told to "network," but you don't know what to say. You're asked, "What are you
								looking for?" and you give a vague answer. You "spray and pray," sending hundreds of
								applications into a black hole, feeling more dejected with every automated rejection.
							</p>
							<p>
								This isn't a personal failure; it's a system failure. The current tools are designed for
								tracking busywork, not for building clarity or leveraging the real relationships that
								lead to offers.
							</p>
						</div>
					</section>

					{/* Section 3: The Solution - The Full Vision */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">From a Clear Message to a Landed Offer</h2>
						<div className="prose prose-lg mx-auto text-default-600">
							<p className="mb-4">
								This isn't just about another app. This is a mission to build a smarter, more humane way
								to find a job. The vision starts with a simple, powerful idea:{" "}
								<strong>Clarity is your unfair advantage.</strong>
							</p>
							<p className="mb-4">
								But a powerful message is just the beginning. It's the key that unlocks the rest of the
								process: focusing your efforts, leveraging your network, and managing the conversations
								that lead to offers.
							</p>
							<p>
								Our mission is to build a single tool that guides you through that entire journey. A
								tool I wish I had, and with your help, we can finally build it.
							</p>
						</div>
					</section>

					{/* Section 4: The Blueprint - How It Will Work */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">
							The Blueprint: From a Messy Brain Dump to a Killer One-Liner.
						</h2>
						<p className="text-center text-default-600 mb-8">
							This isn't ready yet, but here is the three-step process we are designing. Founding members
							will be the first to test it and provide feedback.
						</p>
						<div className="grid md:grid-cols-3 gap-8">
							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">Step 1: Your Raw Thoughts</h3>
									<p className="text-default-500 mb-4">
										The journey will begin with you telling the system everything that's on your
										mind—your skills, your confusing job titles, your vague ideas about company
										size.
									</p>
									<div className="bg-default-100 p-4 rounded-lg">
										<p className="text-sm italic text-default-600">
											THE INPUT: "I'm a mobile developer with around 10 years in HCM/CPG, looking
											for my next role."
										</p>
									</div>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">
										Step 2: Guided Questions to Find Your Focus
									</h3>
									<p className="text-default-500">
										The system will then ask you simple, clarifying questions to translate your
										jargon and nail down your specifics on experience, industry, and ideal work
										environment.
									</p>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">
										Step 3: Your Polished, Powerful "After"
									</h3>
									<p className="text-default-500 mb-4">
										The generator will instantly provide a clear, confident statement you can use on
										your LinkedIn profile, in your resume, and in every networking message.
									</p>
									<div className="bg-default-100 p-4 rounded-lg">
										<p className="text-sm italic text-default-600">
											THE GOAL: "Senior mobile engineer with experience in HR and retail software,
											seeking a native Android developer role at a mid-sized company in the Denver
											area."
										</p>
									</div>
								</div>
							</Card>
						</div>
					</section>

					{/* Section 5: Who This Is For */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">Are You One of Us?</h2>
						<div className="grid md:grid-cols-2 gap-8">
							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4 text-green-600">This is for you if:</h3>
									<ul className="space-y-3 text-default-600">
										<li className="flex items-start gap-2">
											<span className="text-green-500">✓</span>
											<span>
												You're so frustrated with the job search you're willing to try a
												radically new approach.
											</span>
										</li>
										<li className="flex items-start gap-2">
											<span className="text-green-500">✓</span>
											<span>
												You're excited by the idea of shaping a product from the very beginning.
											</span>
										</li>
										<li className="flex items-start gap-2">
											<span className="text-green-500">✓</span>
											<span>
												You're willing to offer feedback on early, imperfect, and even buggy
												prototypes.
											</span>
										</li>
										<li className="flex items-start gap-2">
											<span className="text-green-500">✓</span>
											<span>
												You believe a clear, confident message is the key to a better job
												search.
											</span>
										</li>
									</ul>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4 text-red-600">This is NOT for you if:</h3>
									<ul className="space-y-3 text-default-600">
										<li className="flex items-start gap-2">
											<span className="text-red-500">✗</span>
											<span>
												You're looking for a polished, feature-complete tool to use today.
											</span>
										</li>
										<li className="flex items-start gap-2">
											<span className="text-red-500">✗</span>
											<span>
												You don't have time to provide feedback or join occasional feedback
												sessions.
											</span>
										</li>
										<li className="flex items-start gap-2">
											<span className="text-red-500">✗</span>
											<span>
												You're happy with the current "spray and pray" job application process.
											</span>
										</li>
									</ul>
								</div>
							</Card>
						</div>
					</section>

					{/* Section 6: The Founder & The Ask */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">
							This Started as a Sketch in My Notebook.
						</h2>
						<div className="prose prose-lg mx-auto text-default-600">
							<p className="mb-4">
								My name is Lianna Novitz, and after my own soul-crushing job search post-layoff, I
								became obsessed with finding a better way. Just a Job App (JAJA) is my answer.
							</p>
							<p className="mb-4">
								To be perfectly clear: the tool I've described on this page is still a vision. The code
								isn't finished. The features aren't built. Right now, it's a blueprint and a passionate
								belief that we can fix this.
							</p>
							<p>
								I'm not asking you to buy a product. I'm asking you to believe in a mission and to join
								a small, dedicated group of founding jobseekers to help me build it right. Your voice and
								your experience are more valuable than any line of code I could write right now.
							</p>
						</div>
					</section>

					{/* Section 7: The Final CTA */}
					<section id="join-options" className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">Help Fix the Job Search</h2>
						{status === "success" && (
							<div className="mb-8 p-4 bg-green-100 text-green-800 rounded-lg text-center">
								{message}
							</div>
						)}
						{status === "error" && (
							<div className="mb-8 p-4 bg-red-100 text-red-800 rounded-lg text-center">
								{message}
							</div>
						)}
						<div className="grid md:grid-cols-2 gap-8">
							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">Option 1: Become an Insider</h3>
									<p className="text-default-500 mb-6">
										Tired of applying into a black hole? Get exclusive access to our private beta and help shape a tool that puts jobseekers first.
									</p>
									<form className="space-y-4" onSubmit={(e) => handleNewsletterSignup(e, "founding")}>
										<Input
											className="w-full"
											placeholder="Your Email Address"
											type="email"
											value={email}
											onChange={(e) => setEmail(e.target.value)}
											required
											disabled={status === "loading"}
										/>
										<Button
											className="w-full bg-purple-600 hover:bg-purple-700"
											color="primary"
											type="submit"
											isLoading={status === "loading"}
										>
											I Want Insider Access
										</Button>
									</form>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">Option 2: Follow the Launch</h3>
									<p className="text-default-500 mb-6">
										Want to see if we can actually build a better way to find work? Sign up and we'll only email you with major milestone updates.
									</p>
									<form className="space-y-4" onSubmit={(e) => handleNewsletterSignup(e, "updates")}>
										<Input
											className="w-full"
											placeholder="Your Email Address"
											type="email"
											value={email}
											onChange={(e) => setEmail(e.target.value)}
											required
											disabled={status === "loading"}
										/>
										<Button 
											className="w-full" 
											type="submit" 
											variant="bordered"
											isLoading={status === "loading"}
										>
											Keep Me Posted
										</Button>
									</form>
								</div>
							</Card>
						</div>
					</section>
				</div>
			</main>

			<Footer />
		</div>
	);
};

export default Index;
