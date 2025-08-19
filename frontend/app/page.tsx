"use client";

import { useState } from "react";
import { Button, Card, Tabs, Tab } from "@heroui/react";

import { 
	LineChartIcon, 
	CheckCircle2Icon, 
	PlayIcon,
	InfoIcon,
	CodeIcon,
	MessageSquareIcon,
	DownloadIcon,
	ChevronRightIcon
} from "@/components/icons";
import { Navbar } from "@/components/navbar";
import Footer from "@/components/Footer";
import WaitlistForm from "@/components/WaitlistForm";
import DeveloperInfo from "@/components/DeveloperInfo";
import HeroSection from "@/components/HeroSection";

const Index = () => {
	const [tab, setTab] = useState("waitlist");

	const handleWatchDemo = () => {
		window.open("https://www.youtube.com/shorts/YT7qzTh2Q7A", "_blank");
	};

	return (
		<div className="flex flex-col min-h-screen">
			<main className="flex-grow bg-gradient-to-b from-background to-background/95">
				<Navbar />
				<div className="container mx-auto px-4 py-6 space-y-16">
					<HeroSection onTabChange={setTab} />

					{/* Section 2: The Problem - Agitate the Pain */}
					<section className="max-w-4xl mx-auto py-16">
						<h2 className="text-3xl font-bold text-center mb-12">Sound familiar?</h2>
						<div className="space-y-6">
							<div className="flex items-start gap-4 p-4 bg-secondary/30 rounded-lg">
								<CheckCircle2Icon className="text-green-500 mt-1 flex-shrink-0" size={24} />
								<p className="text-lg">"Did I really do enough to deserve this promotion?"</p>
							</div>
							<div className="flex items-start gap-4 p-4 bg-secondary/30 rounded-lg">
								<CheckCircle2Icon className="text-green-500 mt-1 flex-shrink-0" size={24} />
								<p className="text-lg">"My biggest success was probably just a fluke."</p>
							</div>
							<div className="flex items-start gap-4 p-4 bg-secondary/30 rounded-lg">
								<CheckCircle2Icon className="text-green-500 mt-1 flex-shrink-0" size={24} />
								<p className="text-lg">"I'm terrified they'll ask me a question I can't answer and expose me."</p>
							</div>
							<div className="flex items-start gap-4 p-4 bg-secondary/30 rounded-lg">
								<CheckCircle2Icon className="text-green-500 mt-1 flex-shrink-0" size={24} />
								<p className="text-lg">"I'll just keep my head down and hope my hard work gets noticed."</p>
							</div>
						</div>
						<p className="text-center text-xl text-default-600 mt-8 italic">
							The voice of doubt gets its power from forgotten details.
						</p>
					</section>

					{/* Section 3: The Solution - Introduce the Weapon */}
					<section className="max-w-4xl mx-auto py-16">
						<h2 className="text-3xl font-bold text-center mb-8">Your Accomplishments Are Not Feelings. They Are Facts.</h2>
						<div className="bg-gradient-to-r from-purple-50 to-indigo-50 p-8 rounded-xl border border-purple-200">
							<p className="text-lg text-center leading-relaxed">
								For the professional who has done the work but struggles to show it, JAJA isn't just another prep tool—it's your personal system of proof. We help you find the hard data in your past and build the undeniable stories for your future.
							</p>
							<p className="text-lg text-center leading-relaxed mt-6">
								Unlike the chaos of scattered notes or the generic advice from AI chatbots, JAJA provides a single, secure vault to capture your achievements and testimonials. So you can walk into any high-stakes moment with the one thing Imposter Syndrome can't argue with: evidence.
							</p>
						</div>
					</section>

					{/* Section 4: How It Works */}
					<section className="max-w-5xl mx-auto py-16">
						<h2 className="text-3xl font-bold text-center mb-12">From Doubt to Dominance in 3 Steps</h2>
						<div className="grid md:grid-cols-3 gap-8">
							<Card className="text-center p-6">
								<div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
									<LineChartIcon className="text-purple-600" size={32} />
								</div>
								<h3 className="text-xl font-semibold mb-3">Capture Your Wins</h3>
								<p className="text-default-600">
									Instantly log accomplishments and colleague testimonials in your private 'brag book' the moment they happen. No more forgetting.
								</p>
							</Card>

							<Card className="text-center p-6">
								<div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
									<CodeIcon className="text-purple-600" size={32} />
								</div>
								<h3 className="text-xl font-semibold mb-3">Craft Your Stories</h3>
								<p className="text-default-600">
									Our AI helps you transform your data into compelling, interview-ready STAR stories. No more blank pages.
								</p>
							</Card>

							<Card className="text-center p-6">
								<div className="bg-purple-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
									<CheckCircle2Icon className="text-purple-600" size={32} />
								</div>
								<h3 className="text-xl font-semibold mb-3">Conquer Your Moment</h3>
								<p className="text-default-600">
									Walk into your promotion review or final interview with a library of proof. No more self-doubt.
								</p>
							</Card>
						</div>
					</section>

					{/* Section 5: Features as Benefits */}
					<section className="max-w-5xl mx-auto py-16">
						<h2 className="text-3xl font-bold text-center mb-12">The Anti-Imposter Syndrome Toolkit</h2>
						<div className="grid md:grid-cols-2 gap-8">
							<Card className="p-6">
								<div className="flex items-start gap-4">
									<InfoIcon className="text-purple-600 mt-1" size={32} />
									<div>
										<h3 className="text-xl font-semibold mb-2">The Accomplishment Vault</h3>
										<p className="text-default-600">
											Your permanent, searchable record of every success. The Glimmer-proof vault we talked about.
										</p>
									</div>
								</div>
							</Card>

							<Card className="p-6">
								<div className="flex items-start gap-4">
									<CodeIcon className="text-purple-600 mt-1" size={32} />
									<div>
										<h3 className="text-xl font-semibold mb-2">AI-Powered Story Engine</h3>
										<p className="text-default-600">
											Turns fragmented details into powerful narratives that sound like you, only more confident.
										</p>
									</div>
								</div>
							</Card>

							<Card className="p-6">
								<div className="flex items-start gap-4">
									<MessageSquareIcon className="text-purple-600 mt-1" size={32} />
									<div>
										<h3 className="text-xl font-semibold mb-2">Testimonial Capture</h3>
										<p className="text-default-600">
											Let the words of your colleagues silence your inner critic. Collect and store praise to use as undeniable third-party proof.
										</p>
									</div>
								</div>
							</Card>

							<Card className="p-6">
								<div className="flex items-start gap-4">
									<DownloadIcon className="text-purple-600 mt-1" size={32} />
									<div>
										<h3 className="text-xl font-semibold mb-2">You Own Your Data</h3>
										<p className="text-default-600">
											Your career story belongs to you, not your employer. Export it anytime. We are your trusted partner, not a data broker.
										</p>
									</div>
								</div>
							</Card>
						</div>
					</section>

					{/* Section 6: Social Proof */}
					<section className="max-w-4xl mx-auto py-16">
						<h2 className="text-3xl font-bold text-center mb-12">You're not alone in feeling this way.</h2>
						<div className="space-y-8">
							<Card className="p-8 bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200">
								<p className="text-lg italic mb-4">
									"Before JAJA, I'd freeze up when asked about my successes. I felt like a fraud. Now, I have a library of stories with real data to back them up. The confidence I felt in my last interview was a complete game-changer."
								</p>
								<p className="font-semibold text-purple-600">
									— Alex R., Senior Product Manager, formerly at [Company]
								</p>
							</Card>
						</div>
					</section>

					{/* Section 7: Final CTA */}
					<section className="max-w-4xl mx-auto py-16 text-center">
						<h2 className="text-3xl font-bold mb-6">Stop letting doubt define your value.</h2>
						<p className="text-xl text-default-600 mb-8">
							Your hard work deserves to be seen. Your accomplishments deserve to be heard. Start building the undeniable proof of your career today.
						</p>
						<Button
							className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-6 text-lg h-auto"
							color="primary"
							endContent={<ChevronRightIcon size={20} />}
							onPress={() => {
								setTab("waitlist");
								setTimeout(() => {
									document.getElementById("email-input")?.focus();
								}, 100);
							}}
						>
							Capture Your First Win for Free
						</Button>
						<p className="text-sm text-default-500 mt-4">
							<a href="#pricing" className="text-purple-600 hover:underline">See pricing plans</a>
						</p>
					</section>

					{/* Original sections kept for functionality */}
					<section className="max-w-4xl mx-auto bg-secondary/50 rounded-lg p-8">
						<h2 className="text-2xl font-bold text-center mb-6">Ready to ditch your spreadsheet?</h2>
						<Tabs
							aria-label="User Options"
							className="w-full"
							selectedKey={tab}
							onSelectionChange={(key) => setTab(key as string)}
						>
							<Tab key="waitlist" title="Join the Beta">
								<div className="space-y-4 mt-4">
									<p className="text-center text-default-600 mb-6">
										Reserve your spot in our closed beta. Limited to 100 users.
									</p>
									<WaitlistForm />
								</div>
							</Tab>
							<Tab key="developer" title="Do-It-Yourself Install">
								<div className="space-y-4 mt-4">
									<p className="text-center text-default-600 mb-6">
										Not technical? We'll help you get set up! Email us to book time with a friendly
										developer.
									</p>
									<DeveloperInfo />
								</div>
							</Tab>
						</Tabs>
					</section>

					<section className="max-w-3xl mx-auto bg-secondary/50 rounded-lg p-8 flex flex-col items-center text-center">
						<h2 className="text-2xl font-bold mb-4">See How It Works</h2>
						<p className="text-default-600 mb-6">Watch how we make job searching simpler</p>
						<Button
							className="bg-purple-600 hover:bg-purple-700"
							color="primary"
							onPress={handleWatchDemo}
							startContent={<PlayIcon size={16} />}
							variant="solid"
						>
							Watch Demo
						</Button>
					</section>
				</div>
			</main>

			<Footer />
		</div>
	);
};

export default Index;
