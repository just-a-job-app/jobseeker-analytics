"use client";

import { useRouter } from "next/navigation";
import { Button } from "@heroui/react";

import { ExternalLinkIcon, GoogleIcon } from "@/components/icons";

// Function to create a firework particle effect
// Exported so it can be used from other components
export const createFireworkEffect = (element: HTMLElement) => {
	// Number of particles - reduced for a quicker effect
	const particleCount = 30;

	// Get element position for centering the effect
	const rect = element.getBoundingClientRect();
	const centerX = rect.left + rect.width / 2;
	const centerY = rect.top + rect.height / 2;

	// Create container for particles
	const container = document.createElement("div");
	container.style.position = "fixed";
	container.style.left = "0";
	container.style.top = "0";
	container.style.width = "100%";
	container.style.height = "100%";
	container.style.pointerEvents = "none";
	container.style.zIndex = "9999";
	document.body.appendChild(container);

	// Create particles
	for (let i = 0; i < particleCount; i++) {
		const particle = document.createElement("div");

		// Random particle properties
		const size = Math.random() * 8 + 4; // 4-12px
		const angle = Math.random() * Math.PI * 2; // 0-360 degrees
		const distance = Math.random() * 100 + 50; // 50-150px

		// Calculate final position
		const destinationX = centerX + Math.cos(angle) * distance;
		const destinationY = centerY + Math.sin(angle) * distance;

		// Set particle styles
		particle.style.position = "absolute";
		particle.style.width = `${size}px`;
		particle.style.height = `${size}px`;
		particle.style.backgroundColor = `rgba(255, ${150 + Math.random() * 100}, 0, ${Math.random() * 0.5 + 0.5})`; // Golden colors
		particle.style.borderRadius = "50%";
		particle.style.left = `${centerX}px`;
		particle.style.top = `${centerY}px`;
		particle.style.transform = "translate(-50%, -50%)";
		particle.style.boxShadow = "0 0 10px 2px rgba(255, 215, 0, 0.8)";

		// Add to container
		container.appendChild(particle);

		// Animate particle - shorter duration
		const duration = Math.random() * 800; // 700-1500ms

		// Create and start animation
		particle.animate(
			[
				{
					left: `${centerX}px`,
					top: `${centerY}px`,
					opacity: 1,
					transform: "translate(-50%, -50%) scale(0)"
				},
				{
					left: `${destinationX}px`,
					top: `${destinationY}px`,
					opacity: 0,
					transform: "translate(-50%, -50%) scale(1)"
				}
			],
			{
				duration,
				easing: "cubic-bezier(0.075, 0.82, 0.165, 1)",
				fill: "forwards"
			}
		);
	}

	// Remove container after animation
	setTimeout(() => {
		document.body.removeChild(container);
	}, 3000);
};

const Footer = () => {
	const router = useRouter();
	const apiUrl = process.env.NEXT_PUBLIC_API_URL!;

	const handleGoogleLogin = () => {
		router.push(`${apiUrl}/login`);
	};

	return (
		<footer className="border-t py-12 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
			<div className="container mx-auto px-4">
				<div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center md:text-left">
					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">Just A Job App</h3>
						<p className="text-default-500 mb-4">
							Designed for ambitious professionals. <br />
							Built to fix a broken system.
						</p>
					</div>

					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">
							Get the Unfair Advantage in Your Job Search.
						</h3>
						<p className="text-default-500 mb-4">
							Join 300+ ambitious professionals on the priority list. We'll give you early access to the
							tools that turn your hidden achievements into your next big opportunity.
						</p>
						<a
							className="flex items-center justify-center md:justify-start gap-2 text-sm text-amber-600 hover:text-amber-700 transition-colors font-medium"
							href="#waitlist"
							onClick={() => {
								// Add fireworks animation to waitlist section
								const waitlistSection = document.getElementById("waitlist");
								if (waitlistSection) {
									waitlistSection.classList.add("golden-sparkle-border");

									// Create actual firework particles on top for extra effect
									createFireworkEffect(waitlistSection);

									// Remove the animation class after a shorter time
									setTimeout(() => {
										waitlistSection.classList.remove("golden-sparkle-border");
									}, 2000);
								}
							}}
						>
							<ExternalLinkIcon size={16} />
							Request Early Access
						</a>
					</div>
					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">Already a Beta Tester?</h3>
						<p className="text-default-500 mb-4">Log In Below.</p>
						<Button
							className="bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
							startContent={<GoogleIcon size={16} />}
							variant="bordered"
							onPress={handleGoogleLogin}
						>
							Login with Google
						</Button>
					</div>
				</div>

				<div className="mt-12 pt-6 border-t text-center text-sm text-default-500">
					<p className="mt-2 text-amber-600 font-medium">© {new Date().getFullYear()} Just A Job App</p>
				</div>
			</div>
		</footer>
	);
};

export default Footer;
