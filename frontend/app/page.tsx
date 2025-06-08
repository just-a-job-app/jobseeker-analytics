"use client";

import { useState } from "react";
import { Button, Card, Tabs, Tab } from "@heroui/react";

import { UsersIcon, LineChartIcon, CheckCircle2Icon, PlayIcon } from "@/components/icons";
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

					<section className="max-w-5xl mx-auto py-8">
						<h2 className="text-3xl font-bold text-center mb-10">Why Just a Job App?</h2>
						<div className="grid md:grid-cols-3 gap-8">
							<Card>
								<div className="p-6">
									<LineChartIcon className="text-purple-500 mb-4" size={48} />
									<h3 className="text-xl font-semibold mb-2">Automatic Tracking</h3>
									<p className="text-default-500">
										No more manual updates. We track your applications straight from your inbox.
									</p>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<CheckCircle2Icon className="text-purple-500 mb-4" size={48} />
									<h3 className="text-xl font-semibold mb-2">Independent</h3>
									<p className="text-default-500">
										Built by jobseekers, for jobseekers. No VC funding.
									</p>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<UsersIcon className="text-purple-500 mb-4" size={48} />
									<h3 className="text-xl font-semibold mb-2">Built in Public</h3>
									<p className="text-default-500">
										Join our community of contributors and help fix the job search.
									</p>
								</div>
							</Card>
						</div>
					</section>

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
							startContent={<PlayIcon size={16} />}
							variant="solid"
							onPress={handleWatchDemo}
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
