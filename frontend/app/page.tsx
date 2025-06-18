"use client";

import { useState } from "react";
import { Button, Card, Input } from "@heroui/react";

import { Navbar } from "@/components/navbar";
import Footer from "@/components/Footer";
import { PAGE_TEXT } from "./constants/text";

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
			setMessage(PAGE_TEXT.messages.success[type]);
			setEmail("");
		} catch (error) {
			setStatus("error");
			setMessage(PAGE_TEXT.messages.error);
		}
	};

	return (
		<div className="flex flex-col min-h-screen">
			<main className="flex-grow bg-gradient-to-b from-background to-background/95">
				<Navbar />
				<div className="container mx-auto px-4 py-6 space-y-16">
					{/* Section 1: The Header - The Focused Hook */}
					<section className="max-w-4xl mx-auto text-center py-12 pb-8">
						<h1 className="text-3xl md:text-6xl font-bold mb-6 pb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-600 to-indigo-600 leading-[1.2]">
							{PAGE_TEXT.header.title}
						</h1>
						<p className="text-xl md:text-2xl text-default-500 mb-10 max-w-3xl mx-auto">
							{PAGE_TEXT.header.subtitle}
						</p>
						<Button
							className="bg-purple-600 hover:bg-purple-700 text-white px-8 py-6 text-lg h-auto"
							color="primary"
							onPress={scrollToOptions}
						>
							{PAGE_TEXT.header.cta}
						</Button>
					</section>

					{/* Section 2: The Problem - The Shared Frustration */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">{PAGE_TEXT.problem.title}</h2>
						<div className="prose prose-lg mx-auto text-default-600">
							<p className="text-xl mb-4">{PAGE_TEXT.problem.subtitle}</p>
							{PAGE_TEXT.problem.description.map((text, index) => (
								<p key={index} className={index === 0 ? "mb-4" : ""}>
									{text}
								</p>
							))}
						</div>
					</section>

					{/* Section 3: The Solution - The Full Vision */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">{PAGE_TEXT.solution.title}</h2>
						<div className="prose prose-lg mx-auto text-default-600">
							{PAGE_TEXT.solution.description.map((text, index) => (
								<p key={index} className={index < PAGE_TEXT.solution.description.length - 1 ? "mb-4" : ""}>
									{text}
								</p>
							))}
						</div>
					</section>

					{/* Section 4: The Blueprint - How It Will Work */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">{PAGE_TEXT.blueprint.title}</h2>
						<p className="text-center text-default-600 mb-8">{PAGE_TEXT.blueprint.subtitle}</p>
						<div className="grid md:grid-cols-3 gap-8">
							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">{PAGE_TEXT.blueprint.steps.step1.title}</h3>
									<p className="text-default-500 mb-4">{PAGE_TEXT.blueprint.steps.step1.description}</p>
									<div className="bg-default-100 p-4 rounded-lg">
										<p className="text-sm italic text-default-600">{PAGE_TEXT.blueprint.steps.step1.example}</p>
									</div>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">{PAGE_TEXT.blueprint.steps.step2.title}</h3>
									<p className="text-default-500">{PAGE_TEXT.blueprint.steps.step2.description}</p>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">{PAGE_TEXT.blueprint.steps.step3.title}</h3>
									<p className="text-default-500 mb-4">{PAGE_TEXT.blueprint.steps.step3.description}</p>
									<div className="bg-default-100 p-4 rounded-lg">
										<p className="text-sm italic text-default-600">{PAGE_TEXT.blueprint.steps.step3.example}</p>
									</div>
								</div>
							</Card>
						</div>
					</section>

					{/* Section 5: Who This Is For */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">{PAGE_TEXT.audience.title}</h2>
						<div className="grid md:grid-cols-2 gap-8">
							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4 text-green-600">{PAGE_TEXT.audience.forYou.title}</h3>
									<ul className="space-y-3 text-default-600">
										{PAGE_TEXT.audience.forYou.items.map((item, index) => (
											<li key={index} className="flex items-start gap-2">
												<span className="text-green-500">✓</span>
												<span>{item}</span>
											</li>
										))}
									</ul>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4 text-red-600">{PAGE_TEXT.audience.notForYou.title}</h3>
									<ul className="space-y-3 text-default-600">
										{PAGE_TEXT.audience.notForYou.items.map((item, index) => (
											<li key={index} className="flex items-start gap-2">
												<span className="text-red-500">✗</span>
												<span>{item}</span>
											</li>
										))}
									</ul>
								</div>
							</Card>
						</div>
					</section>

					{/* Section 6: The Founder & The Ask */}
					<section className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">{PAGE_TEXT.founder.title}</h2>
						<div className="prose prose-lg mx-auto text-default-600">
							{PAGE_TEXT.founder.description.map((text, index) => (
								<p key={index} className={index < PAGE_TEXT.founder.description.length - 1 ? "mb-4" : ""}>
									{text}
								</p>
							))}
						</div>
					</section>

					{/* Section 7: The Final CTA */}
					<section id="join-options" className="max-w-4xl mx-auto py-12">
						<h2 className="text-3xl font-bold text-center mb-8">{PAGE_TEXT.join.title}</h2>
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
									<h3 className="text-xl font-semibold mb-4">{PAGE_TEXT.join.options.updates.title}</h3>
									<p className="text-default-500 mb-6">{PAGE_TEXT.join.options.updates.description}</p>
									<form className="space-y-4" onSubmit={(e) => handleNewsletterSignup(e, "founding")}>
										<Input
											className="w-full"
											placeholder={PAGE_TEXT.join.options.updates.placeholder}
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
											{PAGE_TEXT.join.options.updates.button}
										</Button>
									</form>
								</div>
							</Card>

							<Card>
								<div className="p-6">
									<h3 className="text-xl font-semibold mb-4">{PAGE_TEXT.join.options.diy.title}</h3>
									<div className="aspect-w-16 aspect-h-9 mb-4">
										<iframe
											src="https://www.youtube.com/embed/6LXlCdcsXPE"
											title="Step-by-step DIY Install Tutorial"
											allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
											allowFullScreen
											className="w-full h-full rounded-lg"
										></iframe>
									</div>
									<p className="text-default-500 mb-6">
										{PAGE_TEXT.join.options.diy.description}
									</p>
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
