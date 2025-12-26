"use client";

import { Navbar as HeroUINavbar, NavbarContent, NavbarBrand, NavbarItem } from "@heroui/react";
import NextLink from "next/link";

export const Navbar = () => {
	return (
		<>
			<HeroUINavbar
				isBordered
				className="sticky top-0 z-40 border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
				maxWidth="xl"
			>
				{/* Desktop Layout */}
				<div className="hidden md:flex w-full justify-between items-center">
					<NavbarContent justify="start">
						<NavbarBrand as="li" className="gap-3 max-w-fit">
							<NextLink className="flex justify-start items-center gap-1" href="/">
								<div className="flex items-center gap-3">
									<img
										alt="Shining Nuggets Logo"
										className="h-12 w-12 object-contain"
										src="/logo.png"
									/>
									<div className="flex flex-col">
										<span className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-600 to-emerald-600">
											JustAJobApp
										</span>
										<span className="text-xs text-default-500 -mt-1">
											Automate the "Second Job" of Job Searching.
										</span>
									</div>
								</div>
							</NextLink>
						</NavbarBrand>
					</NavbarContent>

					<NavbarContent justify="end">
						<NavbarItem>
							<a
								className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-black bg-yellow-400 hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors duration-200"
								href="https://www.buymeacoffee.com/justajobapp"
								rel="noopener noreferrer"
								target="_blank"
							>
								<span className="mr-2">☕</span>
								Buy us a coffee
							</a>
						</NavbarItem>
					</NavbarContent>
				</div>

				{/* Mobile Layout - Just Logo */}
				<div className="md:hidden w-full flex justify-center py-2">
					<NavbarBrand className="flex justify-center">
						<NextLink className="flex justify-center items-center gap-1" href="/">
							<div className="flex items-center gap-3">
								<img alt="Shining Nuggets Logo" className="h-10 w-10 object-contain" src="/logo.png" />
								<div className="flex flex-col">
									<span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-amber-600 to-emerald-600">
										JustAJobApp
									</span>
									<span className="text-xs text-default-500 -mt-1">
										Automate the "Second Job" of Job Searching.
									</span>
								</div>
							</div>
						</NextLink>
					</NavbarBrand>
				</div>
			</HeroUINavbar>

			{/* Mobile Sticky Button */}
			<div className="md:hidden fixed bottom-4 left-1/2 transform -translate-x-1/2 z-50">
				<a
					className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-black bg-yellow-400 hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-colors duration-200 shadow-lg hover:shadow-xl"
					href="https://www.buymeacoffee.com/justajobapp"
					rel="noopener noreferrer"
					target="_blank"
				>
					<span className="mr-2">☕</span>
					Buy us a coffee
				</a>
			</div>
		</>
	);
};
