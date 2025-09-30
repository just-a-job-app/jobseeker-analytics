"use client";

import { useCallback } from "react";

// Function to create a firework particle effect
const createFireworkEffect = (element: HTMLElement) => {
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

export const useFireworks = () => {
	const triggerFireworks = useCallback((targetId: string) => {
		const targetElement = document.getElementById(targetId);
		if (targetElement) {
			// Add golden sparkle border animation
			targetElement.classList.add("golden-sparkle-border");

			// Create firework particle effect
			createFireworkEffect(targetElement);

			// Remove the animation class after 2 seconds
			setTimeout(() => {
				targetElement.classList.remove("golden-sparkle-border");
			}, 2000);
		}
	}, []);

	return { triggerFireworks };
};
