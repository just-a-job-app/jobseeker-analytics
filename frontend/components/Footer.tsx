"use client";

import { useRouter } from "next/navigation";
import { Button } from "@heroui/react";

import { GoogleIcon } from "@/components/icons";

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
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">JustAJobApp</h3>
						<p className="text-default-500 mb-4">Automate the "Second Job" of Job Searching.</p>
						<a
							className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-700 transition-colors duration-200"
							href="/contributors"
						>
							<span className="mr-2">👋</span>
							Join the Community
						</a>
					</div>

					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">Support Us</h3>
						<p className="text-default-500 mb-4">Like the app? Buy us a coffee.</p>
						<a
							className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-black bg-yellow-400 hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors duration-200"
							href="https://www.buymeacoffee.com/justajobapp"
							rel="noopener noreferrer"
							target="_blank"
						>
							<span className="mr-2">☕</span>
							Buy us a coffee
						</a>
					</div>
					<div>
						<h3 className="text-lg font-semibold mb-4 text-emerald-700">Beta Testers</h3>
						<p className="text-default-500 mb-4">Log In Below.</p>
						<Button
							className="bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
							id="beta-login"
							startContent={<GoogleIcon size={16} />}
							variant="bordered"
							onPress={handleGoogleLogin}
						>
							Login with Google
						</Button>
					</div>
				</div>

				<div className="mt-12 pt-6 border-t text-center text-sm text-default-500">
					<div className="flex flex-col space-y-2 mb-4">
						<div className="flex flex-wrap justify-center gap-6">
							<a
								className="text-default-500 hover:text-default-700 dark:hover:text-default-300 transition-colors"
								href="/privacy"
							>
								Privacy Policy
							</a>
							<a
								className="text-default-500 hover:text-default-700 dark:hover:text-default-300 transition-colors"
								href="/terms"
							>
								Terms of Service
							</a>
							<a
								className="text-default-500 hover:text-default-700 dark:hover:text-default-300 transition-colors"
								href="/cookies"
							>
								Cookie Policy
							</a>
							<a
								className="text-default-500 hover:text-default-700 dark:hover:text-default-300 transition-colors"
								href="/dsar"
							>
								Data Requests
							</a>
						</div>
						<div className="flex flex-wrap justify-center gap-4 text-xs">
							<a
								className="text-default-400 hover:text-default-600 dark:hover:text-default-200 transition-colors"
								href="https://app.termly.io/notify/a8dc31e4-d96a-461e-afe0-abdec759bc97"
								rel="noopener noreferrer"
								target="_blank"
							>
								Do Not Sell or Share My Personal Information
							</a>
							<a
								className="text-default-400 hover:text-default-600 dark:hover:text-default-200 transition-colors"
								href="https://app.termly.io/notify/a8dc31e4-d96a-461e-afe0-abdec759bc97"
								rel="noopener noreferrer"
								target="_blank"
							>
								Limit the Use Of My Sensitive Personal Information
							</a>
							<a
								className="text-default-400 hover:text-default-600 dark:hover:text-default-200 transition-colors"
								href="#"
							>
								Change My Consent Preferences
							</a>
						</div>
					</div>
					<p className="mt-2 text-amber-600 font-medium">© {new Date().getFullYear()} JustAJobApp LLC</p>
				</div>
			</div>
		</footer>
	);
};

export default Footer;
