"use client";

import { Navbar as HeroUINavbar, NavbarContent, NavbarBrand, NavbarItem, Button } from "@heroui/react";
import NextLink from "next/link";
import { useRouter } from "next/navigation";

import { GoogleIcon } from "@/components/icons";

interface NavbarProps {
	isAuthenticated: boolean;
	hasPrevAuth: boolean;
	isFirstVisit: boolean;
}

export const Navbar = ({ isAuthenticated, hasPrevAuth, isFirstVisit }: NavbarProps) => {
	const router = useRouter();
	const apiUrl = process.env.NEXT_PUBLIC_API_URL!;

	const handleGoogleLogin = () => {
		router.push(`${apiUrl}/login`);
	};

	const handleLogout = () => {
		router.push("/logout");
	};

	return (
		<HeroUINavbar
			isBordered
			className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
			maxWidth="xl"
		>
			<NavbarContent className="basis-1/5 sm:basis-full" justify="start">
				<NavbarBrand as="li" className="gap-3 max-w-fit">
					<NextLink className="flex justify-start items-center gap-1" href="/">
						<div className="flex items-center gap-3">
							<img alt="Shining Nuggets Logo" className="h-12 w-12 object-contain" src="/logo.png" />
							<div className="flex flex-col">
								<span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-600 to-emerald-600">
									Just A Job App
								</span>
								<span className="text-xs text-default-500 -mt-1">
									Get the Unfair Advantage in Your Job Search.
								</span>
							</div>
						</div>
					</NextLink>
				</NavbarBrand>
			</NavbarContent>

			{/* Desktop/right side */}
			<NavbarContent className="hidden md:flex basis-1/5 sm:basis-full" justify="end">
				{isAuthenticated ? (
					<NavbarItem>
						<Button
							className="bg-amber-600 text-white hover:bg-amber-700"
							variant="solid"
							onPress={handleLogout}
						>
							Logout
						</Button>
					</NavbarItem>
				) : isFirstVisit ? (
					<NavbarItem>
						<Button
							as="a"
							className="bg-amber-600 text-white hover:bg-amber-700"
							href="#waitlist"
							variant="solid"
							onPress={() => {
								const waitlistSection = document.getElementById("waitlist");
								if (waitlistSection) {
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
					</NavbarItem>
				) : hasPrevAuth ? (
					<NavbarItem>
						<Button
							className="bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
							startContent={<GoogleIcon size={16} />}
							variant="bordered"
							onPress={handleGoogleLogin}
						>
							Login with Google
						</Button>
					</NavbarItem>
				) : (
					<NavbarItem>
						<Button
							as="a"
							className="bg-amber-600 text-white hover:bg-amber-700"
							href="#waitlist"
							variant="solid"
							onPress={() => {
								const waitlistSection = document.getElementById("waitlist");
								if (waitlistSection) {
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
					</NavbarItem>
				)}
			</NavbarContent>

			{/* Smaller screens */}
			<NavbarContent className="md:hidden" justify="end">
				{isAuthenticated ? (
					<Button
						className="bg-amber-600 text-white hover:bg-amber-700"
						size="sm"
						variant="solid"
						onPress={handleLogout}
					>
						Logout
					</Button>
				) : isFirstVisit ? (
					<Button
						as="a"
						className="bg-amber-600 text-white hover:bg-amber-700"
						href="#waitlist"
						size="sm"
						variant="solid"
						onPress={() => {
							const waitlistSection = document.getElementById("waitlist");
							if (waitlistSection) {
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
				) : hasPrevAuth ? (
					<Button
						className="bg-white border-gray-300 text-gray-700 hover:bg-gray-50"
						size="sm"
						startContent={<GoogleIcon size={16} />}
						variant="bordered"
						onPress={handleGoogleLogin}
					>
						Login with Google
					</Button>
				) : (
					<Button
						as="a"
						className="bg-amber-600 text-white hover:bg-amber-700"
						href="#waitlist"
						size="sm"
						variant="solid"
						onPress={() => {
							const waitlistSection = document.getElementById("waitlist");
							if (waitlistSection) {
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
				)}
			</NavbarContent>
		</HeroUINavbar>
	);
};
